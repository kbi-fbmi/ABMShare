from ctypes import sizeof
import numpy as np
import covasim as cv
import datetime
from covasim.utils import false
import extensions.utils as exut
import multiprocessing as mp
import extensions.covasim_ex.mobility_old as mb
import extensions.defaults as exdf
import extensions.covasim_ex.configuration_holder as cp
import synthpops as sp
import os
from pytictoc import TicToc
import sciris as sc
from pathlib import Path


class MobilityMultiSim():
    def __init__(self,extension_controller,configurationpath=None,mobilitypath=None,populationpath=None,scale=1,pop_infected=None,
                 test=False,wait=False,save_settings={},override_pop_location=False,initialized_modules=None):
        '''
            extension_controller (ExtensionController)                       : Extension controller
            configurationpath (dict)                                         : Path for Configuration, can hold various key=>values, for sim specification
            mobilitypath (string)                                            : *.xlsx file same as pattern in data, Can be given or loaded default
            populationpath (string)                                          : *.xlsx file same as pattern in data, Can be given or loaded default / NOT IMPLEMENTED YET
            scale(double)                                                    : if 1 then its all persons simulated.. Default 1
            wait (bool)                                                      : if not start process
            save_settings(dict)                                              : speccified save settings from extension caller
            override_pop_location(bool)                                      : if popfiles are located already in new output folder. - Given by extension controller
            initialized_modules(dict)                                        : if modules are initialized already
        '''
        #Params
        self.extension_controller=extension_controller
        self.configurationpath=configurationpath
        self.mobilitypath=mobilitypath
        self.populationpath=populationpath        
        self.scale=scale
        self.mobility=None # Holds list of travelling people for every sim.
        self.population=None # Holds list of population == num of regions (sims)
        self.popinfected=pop_infected
        self.sims = [] #sims as list
        self.interventions=[] #interventions as list of dicts, for each sim
        self.constructor_pars=[] #constructor pars as list of dicts for each sim
        self.simulation_pars=[] # pars for cv.Sim(pars)
        self.mobility_changes=[] #mobility changes as list od dicts for each sim   
        self.variant_list=[]
        self.popfile_file_list=[] #List containing sorted list of popfiles
        self.run_settings=dict()     
        self.configuration=None
        self.covasim_conf=None
        self.result=None
        self.result_list=[] #TODO: test
        self.test=test
        self.save_settings=save_settings
        self.override_pop_location=override_pop_location
        self.initialized_modules=initialized_modules
        # Loaders
        self.covasim_conf=cp.ConfigurationHolder(self.load_conf(self.configurationpath),self.test)
        self.number_of_sims=self.covasim_conf.return_number_of_sims()
        self.load_pop_and_mob(self.mobilitypath,self.populationpath)
        self.check_config_test()
        self.run_settings=self.covasim_conf.return_pars('run_settings_pars')
        if not wait:
            self.run_simulation()
            self.save_multisim()
        
    def load_pop_and_mob(self,mobilitypath=None,populationpath=None):
        '''
            Method for initializing mobility and population data. If there is no data given, it loads defaults
            Method is called in constructor, no need to call it directly.
            !!Important!! always use absolute path if data are given.
        '''
        if  self.mobilitypath is not None:
            mobility=exut.load_datafile(self.mobilitypath)
        elif self.covasim_conf.mobility_path is not None and self.covasim_conf.mobility_path!="":
            mobility=exut.load_datafile(self.covasim_conf.mobility_path)
        else:
            mobility = None
        if mobility is not None:
            self.mobility=np.asarray(mobility[mobility.columns[2:]])*self.scale
            self.mobility[np.isnan(self.mobility)] = 0           

        if self.populationpath is not None:
            population=exut.load_datafile(self.covasim_conf.population_path)
        elif self.covasim_conf.population_path: 
            population=exut.load_datafile(self.covasim_conf.population_path)      
        else:
            population=exut.load_datafile(exut.merge_file_path(exdf.pathvalues['population_path']))
        if population is not None:
            self.population=np.array(population.population*self.scale,dtype=int)  
        return
    
    def check_config_test(self):
        if  self.covasim_conf.test and not self.test:
            self.test=False         

    def load_conf(self,filepath=None):
        '''
            If there is no filepath, then load default.    
            !!Important!! always use absolute path if data are given.
        '''
        if filepath is None: # if is none, load default
            self.configuration=exut.load_config(exut.merge_file_path(exdf.pathvalues['default_configuration']))
        else:
            self.configuration=exut.load_config(filepath)        
        return self.configuration

    def save_multisim(self):
        save_pars=self.covasim_conf.save_pars #shorter usage
        if self.save_settings:
            self.save_settings['sim_location']=os.path.join(self.save_settings['location'],"sims/simulation.msim")
            self.result.save(self.save_settings['sim_location']) 
        elif save_pars:
            self.save_settings['sim_location']=os.path.join(save_pars['dir_path'],save_pars['filename'])
            self.result.save(self.save_settings['sim_location'])
        else:
            exut.directory_validator(exut.merge_default_path("UndefinedOutput"))    
            self.save_settings['sim_location']=os.path.join(exut.merge_default_path("UndefinedOutput"),"NoNamedSimulation.msim")
            self.result.save(self.save_settings['sim_location'])
        print(f"Ulozeno do{self.save_settings['sim_location']}")
        return

    def create_interventions(self,id,config=None):
        '''
            Method for creating interventions. Interventions can be region/sim specific, or global
            for every sim provided. It is called in method, which is creating sims.
        '''
        #If conf is supplied
        if config is not None:
            conf=config
        else:
            conf = self.covasim_conf.return_pars('interventions')
        if conf is None: #If there are no interventions and no config is supplied
            for i in range(self.covasim_conf.return_number_of_sims()):
                self.interventions.append(None)
                return
        elif len(conf)==1: #if there is only global_conf
            id=0
        
        for intervention in conf[id]:
            #If its beta_change intervention            
            if intervention['type']=="beta_change":                
                # First check for parameter validity, otherwise dont include intervention
                if not exut.validate_items_in_lists(list(intervention.keys()),exdf.interventions['beta_change']):
                    print(f"Cannot integrate intervention:{intervention}. Check if you have valid keys:\
                           {exdf.interventions['beta_change']}")
                    continue
                if not('label' in intervention and intervention['label']):
                    label=None
                else:
                    label=intervention['label']
                # Add beta intervention
                try:
                    beta_change=[float(x) for x in intervention['beta_change']]
                    if len(beta_change)==1:
                        beta_change.append(1)
                except:
                    beta_change=[float(intervention['beta_change']),float(1)]
                # Check days
                if 'days' in intervention and intervention['days'] and len(beta_change)==len(intervention['days']):
                    days=intervention['days']                    
                elif ('start_day' in intervention and intervention['start_day']) and ('end_day' in intervention and intervention['end_day']):
                    days=[intervention['start_day'],intervention['end_day']]
                else:                    
                    print(f"Cannot create beta intervention for days{intervention['days']} when beta changes is not a list {beta_change}. Otherwise check for same length")
                    continue
                try:
                    self.interventions[id].append(cv.change_beta(
                            days=days,
                            changes=beta_change,
                            layers=intervention['layers'],
                            label=label))
                except Exception as e:
                    print(f"Cannot create intervention {intervention} due to: {str(e)}")            
                
            #If its mobility change intervention
            elif intervention['type']=='mobility_change' and self.mobility is not None:
                # First check for parameter validity, otherwise dont include intervention
                if not exut.validate_items_in_lists(list(intervention.keys()),exdf.interventions['mobility_change']):
                # not list(intervention.keys())==exdf.interventions['mobility_change']:
                    print(f"Cannot integrate intervention:{intervention}. Check if you have valid keys:\
                           {exdf.interventions['mobility_change']}")
                    continue
                # Add mobility intervention                
                self.mobility_changes[id].append(
                    [datetime.datetime.strptime(intervention['start_day'],'%Y-%m-%d'),
                    datetime.datetime.strptime(intervention['end_day'],'%Y-%m-%d')])
                
            #If its clip_edges - Isolate contacts intervention
            elif intervention['type']=="isolate_contacts":
                if not exut.validate_items_in_lists(list(intervention.keys()),exdf.interventions['isolate_contacts']):
                    print(f"Cannot integrate intervention:{intervention}. Check if you have valid keys:\
                           {exdf.interventions['isolate_contacts']}")
                    continue
                layers=exut.validate_key_and_value(intervention,"layers")            
                label=exut.validate_key_and_value(intervention,"label")
                try:
                    self.interventions[id].append(cv.clip_edges(days=intervention['days'],
                                        changes=intervention['changes'],
                                        layers=layers,
                                        label=label))                
                except Exception as e:
                    print(f"Cannot create intervention {intervention} due to: {str(e)}")            
            # Testing test_num
            elif intervention['type']=="per_day_testing":
                if not exut.validate_items_in_lists(list(intervention.keys()),exdf.interventions['per_day_testing']):
                    print(f"Cannot integrate intervention: {intervention} check for valid keys:\
                          {exdf.interventions['per_day_testing']}")
                    continue
                exut.assign_intervention_keys(intervention,exdf.interventions['per_day_testing'],exdf.default_per_day_testing_values)
                try:
                    self.interventions[id].append(cv.test_num(
                    daily_tests=intervention['daily_tests'], symp_test=intervention['symp_test'], quar_test=intervention['quar_test'],
                    quar_policy=intervention['quar_policy'], subtarget=intervention['subtarget'],
                    ili_prev=intervention['ili_prev'], sensitivity=intervention['sensitivity'], loss_prob=intervention['loss_prob'], test_delay=intervention['daily_tests'],
                    start_day=intervention['start_day'], end_day=intervention['end_day'], swab_delay=intervention['swab_delay'],label=intervention['label']
                    ))
                except Exception as e:
                    print(f"Cannot create intervention: {intervention} due to:{str(e)} check for valid keys and values.")
            # Testing prob
            elif intervention['type']=="testing_probability":
                if not exut.validate_items_in_lists(list(intervention.keys()),exdf.interventions['testing_probability']):
                    print(f"Cannot integrate intervention: {intervention} check for valid keys:\
                          {exdf.interventions['testing_probability']}")
                    continue
                exut.assign_intervention_keys(intervention,exdf.interventions['testing_probability'],exdf.default_prob_testing_values)
                try:
                    self.interventions[id].append(cv.test_prob(
                        symp_prob=intervention['symp_prob'],asymp_prob=intervention['asymp_prob'],symp_quar_prob=intervention['symp_quar_prob'],
                        asymp_quar_prob=intervention['asymp_quar_prob'],quar_policy=intervention['quar_policy'],subtarget=intervention['subtarget'],
                        ili_prev=intervention['ili_prev'],sensitivity=intervention['sensitivity'],loss_prob=intervention['loss_prob'],
                        test_delay=intervention['test_delay'],start_day=intervention['start_day'],end_day=intervention['end_day'],
                        label=intervention['label']
                    ))
                except Exception as e:
                    print(f"Cannot create intervention: {intervention} due to:{str(e)} check for valid keys and values.")
            # Contact tracing
            elif intervention['type']=="contact_tracing":
                if not exut.validate_items_in_lists(list(intervention.keys()),exdf.interventions['contact_tracing']):
                    print(f"Cannot integrate intervention: {intervention} check for valid keys:\
                          {exdf.interventions['contact_tracing']}")
                    continue       
                exut.assign_intervention_keys(intervention,exdf.interventions['contact_tracing'],exdf.default_contact_tracing_values)
                try:
                    self.interventions[id].append(cv.contact_tracing(
                        trace_probs=intervention['trace_probs'],trace_time=intervention['trace_time'],start_day=intervention['start_day'],
                        end_day=intervention['end_day'],presumptive=intervention['presumptive'],capacity=intervention['capacity'],
                        quar_period=intervention['quar_period'],label=intervention['label']
                    ))
                except Exception as e:
                    print(f"Cannot create intervention: {intervention} due to:{str(e)} check for valid keys and values.")
            # Vaccine probability
            elif intervention['type']=="vaccinate_probability":
                if not exut.validate_items_in_lists(list(intervention.keys()),exdf.interventions['vaccinate_probability']):
                    print(f"Cannot integrate intervention: {intervention} check for valid keys:\
                          {exdf.interventions['vaccinate_probability']}")
                    continue
                elif 'use_waning' not in self.simulation_pars[id] or not self.simulation_pars[id]['use_waning']:                    
                    print(f" You cannot define vaccinate probability, when use_waning set to False")
                    continue
                exut.assign_intervention_keys(intervention,exdf.interventions['vaccinate_probability'],exdf.default_vaccinate_probability_values)
                if isinstance(intervention['vaccine'],str):
                    pass
                elif isinstance(intervention['vaccine'],dict):
                    if not exut.validate_pars(intervention['vaccine'],exdf.vaccine_keys):
                        print(f"Cannot create intervention:{intervention} because there are no valid keys for vaccine. Please define keys:{exdf.vaccine_keys}")
                        continue                    
                else:
                    print(f"Cannot create intervention:{intervention} because vaccine is not validly defined. Vaccine can be a string name from {exdf.default_variants} Please define keys:{exdf.vaccine_keys}")
                    continue   
                try:
                    self.interventions[id].append(cv.vaccinate_prob(
                        vaccine=intervention['vaccine'],days=intervention['days'],prob=intervention['prob'], label=intervention['label'],
                        subtarget=intervention['subtarget'],booster=['booster']
                    ))
                except Exception as e:
                    print(f"Cannot create intervention: {intervention} due to:{str(e)} check for valid keys and values.")
            #Vaccinate num - given distribution
            elif intervention['type']=="vaccinate_distribution":
                if not exut.validate_items_in_lists(list(intervention.keys()),exdf.interventions['vaccinate_distribution']):
                    print(f"Cannot integrate intervention: {intervention} check for valid keys:\
                          {exdf.interventions['vaccinate_distribution']}")
                    continue
                elif 'use_waning' not in self.simulation_pars[id] or not self.simulation_pars[id]['use_waning']:                    
                    print(f" You cannot define vaccinate probability, when use_waning set to False")
                    continue
                exut.assign_intervention_keys(intervention,exdf.interventions['vaccinate_distribution'],exdf.default_vaccinate_probability_values)
                if isinstance(intervention['vaccine'],str):
                    pass
                elif isinstance(intervention['vaccine'],dict):
                    if not exut.validate_pars(intervention['vaccine'],exdf.vaccine_keys):
                        print(f"Cannot create intervention:{intervention} because there are no valid keys for vaccine. Please define keys:{exdf.vaccine_keys}")
                        continue                    
                else:
                    print(f"Cannot create intervention:{intervention} because vaccine is not validly defined. Vaccine can be a string name from {exdf.default_variants} Please define keys:{exdf.vaccine_keys}")
                    continue   
                try:
                    self.interventions[id].append(cv.vaccinate_num(
                        vaccine=intervention['vaccine'],sequence=intervention['sequence'],num_doses=intervention['num_doses'], booster=intervention['booster'],
                        subtarget=intervention['subtarget'],label=intervention['label']
                    ))
                except Exception as e:
                    print(f"Cannot create intervention: {intervention} due to:{str(e)} check for valid keys and values.")
            # Simple vaccine
            # elif intervention['type']=="simple_vaccination":
            #     if not exut.validate_items_in_lists(list(intervention.keys()),exdf.interventions['simple_vaccination']):
            #         print(f"Cannot integrate intervention: {intervention} check for valid keys:\
            #               {exdf.interventions['simple_vaccination']}")
            #         continue
            #     # elif 'use_waning' in self.simulation_pars[id] or self.simulation_pars[id]['use_waning']:                    
            #     #     print(f" You cannot define vaccinate probability, when use_waning set to True")
            #     #     continue              
            #     exut.assign_intervention_keys(intervention,exdf.interventions['simple_vaccination'],exdf.default_simple_vaccination_values)
            #     try:
            #         self.interventions[id].append(cv.simple_vaccine(
            #             days=intervention['days'],prob=intervention['prob'],rel_sus=intervention['rel_sus'], rel_symp=intervention['rel_symp'],
            #             subtarget=intervention['subtarget'],cumulative=intervention['cumulative'],label=intervention['label']
            #         ))
            #     except Exception as e:
            #         print(f"Cannot create intervention: {intervention} due to:{str(e)} check for valid keys and values.")            
            # Place for further intervention types
        return self.interventions
    
    def create_variants(self,id,config=None):
        '''
            id (int): id of simulation (row of variant)
            config(dict): configuration        
        '''
        if config is None:
            config = self.covasim_conf.return_pars('variants')
        if len(config)==0:
            self.variant_list=None
        for variant in config[id]:
            self.variant_list[id].append(cv.variant(
                                    variant=variant[exdf.confkeys['variant']],
                                    label=variant[exdf.confkeys['label']],
                                    days=variant[exdf.confkeys['days']],
                                    n_imports=variant[exdf.confkeys['n_imports']]
            ))
        

    def return_intervention(self,id,interventions_list=None):
        interventions=interventions_list or self.interventions
        if id >= len(interventions):
            return None
        else:
            return interventions[id]
    
    def return_variants(self,id,variant_list=None):
        variants=variant_list or self.variant_list
        if id>=len(variants):
            return None
        else:
            return variants[id]

    #Config can be provided, or it will defaultly load config file for sims
    def create_pars(self,id,config=None):
        '''
            Method for creating pars dictionary based on configuration.
            config=None - config with pars can be given
            id= which sim pars are need to create
        '''
        #for shorther usage
        if config is not None:
            conf=config
        else:
            conf=self.covasim_conf.return_pars('covasim')
        #if config does contains only one global pars
        if len(conf)==1:
            id=0
        pars=dict()
        constructor_pars=dict()
        for key,value in conf[id].items():
            if exut.validate_pars(key,exdf.covasim_pars['sim_pars']) and value is not None: #sim parse are on hard
                pars[key]=value
            elif exut.validate_pars(key,exdf.covasim_pars['sim_constructor']) and value is not None:# Handle pars, which must be set different way     
                # Handle label change if there is global settings
                if not self.covasim_conf.pars_different_bool and key=="label":
                    constructor_pars[key]=f"{value}_reg{id}"
                else:
                    constructor_pars[key]=value
            elif value is None or key=="location_code":
                pass #ignoring par, which has no value          
            else:
                print(f" {key} is not valid key. You can use only:{exdf.covasim_pars}. Ignoring:{key}") 
            # Handle popfile pars if overrided, Set the right location
            if  self.override_pop_location:  #Overriding pop_location if there is full initialization
                constructor_pars['popfile']=str(Path(self.save_settings['location']).joinpath(exdf.save_settings['population_path']).joinpath(self.popfile_file_list[id]))
            else:
                constructor_pars['popfile']=conf[id]['popfile']
        # Handle pop_infected if its missing in conf file, then set to 1 for each sim
        if 'pop_infected' not in pars or pars['pop_infected'] is None:
            pars['pop_infected']=1
        # Handle pop size if its test
        if self.test:
            pars['pop_size']=exdf.test_n_people
            self.population[id]=exdf.test_n_people            
        else:
            pars['pop_size']=self.population[id]
        # Handle pop_size if there is mobility
        if self.mobility is not None and not self.test:
            pars['pop_size']+=int(self.mobility[:,id].sum())
        elif self.mobility is not None and self.test:
            self.mobility[self.mobility>0]=exdf.testsettings['mobility_size']
            pars['pop_size']+=int(exdf.testsettings['mobility_size']*(len(conf)-1))
        # Handle population size if there is a test
        self.constructor_pars.append(constructor_pars)
        self.simulation_pars.append(pars)
        return 

    def create_and_initialize_sims(self):
        '''
        If intervention for separated sim or for each
        '''
        # Prepare pars and interventions
        exut.fill_list(self.interventions,self.number_of_sims)
        exut.fill_list(self.mobility_changes,self.number_of_sims)
        exut.fill_list(self.variant_list,self.number_of_sims)
        # Sort sims by location_code in region pars
        if self.override_pop_location: # Only if there is no provided popfiles by big run
            self.popfile_file_list=exut.sort_sims_by_synthpops_location(conf=self.covasim_conf.return_pars('covasim'),save_settings_location=self.save_settings['location'])
        # Method for sorting synthpops    
        # if self.extension_controller.synthpop_pops:
        #     exut.sort_synthpop_files(loaded_pops=self.extension_controller.synthpop_pops,conf=self.covasim_conf.return_pars('covasim'))
        for id in range(self.number_of_sims):
            self.create_pars(id)
            self.create_interventions(id)
            self.create_variants(id)
        # Choose run based on parallel_run
        if 'parallel_run' in self.run_settings:
            if self.run_settings['parallel_run']:
                self.parallel_sim_creation()
                return
        self.normal_sim_creation()

    def normal_sim_creation(self):
        '''
            This method stands for normal non-parallel creating sims and initializing them
        '''
        for id in range(self.number_of_sims):
            self.sim_creation_process(id)
    
    def parallel_sim_creation(self):
        with mp.Manager() as manager:
            self.sims = manager.list()
            processes=[]
            for i in range(self.number_of_sims):
                p=mp.Process(target=self.sim_creation_process,args=(i,))
                p.start()
                processes.append(p)
            for p in processes:
                p.join()
            self.sims=list(self.sims) # Retype proxylist back to list
    
    def sim_creation_process(self,id):
        '''
            Method for loading configuration for sim / can be used both by parallel or normal run
        '''
        if  'popfile' in self.constructor_pars[id] and self.constructor_pars[id] is not None: # If people are provided
            self.simulation_pars[id]['pop_type']='synthpops'
            if self.save_settings and exdf.confkeys['copy_loaded_pop'] in self.save_settings and self.save_settings[exdf.confkeys['copy_loaded_pop']]:
                exut.copy_files(self.constructor_pars[id]['popfile'],exut.merge_twoPaths(exut.merge_twoPaths(self.save_settings['location'],exdf.save_settings['population_path']),os.path.basename(self.constructor_pars[id]['popfile'])))
            # if self.extension_controller.synthpop_pops:
            #     # Method for sorting synthpops
            #     sp_people=self.extension_controller.synthpop_pops[id]
            #     print(f"Using people from synthpops {id}")
            # else:
            sp_people=sp.Pop.load(self.constructor_pars[id]['popfile']) # Must be absolute path
            print(f"Loading people from:{self.constructor_pars[id]['popfile']}")
            exut.validate_pop_size(self.simulation_pars[id]['pop_size'],sp_people.n)
        else:
            sp_people=None
        sim = cv.Sim(pars=self.simulation_pars[id],
                     interventions=self.return_intervention(id),
                     variants=self.return_variants(id),
                     label=self.constructor_pars[id]['label'],
                     people=sp_people)
        sim.initialize()
        sim._orig_pars=sc.dcp(sim.pars)
        # self.extension_controller.synthpop_pops[id]=None # Free memory
        self.sims.append(sim) 
    

    def run_sim_parallel(self):
        #Timer
        tictoc=TicToc()
        tictoc.tic()
        #Create sims
        self.create_and_initialize_sims()
        #Initial interaction for all sims
        self.sims=exut.sort_sims(self.constructor_pars,self.sims) #Sorting for sims 
        conf=self.covasim_conf.return_pars('covasim')
        if self.mobility is not None and self.population is not None:
            mb.interactions(self.sims,self.mobility,self.population)
        barrier = mp.Barrier(self.number_of_sims)  # Create a barrier for synchronization
        with mp.Manager() as manager:
            self.result_list = manager.list()
            processes = []

            for i in range(self.number_of_sims):
                p = mp.Process(target=self.sim_process, args=(i, self.sims[i], conf[i], barrier))
                p.start()
                processes.append(p)

            for p in processes:
                p.join()
            print("Processes done")

            self.result_list=exut.sort_sims(self.constructor_pars,list(self.result_list))
            self.result = cv.MultiSim(sims=list(self.result_list))
            
        del self.result_list        
        tictoc.toc("Vse hotovo za: ")
        return self.result
    
    def sim_process(self,index,sim,conf,barrier):
        for t in range(sim['n_days'] + 1):
            if ('rand_seed' in conf and int(conf['rand_seed']) > 1) or (
                    'rand_seed' in conf and conf['rand_seed']):
                sim.set_seed()
            sim.step()
            barrier.wait()  # Wait for all processes to reach this point before proceeding
            if self.mobility is not None and self.mobility_changes: # Integrate mobility changes for global or single          
                exclude_mobility_list=[]
                actual_date=datetime.datetime.strptime(sim.date(t),'%Y-%m-%d')
                for i,region_sim in enumerate(self.mobility_changes):
                    for change in region_sim:
                        if (change[0] <= actual_date <= change[1]):
                            if not i in exclude_mobility_list:
                                exclude_mobility_list.append(i)
                if len(exclude_mobility_list) == self.number_of_sims or len(exclude_mobility_list)==0: #if its for all regions, then dont do interactions, of if there is none
                    pass
                elif len(exclude_mobility_list) != self.number_of_sims:
                    for i,index in enumerate(exclude_mobility_list):
                        if i>0: # if one row/col was already deleted + number of been deleted
                            modyfied_mobility=exut.delete_mobility(modyfied_mobility,index-i)
                        else: # If its first appearance of deleting
                            modyfied_mobility=exut.delete_mobility(self.mobility,index)
                    mb.interactions([sim for i,sim in enumerate(self.sims) if i not in exclude_mobility_list],
                                    modyfied_mobility,
                                    [pop for i,pop in enumerate(self.population) if i not in exclude_mobility_list])                                        
            elif self.mobility is not None:
                mb.interactions(self.sims,self.mobility,self.population)
        sim.finalize()
        sim.summarize()
        self.result_list.append(sim)
        return 

    def run_sim_single_core(self):
        #Timer
        tictoc=TicToc()
        tictoc.tic()
        #Create sims
        self.create_and_initialize_sims()
        #Initial interaction for all sims
        self.sims=exut.sort_sims(self.constructor_pars,self.sims) #Sorting for sims 
        conf=self.covasim_conf.return_pars('covasim')
        if self.mobility is not None and self.population is not None:
            mb.interactions(self.sims,self.mobility,self.population)
        for t in range(self.sims[0]['n_days']+1):
            print(f"Running sim for day:{t}")
            for i,sim in enumerate(self.sims): 
                if ('rand_seed' in conf[i] and int(conf[i]['rand_seed']) > 1) or ('rand_seed' in conf and conf['rand_seed']):                    
                    sim.set_seed()
                # Wanning fix
                sim.step()
                                                   
            if self.mobility is not None and self.mobility_changes: # Integrate mobility changes for global or single          
                exclude_mobility_list=[]
                actual_date=datetime.datetime.strptime(sim.date(t),'%Y-%m-%d')
                for i,region_sim in enumerate(self.mobility_changes):
                    for change in region_sim:
                        if (change[0] <= actual_date <= change[1]):
                            if not i in exclude_mobility_list:
                                exclude_mobility_list.append(i)
                if len(exclude_mobility_list) == self.number_of_sims or len(exclude_mobility_list)==0: #if its for all regions, then dont do interactions, of if there is none
                    pass
                elif len(exclude_mobility_list) != self.number_of_sims:
                    for i,index in enumerate(exclude_mobility_list):
                        if i>0: # if one row/col was already deleted + number of been deleted
                            modyfied_mobility=exut.delete_mobility(modyfied_mobility,index-i)
                        else: # If its first appearance of deleting
                            modyfied_mobility=exut.delete_mobility(self.mobility,index)
                    mb.interactions([sim for i,sim in enumerate(self.sims) if i not in exclude_mobility_list],
                                    modyfied_mobility,
                                    [pop for i,pop in enumerate(self.population) if i not in exclude_mobility_list])                                        
            elif self.mobility is not None:
                mb.interactions(self.sims,self.mobility,self.population)
        for sim in self.sims:
            sim.finalize()
            sim.summarize()
        self.result=cv.MultiSim(sims=self.sims)
        tictoc.toc("Vse hotovo za: ")     
        return self.result
    
    def run_simulation(self):
        if 'parallel_run' in self.run_settings and self.run_settings['parallel_run']:
            self.run_sim_parallel()
        else:
            self.run_sim_single_core()