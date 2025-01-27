import extensions.defaults as exdf
import extensions.utils as exut
import extensions.synthpops_ex.old_region_config_creator as reg_creator
import extensions.synthpops_ex.old_pop_creator as old_pop_creator

class SynthpopsExtensionController():
    def __init__(self,extension_controller,configuration,pop_creator_conf=None,region_config_creator_conf=None,age_distribution_conf=None,wait=False,mobility_path=None,test=False,save_settings:dict=None,csv_data_dict:dict=None,override_pop_location:bool=False):
        '''
        Initialize instance of Synthpops extension controller which is responsible for creating populations.

            configuration (dict)                    : configuration with informations for run synthpops
            pop_creator_conf (dict)                 : OPTIONAL configuration for pop_creator, if not provided,
                                                      then its loaded from default configuration for synthpops
            region_config_creator_conf (dict)       : OPTIONAL configuration for region_config_creator, if not provided,
                                                      then its loaded from default configuration for synthpops
            age_distribution_conf (dict)            : OPTIONAL configuration for region_config creator for age_distribution,
                                                      if not provided, then loaded from default configuration for synthpops                                                      
            wait (bool)                             : for not parsing automatically with instance creation          
            test (bool)                             : configure test settings by default values
            save_settings(dict)                     : dictionary with specified save_pars for every creates/used files
            csv_data_dict (dict)                    : speccifies dictionary for other csv parameters used in synthopps config creator
            override_pop_location (bool)            : if it should override pop location in configuration file
        '''
        if not isinstance(configuration,dict):
            configuration=exut.load_config(configuration)
        self.configuration=configuration
        self.pop_creator_conf=pop_creator_conf
        self.region_config_creator_conf=region_config_creator_conf
        self.age_distribution_conf=age_distribution_conf
        self.csv_data_dict=csv_data_dict or {}
        self.mobility_path=mobility_path        
        if 'test' in self.configuration:
            test=self.configuration['test']
        self.test=test
        self.save_settings=save_settings or {}
        self.override_pop_location=override_pop_location
        self.extension_controller=extension_controller
        # Assign subconfigs from cofniguration file, if separately not provided
        if self.pop_creator_conf is None:
            self.pop_creator_conf=self.configuration[exdf.confkeys['pop_creator_config']]
        if self.region_config_creator_conf is None:
            self.region_config_creator_conf=self.configuration[exdf.confkeys['region_config']]        
        if self.age_distribution_conf is None:
            self.age_distribution_conf=self.configuration['population_age_distributions']
        # For csv files with data for config creation     
        for key in exdf.synthpops_csv_files:
            if key in self.configuration and self.configuration[key]['value']:
                self.csv_data_dict[key]={}
                try:
                    for key2 in self.configuration[key]:
                        if key2==exdf.confkeys['filepath']:
                            self.csv_data_dict[key]['data']=exut.load_datafile(self.configuration[key]['filepath'])
                            continue
                        self.csv_data_dict[key][key2]=self.configuration[key][key2]                                                
                except:
                    self.csv_data_dict[key]['data']=exut.load_datafile(exut.merge_filepathSP(f"{exdf.pathvalues['default_synthpops_region_creator_datafiles']}/{key}.csv"))

        if not wait:
            self.parser()

    def parser(self):
        '''
            Core function for parsing synthpops configuration
        '''
        if self.configuration['create_jsons']:
            reg_creator.RegionConfigCreator(self.region_config_creator_conf,age_distribution_configuration=self.age_distribution_conf,save_settings=self.save_settings,csv_data_dict=self.csv_data_dict)

        if self.configuration['create_pop']:
            if self.mobility_path:
                mobility=exut.load_datafile(self.mobility_path)
            elif self.configuration['mobility_include'] and self.configuration['mobility_path']:
                mobility=exut.load_datafile(self.configuration['mobility_path'])
            else:
                mobility=None            
            if self.configuration['parallel_run']:
                pop_c=old_pop_creator.PopCreator(
                configuration=self.pop_creator_conf,age_distribution_configuration=self.age_distribution_conf,
                full_configuration=self.configuration,mobilitydf=mobility,multiprocess=True,
                save_settings=self.save_settings,override_pop_location=self.override_pop_location,test=self.test)
                # self.extension_controller.synthpop_pops=pop_c.get_pops()
                del pop_c
            else:
                pop_c=old_pop_creator.PopCreator(
                configuration=self.pop_creator_conf, age_distribution_configuration=self.age_distribution_conf,
                full_configuration=self.configuration,mobilitydf=mobility,
                save_settings=self.save_settings,override_pop_location=self.override_pop_location,test=self.test)
                # self.extension_controller.synthpop_pops=pop_c.get_pops()
                del pop_c
        ''' 
            def fce pro ploting, saving data?            
        '''