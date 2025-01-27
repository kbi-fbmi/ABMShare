import extensions.defaults as exdf
import extensions.utils as exut
import extensions.report_ex.report_utils as exru
import covasim as cv
import copy
import os

class Report_ex_controller():
    def __init__(self,configuration=None,simulation=None, save_settings:dict=None,save_name:str=None, wait:bool=False):
        '''
            configuration(dict)                                         : OPTIONAL, can be only called with autosave, configuration for report extension.
            simulation (cv.MultiSim)                                    : a multisim object, can be loaded from configuration file, or given. 
                                                                            This Overrides the configuration settings
            save_settings(dict)                                         : speccified save settings from extension caller
            wait (bool)                                                 : boolean just for testing or experimental purposes
        '''
        # Handle configuration file
        if configuration is None:
            pass
        elif not isinstance(configuration,dict):
            configuration=exut.load_config(configuration)
        self.configuration = configuration
        self.save_settings=save_settings
        # Handle simulation object
        if simulation is None and self.save_settings is None:
            simulation = exru.load_sim(self.configuration[exdf.confkeys['input_multisim']]['filepath'])
        elif self.save_settings:
            simulation = exru.load_sim(self.save_settings['sim_location'])
        elif save_name is not None:
            simulation = exru.load_sim(save_name)
        # Handle some pars
        self.simulation = simulation
        self.report_list=[]       
        # Define save_location
        if self.save_settings:
            self.save_location=exut.merge_twoPaths(self.save_settings['location'],exdf.save_settings['output_reports'])
            exut.directory_validator(self.save_location,create_new=True)
        elif "output_path" in self.configuration and self.configuration['output_path'] is not None:
            self.save_location=self.configuration['output_path']
        # Define output format
        try:
            self.output_format= self.configuration['output_format']
        except:
            self.output_format=".csv"
        if not wait:
            self.process()


    def process(self):
        '''
            Core method for creating reports.
        ''' 
        try:       
            conf = self.configuration[exdf.confkeys['input_multisim']] # for shorter usage
            if 'reports' in self.configuration:
                self.parse_reports() # parse every single report
        except ValueError:
            print("No configuration for report module provided")
        # Core processing
        if (self.configuration is not None and (self.save_settings and self.configuration[exdf.confkeys['create_report']])) or self.configuration[exdf.confkeys['create_report']]:
            if conf[exdf.confkeys['whole_simulation']]:
                exru.save_whole(self.simulation,self.save_location,extension=self.output_format)
            if conf[exdf.confkeys['separated_simulation']]:
                self.save_separated(self.save_location)
            if exdf.confkeys['whole_variants'] in conf and conf[exdf.confkeys['whole_variants']]:
                output,variant_names=self.process_multiple_variants(dirpath=self.save_location)
            if exdf.confkeys['separated_variants'] in conf and conf[exdf.confkeys['separated_variants']]:
                self.process_whole_variants(output=output,variant_names=variant_names,dirpath=self.save_location)
        elif self.save_settings: #If there is only self.save_settings
            try:
                exru.save_whole(self.simulation,self.save_location,extension=self.output_format)
                self.save_separated(self.save_location)
                output,variant_names=self.process_multiple_variants(self.save_location)
                self.process_whole_variants(output=output,variant_names=variant_names,dirpath=self.save_location)
            except: 
                print("An error occured while creating reports. While only save settings.")
        else:
            print("Nothing to do here")
        # Parse reports from list for the fullsimulation as well for separated simulations/regions
        if self.report_list:
            for report in self.report_list:
                for sim in self.simulation.sims:            
                    newreport=copy.deepcopy(report)
                    newreport['filename']=f"{sim.label}_{report['filename']}"
                    exru.save_report(report=newreport,sim_results=sim.results,location=self.save_location)


    def parse_reports(self):
        '''
            Method for getting every single report info from configuration file.
        '''
        for i,report in enumerate(self.configuration[exdf.confkeys['reports']]):
            if not exut.validate_pars(report['keys'],exdf.report_keys):
                print(f"This report{report} cannot be processed")
                continue
            if not report['output_format'] and not self.output_format:
                report['output_format']=exdf.report_default_format #default format 
            elif self.output_format:
                report['output_format']=self.output_format
            if not report['filename']:
                report['filename']=f"Unnamed-{i}"
            self.report_list.append({"keys": report['keys'],
                                 "output_format":report['output_format'],
                                 "filename":report['filename']})
    
    def save_separated(self,dirpath,filename=None):
        '''
            Method for saving all the brief (every parameter from simulation). Separately for each region/simulation from the Multisimulation object.
        '''
        if isinstance(self.simulation,cv.MultiSim):
            for sim in self.simulation.sims:
                filename=exut.filename_validator(exut.merge_twoPaths(dirpath,sim.label))
                filename=os.path.basename(filename)
                exut.save_file(dirpath,filename,extension=self.output_format,data=sim.to_df())
                    
    def process_multiple_variants(self, dirpath=None, filename=None):
        output = []  # Initialize output as an empty list or suitable default
        variant_names = []  # Initialize variant_names as empty list or suitable default
        if isinstance(self.simulation, cv.MultiSim):
            for i, sim in enumerate(self.simulation.sims):
                if sim['n_variants'] > 1:
                    dflist, variant_names = exru.create_single_variant_output(simulation=sim, dirpath=dirpath)
                    if i == 0:
                        output = copy.deepcopy(dflist)
                    else:
                        exru.sum_dataframes(output, dflist)
                else:
                    return "", []  # If the loop is executed but the condition is not met, it will return empty values
        return output, variant_names

    def process_whole_variants(self,output,variant_names,dirpath,filename=None):
            exru.save_whole_variant_output(dataframe_list=output,
                                       variant_names=variant_names,
                                       dirpath=dirpath,
                                       filename=filename)
            
