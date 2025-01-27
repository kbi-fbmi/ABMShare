import extensions.utils as exut
import extensions.defaults as exdf
import extensions.synthpops_ex.synthpops_conf_getter as spcg
from extensions.synthpops_ex.region import Region
import extensions.extension_controller as extc
import multiprocessing as mp

class RegionConfigCreator:
    def __init__(self,configuration:dict|str,
                 parent_configuration:dict|str=None,                 
                 wait:bool=False,
                 save_settings:dict=None,
                 test:bool=False,
                 mobility:bool=None
                 ):
        """_summary_

        Args:
            configuration (dict): main configuration
            parent_configuration (dict, optional): there can be preloaded configuration with some pars. Can be loaded from main conf
            wait (bool, optional): if wait is true, then its manually needed to call process function
            save_settings (dict, optional): (OPTIONAL) if provided, then its changed output filepath
        """
        # Some pars
        if isinstance(configuration,str):
            configuration=exut.load_config(configuration)
        if isinstance(parent_configuration,str):
            parent_configuration=exut.load_config(parent_configuration)
        self.configuration=configuration
        self.parent_configuration=parent_configuration
        self.test=test
        self.wait=wait
        self.save_settings=save_settings or {}
        self.regions={}
        # Other parameters
        self.num_of_regions=None        
        # Creator parameters
        self.multiprocess=self.configuration.get(exdf.confkeys['multiprocess'],False)
        self.mobility=mobility

        if exut.get_nested_value_from_dict(dictionary=self.configuration,keys=exdf.synthpops_mobility_confkeys+['value']) and self.mobility==None or self.mobility==True: 
            self.mobility_dict=exut.prepare_mobility(exut.load_datafile(spcg.get_mobility_filepath(self.configuration)))
        else:
            self.mobility_dict=False     
        # Check and assign/empty configuration structure
        self.empty_configuration=exut.load_config(exut.merge_file_path("synthpops_ex/data/empty_region.json"))        
        if not wait:
            self.process()
        
    def preparation_region_pop_creator(self):
        for region in spcg.get_all_regions(self.configuration):
            # First add popsize and mobility
            if self.test and isinstance(self.mobility_dict,bool):
                self.regions[region].add_pop_size(exdf.testsettings['n_size'])
            elif self.test and self.mobility_dict:
                self.regions[region].add_pop_size(exdf.testsettings['n_size']+(int(exdf.testsettings['mobility_size']*(self.num_of_regions-1))))     
            elif isinstance(self.mobility_dict,bool):
                self.regions[region].add_pop_size(spcg.get_popsize(self.configuration,location_code=self.regions[region].location_code,
                                                               age_distribution_filepath=self.regions[region].data_files[exdf.synthpops_input_files['population_age_distributions']]))
            else:                
                self.regions[region].add_pop_size(spcg.get_popsize(self.configuration,location_code=self.regions[region].location_code,
                                                               age_distribution_filepath=self.regions[region].data_files[exdf.synthpops_input_files['population_age_distributions']])
                                                               +int(exut.get_mobility_num(self.mobility_dict,self.regions[region].location_code,all_location_codes=self.regions.keys())))        
            # Pars
            for key,value in exdf.synthpops_creator_pars_mapped.items():
                if key in self.regions[region].__dict__:
                    self.regions[region].add_pop_creator_par(key=value,value=key)


    def create_population_objects_multiprocess(self,location_key:str):
        self.regions[location_key].create_population_object()

    def create_population_objects(self):
        if self.multiprocess:
            processes=[]
            for key in self.regions.keys():
                p=mp.Process(target=self.create_population_objects_multiprocess,args=(key,))
                p.start()
                processes.append(p)
            for p in processes:
                p.join()
        else:
            for key in self.regions.keys():
                self.regions[key].create_population_object()

        

    def preparation_region_config(self):
        # Look for csv files, otherwise regions
        for region in spcg.get_all_regions(self.configuration):
            self.regions[region]=""
        self.num_of_regions=len(self.regions) 

    def process(self):
        # Region config creation
        self.region_config_creator(test=self.test)
        # Population object creation
        self.preparation_region_pop_creator()
        self.create_population_objects() 
        print()

    def region_config_creator(self,test:bool=False):
        self.preparation_region_config()        
        creator_data=exut.load_datafile(exut.get_nested_value_from_dict(dictionary=self.configuration,
                            keys=exdf.synthpops_creator_confkeys).get(exdf.confkeys['filepath'], None))
        for key,value in self.regions.items():
            id=exut.get_index_by_column_and_value(df=creator_data,column=exdf.synthpops_region_csv_columns['location_code'],value=key)
            self.regions[key]=Region(location_code=creator_data[exdf.synthpops_region_csv_columns['location_code']][id],
                                     region_name=creator_data[exdf.synthpops_region_csv_columns['region_name']][id],
                                     untrimmed_name=creator_data[exdf.synthpops_region_csv_columns['untrimmed_name']][id],
                                     sheet_name=creator_data[exdf.synthpops_region_csv_columns['sheet_name']][id],
                                     pars=spcg.get_synthpops_parameters(self.configuration,location_code=creator_data[exdf.synthpops_region_csv_columns['location_code']][id]
                                                                        ,region_parent_name=creator_data[exdf.synthpops_region_csv_columns['region_parent_name']][id]),
                                     notes=creator_data[exdf.synthpops_region_csv_columns['notes']][id],
                                     region_parent_name=creator_data[exdf.synthpops_region_csv_columns['region_parent_name']][id],
                                     parent_config=spcg.get_parent_location(config=self.configuration,code=creator_data[exdf.synthpops_region_csv_columns['location_code']][id]),
                                     save_settings=self.save_settings     
                                     )
            self.regions[key].add_datafiles(datafiles=spcg.get_region_specific_csv_files(config=self.configuration,location_code=creator_data[exdf.synthpops_region_csv_columns['location_code']][id],mapped_output=True))
            self.regions[key].add_naming_object(naming_object=exut.get_nested_value_from_dict(dictionary=self.configuration,keys=exdf.synthpops_naming_confkeys))
            self.regions[key].process_region_creation(test=test)



    def return_regions(self):
        return self.regions
    








# #Testing
# if __name__=="__main__":
#     config="/storage/ssd2/sharesim/share-covasim/Tests/new_confs/synthpops.json"
#     save_settings={
#         "value":True,
#         "auto_increment":True,
#         "dirname":"NoTestValues",
#         "location":"/storage/ssd2/sharesim/share-covasim/Outputs"
#     }
#     def load_save_settings_parse(configuration:dict=None):
#         '''
#             Method for returning save settings pars, if provided
#             First it looks for name, if there is a name
#         '''
#         configuration=configuration
#         settings = configuration.copy()
#         if not 'location' in settings or not settings['location']:
#             # If there is no provided location, look for default
#             settings['location'] = str(exut.merge_default_path(exdf.pathvalues['output_path']))
#         if settings['dirname']:
#             path = exut.name_generator(basepath=settings['location'], output_dirname=settings['dirname'])
#         else:
#             path = exut.name_generator(basepath=settings['location'])
#         settings['location'] = path
#         if exdf.confkeys['copy_files'] in settings and (exdf.confkeys['grid_compute'] in configuration and not configuration[exdf.confkeys['grid_compute']]['value']):
#             if exdf.confkeys['copy_loaded_pop'] in settings[exdf.confkeys['copy_files']] and settings[exdf.confkeys['copy_files']][exdf.confkeys['copy_loaded_pop']] and not configuration['initialize']['synthpop_initialize']:
#                 settings[exdf.confkeys['copy_loaded_pop']]=True
#                 exut.directory_validator(exut.merge_twoPaths(settings['location'],exdf.save_settings['population_path']),True)
#         return settings
#     save_settings=load_save_settings_parse(configuration=save_settings)
#     test=RegionConfigCreator(configuration=exut.merge_file_path(config),save_settings=save_settings,test=True)
#     print()

