import abmshare.utils as exut
import abmshare.defaults as exdf

import synthpops as sp
import os
from multiprocessing import Pool
from pytictoc import TicToc
import shutil
from distutils.dir_util import copy_tree
import time
import numpy as np

class PopCreator():
    '''
        Class for creating pops based on configuration.
    '''
    def __init__(self,configuration,age_distribution_configuration,popsize_list=None,pop_loation_pars=None,multiprocess=False,wait=False,mobilitydf=None,test=False,save_settings:dict={},override_pop_location:bool=False,**kwargs):
        '''
            configuration (dict or string)          : base synthpops_pop_creation configuration
            age_distribution_configuration (dict)   : configuration for age distribution
            popsize_list (list:int)                 : list of population sizes coresponding to region number
            pop_location_pars (dict)                : dictionary with basic location pars for json files.            
            multiprocess (bool)                     : multiprocess is assigned automatically from configs, but can be also manually
            wait (bool)                             : wait for debugging, otherwise will everything process with created instance of this class
            mobilitydf (pd.dataframe)               : dataframe for extending pop_size
            test (bool)                             : for setting pop_sz to defaults, can be also obtained from configuration file
            save_settings (dict)                    : if provided, use them for saving outputs
            override_pop_location (bool)            : if true, then pop_location_pars will be used for saving pops
            **kwargs:
            pop_name_prefix (string)                : can also be from configuration as same key, or can be missing, adds prefix to output pop filename
            pop_name_suffix (string)                : can also be from configuration as same key, or can be missing, adds suffix to output pop filename
        '''
        # init Loaders
        if not isinstance(configuration,dict):
            configuration=exut.load_config(configuration)        
        if not isinstance(age_distribution_configuration,dict):
            age_distribution_configuration=exut.load_config(age_distribution_configuration)            
        self.configuration=configuration
        self.age_distribution_configuration=age_distribution_configuration
        if popsize_list is None:
            popsize_list=self.create_popsize_list()
        self.popsize_list=popsize_list
        # Pars
        if not 'pop_input_type' in self.configuration:
            self.configuration['pop_input_type']=""
        self.pop_input_type=self.configuration['pop_input_type']
        self.region_settings=[]#maybe
        self.creator_pars=[]
        self.multiprocess=multiprocess
        self.mobilitydf=mobilitydf
        self.save_settings=save_settings
        self.override_pop_location=override_pop_location
        self.pop_list=list()
        if self.mobilitydf is not None: #because of pd.DataFrame
            self.mobility=exut.prepare_mobility(self.mobilitydf)
        else:
            self.mobility = None
        self.test=test
        self.synthpops_data_destination=None
        self.check = 0 # information for deleting configurations
        if kwargs:
            for key,value in kwargs.items():
                setattr(self,key,kwargs[key])
        else:
            self.kwargs=dict()
        if not wait: 
            self.process(self.test)
        
        
    def create_popsize_list(self,filepath=None):
        '''
            Method for creating list of population sizes. 
            filepath (string)                       : filepath to age_distribution file if provided, or load via config path
        '''
        filepath = filepath or self.age_distribution_configuration['filepath']
        df=exut.load_datafile(filepath)
        x = [x for x in df['population']]
        return x   
    
    def save_pop(self,pop:sp.Pop,filename,filedir=None):
        self.check+=1
        if self.save_settings:
            filedir=os.path.join(self.save_settings['location'],exdf.save_settings['population_path'])
        elif not filedir and 'output_pop_filepath' in self.kwargs:
            filedir = self.kwargs['output_pop_filepath']
        else:        
            filedir=self.configuration['output_pop_filepath']
        exut.directory_validator(filedir)
        filepath=os.path.join(filedir,filename)
        if self.pop_input_type == "json": 
            pop.to_json(f"{filepath}.json")
        elif self.pop_input_type =="obj":
            pop.save(f"{filepath}.pop")
        else:
            print("Location for save was not specified, saving as object file")
            pop.save(f"{filepath}.pop")

    def prepare_pars(self,iteration=0,test=False):
        '''
            iteration (int)                         : default for first region as 0
            return pars for pop creating
        '''        
        # First prepare pars defined in configuration
        pars=dict()
        for key,value in self.configuration['pars'].items():
            if key in exdf.synthpops_pars['pop_creator_pars']:                
                pars[key]=value
            else:
                print(f"Key:{key} is not in pars:{exdf.synthpops_pars['pop_creator_pars']}")
        # Secondly define location informations
        for key,value in self.configuration['pops'].items():
            if key in exdf.synthpops_pars['pop_location_pars']:
                if isinstance(value,list): # IF there is a list, provide specific index
                    value=value[iteration]
                
                if key=="state_location":
                    try:
                        name,code=value.split("_")
                        pars['location_code']=code
                        pars['state_location']=value
                    except Exception as e:
                        print("Error in parsing state location code. Make sure it is in format Name_Code like Czechia_CZ01. \nError:",e)
                elif key==exdf.confkeys['region_config_filename']: # Added new key
                    pars['region_config_path']=value
                else:
                    pars[key]=value
            else:
                print(f"Key:{key} is not in pars:{exdf.synthpops_pars['pop_location_pars']}")
        # Handle population size
        if ("test" in self.configuration and self.configuration['test']==True) or test or self.test:
            pars['n']=exdf.testsettings['n_size']
        else:
            pars['n']=self.popsize_list[iteration]
        # Edit population size based on mobility
        if self.mobility is not None:
            if ("test" in self.configuration and self.configuration['test']==True) or test or self.test:
                pars['n']+=int(exdf.testsettings['mobility_size']*(len(self.configuration['pops']['pop_location'])-1))
            else:
                pars['n']+=int(self.mobility[:,iteration].sum())
        # Handle config_dirpath for specific location
        if exdf.confkeys['config_dirpath'] in self.configuration and self.configuration[exdf.confkeys['config_dirpath']]:
            pars[exdf.confkeys['config_dirpath']] = self.configuration[exdf.confkeys['config_dirpath']]
            pars[exdf.confkeys['region_config_path']]=exut.merge_twoPaths(self.configuration[exdf.confkeys['config_dirpath']],pars[exdf.confkeys['region_config_path']])
        elif self.save_settings:
            pars[exdf.confkeys['config_dirpath']] = exut.merge_twoPaths(self.save_settings['location'],exdf.save_settings['population_configurations'])
            pars[exdf.confkeys['region_config_path']]=exut.merge_multiple_paths(self.save_settings['location'],[exdf.save_settings['population_configurations'],pars[exdf.confkeys['region_config_path']]])
        return pars
        

    def generate_filename(self,country_location,state_location,prefix=None,suffix=None):
        '''
            Method for handlind suffixes and preffixes from conf/kwargs value.
            Also change the extension based on mobility.
        '''
        filename=""
        prefix=prefix or ""
        suffix=suffix or ""        
        try:
            prefix=self.pop_name_prefix
        except:
            try:
                prefix=self.configuration['pop_name_prefix']
            except:
                prefix=""
        try:
            suffix=self.pop_name_suffix
        except:
            try:
                suffix=self.configuration['pop_name_suffix']
            except:
                suffix=""
        # Handle test default suffix, prefix
        if self.test:
            suffix=exdf.testsettings['suffix']
            prefix=exdf.testsettings['prefix']
        filename=f"{prefix}{country_location}-{state_location}{suffix}"
        if self.mobility is not None and suffix!="_mob": # Control, if suffix is _mob
            filename=f"{filename}_mob"
        return filename


    def init_and_save(self,index,process_pars): #before pars=processes or look to github
        t=TicToc()
        t.tic()
        if isinstance(process_pars,list):
            pars=process_pars[index]
        elif isinstance(process_pars,dict):
            pars=process_pars
        print(f"\nCreating population:{pars['state_location']}")
        pop=sp.Pop(**pars)
        filename=self.generate_filename(pars['country_location'],pars['state_location'])
        self.save_pop(pop,filename)
        t.toc(f"Region:{pars['state_location']} generated and saved to{filename}")
        if self.multiprocess and self.check==len(self.configuration['pops']):
            self.clear_configuration_files()
        return pop
 
    def process(self,test=False):
        '''
            This method is responsible for creating one population.
            test (bool)                     : just for testing purposes set population to 20k size
            prepare_pars -> copy jsons -> create pop -> save pop
        '''
        process_par_lists=[]
        for i, region in enumerate(self.configuration['pops']['state_location']):
            pars=self.prepare_pars(i,test)
            if self.multiprocess:
                process_par_lists.append(pars)
            else:
                self.init_and_save(i,pars) 
        # For multiprocessing               
        # if processes:
        #     p=Pool(len(processes))
        #     p.map(self.init_and_save,processes)
        if process_par_lists:
            with Pool(processes=len(process_par_lists)) as pool:
                self.pop_list = pool.starmap(self.init_and_save, [(i, process_par_lists) for i in range(len(process_par_lists))])


    def get_pops(self):
        return self.pop_list