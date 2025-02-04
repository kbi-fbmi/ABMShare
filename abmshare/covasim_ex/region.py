# Core function for initializiing everything from configuration file
from abmshare.covasim_ex.intervention_process import MobilityIntervention
import abmshare.defaults as exdf
import abmshare.utils as exut
import os
import covasim as cv
import pandas as pd
import numpy as np
import synthpops as sp
import sciris as sc
from pathlib import Path

class Region:
    def __init__(self,
                 location_code:str,
                 name:str,
                 population_size:int, # Also adds mobility, if is given
                 mobility_data:dict=None,
                 mobility_incoming_data:dict=None,
                 intervention_list:list=None,
                 region_pars:dict=None,
                 variant_list:list=None, 
                 save_settings:dict=None,
                 wait:bool=False,
                 test:bool=False,
                 override_pop_location:bool=False):
        """_summary_

        Args:
            location_code (str): _description_
            name (str): _description_
            population_size (int): _description_
            ifisgivenmobility_data (dict, optional): _description_. Defaults to None.
            intervention_list (list, optional): _description_. Defaults to None.
            region_pars (dict, optional): _description_. Defaults to None.
            variant_list (list, optional): _description_. Defaults to None.
        """

        self.location_code=location_code
        self.name=name
        self.population_size=population_size
        self.mobility_data=mobility_data # From this region to others
        self.mobility_incoming_data=mobility_incoming_data # To this region from others
        self.intervention_list=intervention_list
        self.region_pars=region_pars
        self.variant_list=variant_list
        self.save_settings=save_settings
        self.test=test
        self.override_pop_location=override_pop_location
        # Aditional pars
        if self.mobility_incoming_data:
            self.original_population_size=population_size-sum([v for k,v in self.mobility_incoming_data.items() if v is not None and not pd.isna(v)]) # Without added mobility
        else:
            self.original_population_size=population_size
        self.simulation_pars={}
        self.constructor_pars={}
        self.mobility_intervention_list=[]
        self.unique_mobility_indexes={}
        self.cv_simulation=None
        # Process
        if not wait:
            self.process()

    def process(self):
        # Core processing class
        self.filter_simulation_pars()
        self.filter_mobility_interventions()
        if self.test: # Override population size
            self.override_test()
        self.create_simulation()


    def filter_simulation_pars(self):
        """ Filter incoming parameters to constructor and simulation specific pars. (For covasim simulation creation)
        """
        # Filter only those pars, which can be used in simulation
        for key, value in self.region_pars.items():
            if key in exdf.covasim_constructor_pars_mapping.keys():
                self.constructor_pars[exdf.covasim_constructor_pars_mapping[key]]=value
            elif key in exdf.covasim_pars_all and not key in exdf.covasim_exclude_simulation_pars:
                self.simulation_pars[key]=value            
            elif key in exdf.covasim_exclude_simulation_pars: # Only for key use
                continue
            else:
                print(f"Cannot use key {key} in region {self.name} for simulation. Please use only this keys: {exdf.covasim_pars_all}")
        # Filter pop_type
        if self.region_pars.get('popfile',None) and not pd.isna(self.region_pars.get('popfile',None)):
            self.simulation_pars['pop_type']='synthpops'
        elif not (self.region_pars.get('pop_type',None)) and (pd.isna(self.region_pars.get('popfile'))):
            self.simulation_pars['pop_type']='hybrid'
        # Check for pop override_settings
        if self.override_pop_location and exut.is_none_or_empty(self.constructor_pars['popfile']):
            for file in exut.merge_twoPaths(self.save_settings.get('location',None),exdf.save_settings['population_path']):
                if self.location_code.lower() in file.lower():
                    self.constructor_pars['popfile']=file
                    break
        # Add population size
        self.simulation_pars['pop_size']=self.population_size
        
    def filter_mobility_interventions(self):
        """ Filter mobility interventions and add them to separate intervention list        
        """
        ids_to_remove=[]
        for i,intervention in enumerate(self.intervention_list):
            if type(intervention)==MobilityIntervention:
                self.mobility_intervention_list.append(exut.deepcopy_object(intervention))
                ids_to_remove.append(i)
        ids_to_remove.sort(reverse=True)
        for id in ids_to_remove: del self.intervention_list[id]
                

    def create_simulation(self):
        try:
            self.cv_simulation=cv.Sim(pars=self.simulation_pars,
                                interventions=self.intervention_list,
                                variants=self.variant_list,
                                label=self.constructor_pars.get('label',None),
                                people=(
                        (sp.Pop.load(self.constructor_pars.get('popfile'), self.population_size) if not pd.isna(self.constructor_pars.get('popfile')) else None)))
                        #         people=(
                        # (sp.Pop.load(self.constructor_pars.get('popfile'), self.population_size) or {}).get('to_people', lambda: None)()
                        # if not pd.isna(self.constructor_pars.get('popfile')) else None))
        except Exception as e:
            print(f"Cannot create simulation for region {self.name} with error {e}")
    
    def initialize_simulation(self):
        """ Initialize simulation and set some default parameters
        """
        self.cv_simulation.initialize(verbose=0.1)
        self.cv_simulation._orig_pars=sc.dcp(self.cv_simulation.pars)
        self.cv_simulation.set_seed(self.cv_simulation.pars.get('rand_seed',-1)) # Like default covasim
        return self.cv_simulation
        
    def finalize_simulation(self):
        self.cv_simulation.finalize() # Test -1 and maybe change in future
        self.cv_simulation.summarize()

    def override_population_type(self):
        self.simulation_pars['pop_type']='hybrid'
        return None

    def override_test(self):
        """If test simulation is called then maintain population and mobility size
        """
        mobility_increment=0
        if self.mobility_data:
            for key,val in self.mobility_data.items():
                self.mobility_incoming_data[key]=exdf.testsettings['mobility_size'] if not pd.isna(self.mobility_data[key]) else np.nan
                self.mobility_data[key]=exdf.testsettings['mobility_size'] if not pd.isna(self.mobility_data[key]) else np.nan
                mobility_increment+=self.mobility_data[key] if not pd.isna(self.mobility_data[key]) else 0                
        self.simulation_pars['pop_size']=exdf.testsettings['n_size']+mobility_increment
        self.original_population_size=exdf.testsettings['n_size']
        self.population_size=self.simulation_pars['pop_size'] # for shorter further usage

    def get_days(self):
        return self.cv_simulation['n_days']


    def run_step(self):
        if self.cv_simulation.initialized:
            self.cv_simulation.step()            
        else:
            print(f"You cannot run simulation {self.name} because it is not initialized. Please initialize it first.")

    def set_unique_mobility_indexes(self,data:dict):
        """ Set unique people to simulation
        """
        self.unique_mobility_indexes=data