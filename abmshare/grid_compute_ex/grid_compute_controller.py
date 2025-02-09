import abmshare.utils as exut
import abmshare.defaults as exdf
import abmshare.synthpops_ex.synthpops_conf_getter as spcg
import abmshare.covasim_ex.simulation_conf_getter as simcg
import abmshare.grid_compute_ex.grid_utils as grut
import os

class CopyConfigsInfo():
    def __init__(self):
        self.SYNTHPOP=False
        self.SIMULATION=False
        self.REPORT=False

class GridComputeSettings:
    _allowed_caller = "GridComputeController"
    
    def __init__(self,key_path:str=None,conf_path:str=None):
        if not grut.check_files():
            print("First you need to generate key and conf file for grid computing")
            raise Exception("Key or conf file not found")
        self.__key=grut.load_key(key_path)
        self.__conf=grut.load_conf_to_dict(path=conf_path,key=self.__key) # decrypted data
    
    def get_user_name(self):
        return self.__conf[exdf.grid_confkeys['username']]
    
    def get_server_name(self):
        return self.__conf[exdf.grid_confkeys['server']]
    
    def get_server_input_path(self):
        return self.__conf[exdf.grid_confkeys['input_path_server']]
    
    def get_server_output_path(self):
        return self.__conf[exdf.grid_confkeys['output_path_server']]
    
    def get_server_kerberos_name(self):
        return self.__conf[exdf.grid_confkeys['kerberos_user']]
    
    def get_server_script_path(self):
        return self.__conf[exdf.grid_confkeys['remote_script_path']]

    @classmethod
    def create_instance(cls,caller):
        if not isinstance(caller,globals()[cls._allowed_caller]):
            raise Exception(f"Class {cls.__name__} can be created only from {cls._allowed_caller.__name__}")
        return cls()

class GridComputeController:
    def __init__(self,config:str|dict,base_conf_path:str=None,grid_user:str=None,wait:bool=False,test:bool=False):
        """Controller for grid compute sending jobs to cluster

        Args:
            config (str/dict): config dictionary or path for loading config
        """        
        self.config_info=CopyConfigsInfo()
        self.config_input=base_conf_path
        self.config=exut.load_config_dict(config)
        self.to_copy_files={"mainconfig":None,"synthpops":None,"simulation":None,"report":None,"pops":None,"input_data":None,"synthpops_input_data":None,
                            "simulation_configuration_files":None,"synthpops_configuration_files":None,"simulation_immunity_files":None} 
        #mainconfig, synthpops and simulation goes into input_data, data goes into input_data/data
        self.grid_user=grid_user # For knowing which user is sending the job
        self.path=None # Path for the main folder, which contains all the input/output data
        self.grid_settings=GridComputeSettings.create_instance(self)
        self.test=test
        self.queue_append_string=None
        if not wait:
            self.process()

    def process(self):
        self.process_configs() # Prepare configs
        self.process_data() # Prepare data
        self.process_local_copy() # Copy all localy
        self.process_remote_copy() # Copy to remote server
        self.process_qsub() # Create qsub command

        
    def process_configs(self):
        conf=self.config #for shorter usage
        # Initialize for synthpops
        if conf[exdf.confkeys['initialize']].get(exdf.confkeys['synthpop_initialize'],False):
            self.to_copy_files['synthpops']=conf[exdf.confkeys['synthpops_settings']][exdf.confkeys['filepath']]
            self.config_info.SYNTHPOP=True
        # Initialize for simulation
        if conf[exdf.confkeys['initialize']].get(exdf.confkeys['simulation_initialize'],False):
            self.to_copy_files['simulation']=conf[exdf.confkeys['simulation_settings']][exdf.confkeys['filepath']]
            self.config_info.SIMULATION=True
        # Initialize for reporting
        if conf[exdf.confkeys['initialize']].get(exdf.confkeys['report_module_initialize'],False):
            self.to_copy_files['report']=conf[exdf.confkeys['report_settings']][exdf.confkeys['filepath']]
            self.config_info.REPORT=True
        # Base Share-Sim configuration
        if isinstance(self.config_input,str): 
            self.to_copy_files['mainconfig']=self.config_input

    def process_data(self):
        """Class for processing
        """
        # If synthpops - copy synthpops data
        if self.config_info.SYNTHPOP:
            self.get_synthpops_data()
        # If not synthpops and popfiles provided, copy only popfiles
        elif not self.config_info.SYNTHPOP and self.config_info.SIMULATION:
            self.to_copy_files['pops']=simcg.get_popfiles(self.to_copy_files['simulation'])
        # If covasim - copy covasim data
        if self.config_info.SIMULATION:
            self.get_covasim_data()
    
    def get_synthpops_data(self,config:str|dict=None):
        conf=config or self.to_copy_files['synthpops']
        self.to_copy_files['input_data']=self.to_copy_files['input_data'] or []
        # Parent json
        if isinstance(spcg.get_parent_location(config=conf),list):
            self.to_copy_files['input_data']+=spcg.get_parent_location(config=conf)
        else: 
            self.to_copy_files['input_data'].append(spcg.get_parent_location(config=conf)) if spcg.get_parent_location(config=conf) is not None else None
        # Mobility file
        self.to_copy_files['input_data'].append(spcg.get_mobility_filepath(config=conf)) if spcg.get_mobility_filepath(config=conf) is not None else None                
        # Check for xlsx/csv file
        self.to_copy_files['synthpops_configuration_files']=spcg.get_all_synthpops_csv_files(config=conf)
        # Check for global input data
        self.to_copy_files['synthpops_input_data']=spcg.get_all_data_based_on_input_csv(config=conf)

    def get_covasim_data(self,config:str|dict=None):
        conf=config or self.to_copy_files['simulation']
        self.to_copy_files['input_data']=self.to_copy_files['input_data'] or []
        # Mobility file (note: must be the same as for synthpop loaded populations)
        self.to_copy_files['input_data'].append(simcg.get_mobility_filepath(config=conf)) if simcg.get_mobility_filepath(config=conf) is not None else None
        # Pop location file (age distribution)
        self.to_copy_files['input_data'].append(simcg.get_population_filepath(config=conf)) if simcg.get_population_filepath(config=conf) is not None else None
        # Get new csv files for simulation
        self.to_copy_files['simulation_configuration_files']=simcg.get_all_csv_files(config=conf)
        # Get immunity csv files for simulation
        self.to_copy_files['simulation_immunity_files']=simcg.get_immunity_files(config=conf)

    def process_local_copy(self):
        # Copy to given structure at user (accessible now by self.grid_user) sandbox input folder (new structure)
        path=exdf.base_local_input_path(self.grid_user)
        path_with_dir=exut.name_generator(path,exdf.base_simulation_name)
        # Create folder structure
        folder_structure=exdf.input_folder_structure
        # Prepare files to structure
        for key, value in self.to_copy_files.items():
            # First add config files
            if key in exdf.config_list:
                folder_structure[exdf.confkeys['input_data']][exdf.confkeys['original_confs']].append(value) #NOTE: Now it is in original_conf folder
            # Look for input_datas
            if key == exdf.confkeys['input_data'] and value is not None:
                if isinstance(value,list):
                    for file in value:
                        folder_structure[exdf.confkeys['input_data']][exdf.confkeys['data']].append(file)
                else:
                    folder_structure[exdf.confkeys['input_data']][exdf.confkeys['input_data']].append(value)
            # Look for pops
            if key == exdf.confkeys['pops'] and value is not None:
                for file in value:
                    folder_structure[exdf.confkeys['output_data']][exdf.base_simulation_name][exdf.confkeys['pops']].append(file)
            if key=="synthpops_input_data" and self.to_copy_files.get(key,False):                
                for file in value:
                    folder_structure[exdf.confkeys['input_data']][exdf.confkeys['synthpops_input_data']].append(file)
            if key=="simulation_configuration_files" and self.to_copy_files.get(key,False):
                for file in value:
                    folder_structure[exdf.confkeys['input_data']][exdf.confkeys['simulation_configuration_files']].append(file)
            if key=="synthpops_configuration_files" and self.to_copy_files.get(key,False):
                for file in value:
                    folder_structure[exdf.confkeys['input_data']][exdf.confkeys['synthpops_configuration_files']].append(file)
            if key=="simulation_immunity_files" and self.to_copy_files.get(key,False):
                for file in value:
                    folder_structure[exdf.confkeys['input_data']][exdf.confkeys['simulation_immunity_files']].append(file)
        self.path=path_with_dir                    
        # Copy from self.to_copy_files to folder_structure
        # Copy to input_folder_structure
        if not self.test:
            exut.create_dirs_based_on_dict(basepath=path_with_dir,dir_structure=folder_structure)
            grut.copy_files_to_parent(path=exut.merge_multiple_paths(base_path=self.path,paths=[exdf.confkeys['input_data'],exdf.confkeys['original_confs']]))

    def process_remote_copy(self):
        # Check klist from another user
        if not self.test:
            try:
                grut.execute_shell_script_and_check_output(command=f"{exut.merge_filepathGC(exdf.grid_process_script)} -f {exdf.grid_script_functions['credentials']}")
            except:
                try:
                    grut.execute_shell_script_and_check_output(command=f" sudo -u {self.grid_settings.get_server_kerberos_name()} {exut.merge_filepathGC(exdf.grid_process_script)} -f {exdf.grid_script_functions['credentials']}")
                except:
                    print("You have no valid kerberos ticket, please contact administrator")
                    return
        # Copy to server
        command=f"{exut.merge_filepathGC(exdf.grid_process_script)} -f {exdf.grid_script_functions['copy_to_remote']} -i {self.path} -u {self.grid_settings.get_user_name()} \
-s {self.grid_settings.get_server_name()} -o {exut.merge_twoPaths(self.grid_settings.get_server_input_path(),os.getlogin())}"
        if not self.test:
            try:
                grut.execute_shell_script(command=command)
                print("Files succesfully coppied to remote server.")
            except:
                print("Error while copying to remote server.")
                return

    def process_qsub(self):
        self.generate_qsub_string()
        self.append_to_queue()

    def generate_qsub_string(self):
        n_cpus=f"{simcg.get_number_of_regions(self.to_copy_files['simulation'])}"
        mem=f"{int(simcg.get_num_of_population(self.to_copy_files['simulation'])/100)}mb" # Totall popullation size
        ssd_capacity="300gb"
        job_name=f"'ABMshare_via:{os.getlogin()}'"
        time="24:00:00"
        cmd_str=f"'qsub -l walltime={time} -q default@pbs-m1.metacentrum.cz -l"        
        cmd_str+=f" select=1:ncpus={n_cpus}:mem={mem}"
        cmd_str+=f":scratch_ssd={ssd_capacity}"
        cmd_str+=f" -N {job_name} -m n -W umask=002"
        cmd_str+=" -W group_list=cvut_fbmi_kbi"
        # Command for qsub
        cmd_str+=f" -- {self.grid_settings.get_server_script_path()}\
 -f {grut.get_folder_name(self.path)}\
 -u {os.getlogin()}\
 -c {os.path.basename(self.to_copy_files['mainconfig'])}'"
        if self.test:
            cmd_str+=" -d true"
        # queue append string
        # self.queue_append_string=f"-a '-u {os.getlogin()} -o {exdf.base_local_output_path(os.getlogin())} -i {exut.merge_multiple_paths(self.grid_settings.get_server_output_path(),[os.getlogin(),os.path.basename(self.path)])}'"
        # print(cmd_str)
        # Command for grid process
        command=f"{exut.merge_filepathGC(exdf.grid_process_script)} -f {exdf.grid_script_functions['send_qsub']} -q {cmd_str} -u {self.grid_settings.get_user_name()}\
 -s {self.grid_settings.get_server_name()}"
        # print()
        if not self.test:
            try:
                grut.execute_shell_script(command=command)
                print("Job succesfully submited to remote server.")
            except:
                print("Error while submitting job to remote server.")
                return
    
    def append_to_queue(self):
        try:
            grut.add_to_queue(user_name=os.getlogin(),local_location=exdf.base_local_output_path(os.getlogin()),
                              remote_location=exut.merge_multiple_paths(self.grid_settings.get_server_output_path(),[os.getlogin(),os.path.basename(self.path)]))
            print("Job succesfully submited to queue for download.")
        except:
            print("Error while appending job to queue.")

if __name__=="__main__":
    grid_compute_settings={
        "value":True,
        "processed":False
    }
    conf_path=""
    test= GridComputeController(config=conf_path,base_conf_path=conf_path,grid_user="user",test=True)
    print()

    