import covasim as cv
import abmshare.utils as exut
import multiprocessing as mp
import abmshare.defaults as exdf
import abmshare.covasim_ex.mobility as mb
import abmshare.covasim_ex.simulation_conf_getter as exscg
from abmshare.covasim_ex.region import Region
import abmshare.covasim_ex.intervention_process as exip
from pytictoc import TicToc
import datetime
import functools
import concurrent.futures

class Simulation_creator():
    def __init__(self,configuration:dict,
                 parallel_run:bool=False,
                 wait:bool=False,
                 test:bool=False,
                 save_settings:dict=None,
                 unique_mobility_indexes:dict=False,
                 override_pop_location:bool=False,
                 mobility:bool=None):
        """_summary_

        Args:
            configuration (dict): _description_
            wait (bool, optional): _description_. Defaults to False.
            test (bool, optional): _description_. Defaults to False.
            save_settings (dict, optional): _description_. Defaults to None.
        """
        if not isinstance(configuration,dict):
            configuration=exut.load_config(configuration)
        self.configuration=configuration   
        self.test=self.configuration.get("test",False) or test
        self.parallel_run=parallel_run 
        self.override_pop_location=override_pop_location        
        self.save_settings=save_settings or {}
        self.mobility=mobility        
        # Simulation parameters
        self.region_objects={}
        self.simulation_days=None
        self.multisim_result=None        
        self.region_objects_result={}
        self.shared_mobility_exclude = list()
        self.unique_mobility_indexes=exscg.get_global_pars(self.configuration,'unique_mobility_indexes') or unique_mobility_indexes
        # Initialize new immunity data and variants
        if not wait: 
            self.process()

    def process(self):
        # Core processing class
        if not self.parallel_run: self.run_single_core_sims()
        else: self.run_multi_core_sims() 
        # Save multisim object
        self.save_multisim_object()
        
    def run_single_core_sims(self):
        """_summary_

        """
        tic=TicToc()
        tic.tic()
        # Sim preparation
        for location_code in exscg.get_region_codes(self.configuration):
            self.sim_creation_process(location_code=location_code)
        self.simulation_days=(next(iter(self.region_objects.values()))).get_days()+1 
        # Initial interaction for all simulations
        if self.mobility and self.unique_mobility_indexes:
            mb.interactions(self.region_objects,init=True) 
        elif self.mobility and not self.unique_mobility_indexes:
            mb.interactions(self.region_objects,init=True)
        # Run sims
        for t in range(self.simulation_days):            
            print(f"Running sim for day:{t}")            
            exclude_regions=[]
            for region in self.region_objects.values():
                # Prepare mobility keys to exclude
                actual_date=datetime.datetime.strptime(region.cv_simulation.date(t),'%Y-%m-%d')
                if t==0:
                    print(f"Starting simulation date:{actual_date}") 
                region.run_step()
                # Now handle mobility intervention when is turned
                for change in region.mobility_intervention_list:
                    if not self.mobility:
                        break #NOTE: narovnak na ohybak
                    if (change.start_day <= t <= change.end_day):
                        exclude_regions.append(region.location_code)
            # Handle all intervention. Exclude from sync those, which are locked down
            if len(set(exclude_regions)) < len(self.region_objects) and self.mobility:
                mb.interactions({key:self.region_objects[key] for key in self.region_objects.keys() if key not in exclude_regions},init=False)
            # Print
            print(f"Actually infected: {int(sum([sum(region.cv_simulation.results['new_infections']) for region in self.region_objects.values()]))}\n"+
                  f"Total deaths: {int(sum([sum(region.cv_simulation.results['cum_deaths']) for region in self.region_objects.values()]))}\n"+
                  f"From totall population length: {int(sum([region.population_size for region in self.region_objects.values()]))}\n")
        # Finalize sims
        for val in self.region_objects.values():
            val.finalize_simulation()
        tic.toc("Simulations done in:")
        # Create multisim object
        self.multisim_result=cv.MultiSim([val.cv_simulation for val in self.region_objects.values()])
                        
    def sim_creation_process(self, location_code:str,shared_dict=None):
        region = Region(location_code=location_code,
                                                            name=exscg.get_region_name(config=self.configuration,code=location_code),
                                                            population_size=exscg.get_pop_size_by_code(config=self.configuration,code=location_code),
                                                            mobility_data=exscg.get_mobility_data_by_code(config=self.configuration,code=location_code),
                                                            mobility_incoming_data=exscg.get_incoming_mobility_data_by_code(config=self.configuration,code=location_code),
                                                            intervention_list=exip.process_interventions(interventions=exscg.get_interventions_by_code(config=self.configuration,code=location_code),
                                                                                                            config=self.configuration),
                                                            variant_list=exip.create_variants(config=self.configuration,code=location_code),
                                                            region_pars=exscg.get_pars_by_code(config=self.configuration,code=location_code),
                                                            save_settings=self.save_settings,
                                                            test=self.test,
                                                            override_pop_location=self.override_pop_location)
        region.initialize_simulation()
        if shared_dict is not None:
            shared_dict[location_code] = region
        else:
            self.region_objects[location_code] = region

    def sim_simulation_process(self, region: Region, t: int):
        exclude_list_for_this_process = []
        region.run_step()
        for change in region.mobility_intervention_list:
            if not self.mobility: break #NOTE: narovnak na ohybak
            if (change.start_day <= t <= change.end_day):
                exclude_list_for_this_process.append(region.location_code)
        self.region_objects_result[region.location_code] = region
        self.shared_mobility_exclude=exclude_list_for_this_process

    def run_multi_core_sims(self):
        # Timer
        tic = TicToc()
        tic.tic()
        # First parallelly create region object and initialize it
        manager = mp.Manager()
        shared_region_objects = manager.dict()

        simulation_codes = exscg.get_region_codes(self.configuration)

        # Use functools.partial to pass the shared dict to your function
        func = functools.partial(self.sim_creation_process,shared_dict=shared_region_objects)
        with mp.Pool(processes=min(len(simulation_codes), mp.cpu_count())) as pool:
            pool.map(func, simulation_codes)
        # Convert back to regular dictionary after multiprocessing is done
        self.region_objects = dict(shared_region_objects)
        # Handle init mobility interactions
        if self.mobility and self.unique_mobility_indexes:
            mb.interactions(self.region_objects,init=True)
        elif self.mobility and not self.unique_mobility_indexes:
            mb.interactions(self.region_objects,init=True) 
        else:
            pass
            # TODO: future to default version with no randoms  
        self.simulation_days=(next(iter(self.region_objects.values()))).get_days()+1 

        # Run the simulation in parallel and synchro mobility
        for t in range(self.simulation_days):
            print(f"Running multisimulation for day:{t}")
            # Run the simulations in parallel for this day
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = list(executor.map(lambda obj: self.sim_simulation_process(obj, t), self.region_objects.values()))

            if len(set(self.shared_mobility_exclude)) < len(self.region_objects_result) and self.mobility:
                keys_not_excluded = [key for key in self.region_objects_result.keys() if key not in self.shared_mobility_exclude]
                relevant_region_objects = {key: self.region_objects_result[key] for key in keys_not_excluded}
                mb.interactions(relevant_region_objects, init=False)
            # Print
            print(f"Actually infected: {int(sum([sum(region.cv_simulation.results['new_infections']) for region in self.region_objects.values()]))}\n"+
                  f"Total deaths: {int(sum([sum(region.cv_simulation.results['n_dead']) for region in self.region_objects.values()]))}\n"+
                  f"From totall population length: {int(sum([region.population_size for region in self.region_objects.values()]))}\n")

        # Finalize sims after all days are simulated
        self.region_objects = dict(self.region_objects_result)
        for val in self.region_objects.values():
            val.finalize_simulation()
        self.multisim_result=cv.MultiSim([val.cv_simulation for val in self.region_objects.values()])
        
    def save_multisim_object(self):
        if not self.save_settings:
            print("Save settings is not defined. Nowhere to save simulation.")
        else:
            self.save_settings['sim_location']=exut.merge_twoPaths(self.save_settings['location'],exdf.default_multisim_object_rel_path)
            self.multisim_result.save(self.save_settings['sim_location'])

# if __name__=="__main__":
#     config="/home/jedimik/Github/ABMShare/new_simulation.json"
#     save_settings={
#         "value": True,
#         "auto_increment": True,
#         "dirname": "Simulation",
#         "location": "/home/jedimik/Github/ABMShare/local_testing/outputs",
#         "copy_files": {
#             "copy_loaded_pop": True
#         }
#     }
#     meh=Simulation_creator(configuration=config,save_settings=save_settings,override_pop_location=False,test=True,parallel_run=True)
#     print()