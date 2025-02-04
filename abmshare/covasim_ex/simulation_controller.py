import abmshare.defaults as exdf
import abmshare.utils as exut
import abmshare.covasim_ex.simulation_creator as sim_creator

class SimulationExtensionController():
    def __init__(self,configuration,wait=False,test=False,save_settings:dict=None,parallel_run:bool=True,override_pop_location:bool=False,mobility:bool=None):
        '''
        Initialize instance of Synthpops extension controller which is responsible for creating populations.

            configuration (dict)                    : configuration with informations for run synthpops                                                     
            wait (bool)                             : for not parsing automatically with instance creation          
            test (bool)                             : configure test settings by default values
            save_settings(dict)                     : dictionary with specified save_pars for every creates/used files
            override_pop_location (bool)            : if it should override pop location in configuration file
        '''
        if not isinstance(configuration,dict):
            configuration=exut.load_config(configuration)
        self.configuration=configuration   
        if test: self.test=test
        else: self.test=self.configuration.get("test",False)  
        self.save_settings=save_settings or {}
        self.parallel_run=self.configuration.get("parallel_run",False) 
        self.override_pop_location=override_pop_location
        self.mobility=mobility
        if not wait:
            self.parser()

    def parser(self):
        '''
            Core function for parsing synthpops configuration
        '''
        sim_creator.Simulation_creator(configuration=self.configuration,save_settings=self.save_settings,test=self.test,
                                       parallel_run=self.parallel_run,override_pop_location=self.override_pop_location,mobility=self.mobility)