import os
import sys

import abmshare.covasim_ex.immunity_process as exim
from abmshare import defaults as exdf
from abmshare import utils as exut
from abmshare.covasim_ex import simulation_controller as simproc
from abmshare.grid_compute_ex import grid_compute_controller as gridproc
from abmshare.report_ex import report_ex_controller as repproc
from abmshare.synthpops_ex import synthpops_controller as syntproc
from abmshare.validator import validator as val

# Check for the parameters file.

class ExtensionController():
    def __init__(self,configuration,synthpops_configuration=None,simulation_configuration=None,
                 report_configuration=None,grid_compute:bool=False,grid_user:str=None,validate=None,test=False):
        """Configuration (dict)                    : configuration with informations for run synthpops
        synthpops_configuration (dict)          : OPTIONAl, defaultly loaded from main configuration
        covasim_configuration (dict)            : OPTIONAl, defaultly loaded from main configuration
        report_configuration (dict)             : OPTIONAl, defaultly loaded from main configuration
        grid_compute (bool)                     : if it should prepare default grid compute environment and values, or pass
        test (bool)                             : if it should prepare default test environment and values
        validate (bool:None)                    : True - it will only validate input files, None / it will validate and run, False, it Will not validate at all
        grid_user(str)                          : name of user for proper path while grid computing
        """
        if not isinstance(configuration,dict):
            self.conf_path=configuration
            configuration=exut.load_config(configuration)
        self.configuration=configuration
        self.test=test
        self.save_settings={}
        self.synthpop_pops=list() # list of pregenerated populations
        self.override_save_settings=False
        self.grid_compute=grid_compute
        self.grid_user=grid_user
        self.initialized_modules=exdf.modules
        self.log_file=None
        self.validate=validate
        self.mobility=None

        if not synthpops_configuration:
            synthpops_configuration = self.configuration.get("synthpops_settings", None)
        self.synthpops_configuration = synthpops_configuration

        if not simulation_configuration:
            simulation_configuration = self.configuration.get("simulation_settings", None)
        self.simulation_configuration = simulation_configuration

        if not report_configuration:
            report_configuration = self.configuration.get("report_settings", None)
        self.report_configuration = report_configuration

        #Handle test manually
        try:
            # self.test = self.simulation_configuration.get('test', self.test)
            if self.test:
                pass
            else:
                self.test =self.configuration["initialize"].get("test", self.test)
        except Exception:
            self.test=False

        #Handle save options
    def start(self):
        try:
            if exdf.confkeys["auto_save_settings"] in self.configuration and self.validate!=True:
                self.save_settings=self.load_save_settings_parse()
                self.save_configuration()
        except Exception:
            raise NotImplementedError("You need to provide save_settings, for simulation running.")

        if self.grid_compute and self.grid_user:
            if self.validate: # If validate only
                val.process(self.configuration,self.simulation_configuration["filepath"],self.synthpops_configuration["filepath"],self.report_configuration["filepath"])
                print("Validation process has been finished")
                return
            if self.validate==None:
                val.process(self.configuration,self.simulation_configuration["filepath"],self.synthpops_configuration["filepath"],self.report_configuration["filepath"])
            gridproc.GridComputeController(config=self.configuration,base_conf_path=self.conf_path,grid_user=self.grid_user)
            # Changing the value of grid_compute processed to True is by the grid_change_paths script
            return


        # Handle validation, for locall run
        if self.validate: # If validate only
            val.process(self.configuration,self.simulation_configuration["filepath"],self.synthpops_configuration["filepath"],self.report_configuration["filepath"])
            print("Validation process has been finished")
            return
        if self.validate==None:
            val.process(self.configuration,self.simulation_configuration["filepath"],self.synthpops_configuration["filepath"],self.report_configuration["filepath"])

        #Check for possible override_load+and_save settings
        self.check_override()
        # Create logging file
        try:
            file_path=exut.find_directory(os.environ.get("SCRATCHDIR"),"output_data")
            filepath=exut.get_logging_file(file_path)
            self.log_file=open(filepath, "w")
            sys.stdout = self.log_file
        except Exception:
            pass
        if self.configuration["initialize"]["synthpop_initialize"]:
            self.initialized_modules["synthpops"]=True
            if self.mobility==None:
                self.mobility=exut.get_nested_value_from_dict(exut.load_config(self.synthpops_configuration["filepath"]),exdf.synthpops_mobility_bool) if not None else False
            print("*******************************************")
            print("Running pop creation process")
            syntproc.SynthpopsExtensionController(configuration=self.synthpops_configuration["filepath"],save_settings=self.save_settings,test=self.test,mobility=self.mobility)
        if self.configuration["initialize"]["simulation_initialize"]:
            if self.mobility==None:
                self.mobility=exut.get_nested_value_from_dict(exut.load_config(self.synthpops_configuration["filepath"]),exdf.synthpops_mobility_bool) if not None else False
            self.initialized_modules["multisim"]=True
            print("*******************************************")
            print("Running multisim simulation process")
            # immunity
            try:
                temp=exut.load_config(self.simulation_configuration["filepath"])
                if temp.get("immunity",False) and temp["immunity"].get("filepath",False):
                    self.immunity_process=exim.ImmunityProcessing(self.simulation_configuration["filepath"])
            except Exception:
                print("Immunity process could not be initialized.")
                pass
            simproc.SimulationExtensionController(configuration=self.simulation_configuration["filepath"],save_settings=self.save_settings,
                                                  override_pop_location=self.override_save_settings,test=self.test,mobility=self.mobility)
        try:
            if self.configuration["initialize"]["report_module_initialize"]:
                self.initialized_modules["report"]=True
                print("*******************************************")
                print("Running reporting module")
                repproc.Report_ex_controller(configuration=self.report_configuration["filepath"],save_settings=self.save_settings)
        except Exception as e:
            print("Reporting process could not be finished.")
            print(e)
        # Close logging file
        if self.log_file:
            try:
                self.file.close()
            except Exception:
                print ("Could not close the logging file")

    def load_save_settings_parse(self,configuration:dict=None):
        """Method for returning save settings pars, if provided
        First it looks for name, if there is a name
        """
        configuration=configuration or self.configuration["auto_save_settings"]
        settings = configuration.copy()
        if "location" not in settings or not settings["location"]:
            # If there is no provided location, look for default
            settings["location"] = str(exut.merge_default_path(exdf.pathvalues["output_path"]))
        if settings["dirname"]:
            path = exut.name_generator(basepath=settings["location"], output_dirname=settings["dirname"])
        else:
            path = exut.name_generator(basepath=settings["location"])
        settings["location"] = path
        if exdf.confkeys["copy_files"] in settings and (exdf.confkeys["grid_compute"] in self.configuration and not self.configuration[exdf.confkeys["grid_compute"]]["value"]):
            if exdf.confkeys["copy_loaded_pop"] in settings[exdf.confkeys["copy_files"]] and settings[exdf.confkeys["copy_files"]][exdf.confkeys["copy_loaded_pop"]] and not self.configuration["initialize"]["synthpop_initialize"]:
                settings[exdf.confkeys["copy_loaded_pop"]]=True
                exut.directory_validator(exut.merge_twoPaths(settings["location"],exdf.save_settings["population_path"]),True)
        return settings

    def save_configuration(self):
        """Simple method for saving initial configurations
        """
        location=os.path.join(self.save_settings["location"],"Configuration")
        exut.directory_validator(location)
        try:
            exut.save_file(location,"MainConfiguration",".json",self.configuration)
        except Exception:
            pass
        try:
            exut.save_file(location,"SimulationConfiguration",".json",exut.load_config(self.simulation_configuration["filepath"]))
        except Exception:
            pass
        try:
            exut.save_file(location,"SynthpopsConfiguration",".json",exut.load_config(self.synthpops_configuration["filepath"]))
        except Exception:
            pass
        try:
            exut.save_file(location,"ReportModuleConfiguration",".json",exut.load_config(self.report_configuration["filepath"]))
        except Exception:
            pass

    def check_override(self):
        if self.configuration["initialize"]["synthpop_initialize"] and self.configuration["initialize"]["simulation_initialize"]:
            self.override_save_settings=True
        return
