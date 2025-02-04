import os
from pathlib import Path
import abmshare.defaults as exdf
import abmshare.utils as exut
import pandas as pd

class Grid_change_path:
    def __init__(self,wait:bool=False):
        """ Function for changing paths

        Args:
            configuration (dict): main configuration file
        """
        # Main variables
        # Default values from defaults
        self.grid_keys=exdf.grid_dict_info
        self.directory_structure=exdf.input_folder_structure
        # Getters
        self.current_directory_name=self.get_current_directory()
        self.mapped_directory_files=self.dirToDict(self.current_directory_name)
        # Process function 
        if not wait: self.process()

    def process(self):
        """Process function
        """
        # Configuration files
        for file in self.mapped_directory_files['input_data']['files']:     
            if file.split('.')[-1] in exdf.grid_configuration_extensions:
                conf_file=exut.load_config(file)
                conf_file=self.update_config_paths(conf_file, self.mapped_directory_files)
                exut.save_json(file,conf_file)
        # Synthpops input data files
        for file in self.mapped_directory_files['input_data']['synthpops_configuration_files']['files']:     
            if file.split('.')[-1] in exdf.grid_csv_extensions:
                data=exut.load_datafile(file)
                data=self.update_dataframe_paths(data, self.mapped_directory_files)
                exut.save_csv(file,data)
        # Covasim input data files
        for file in self.mapped_directory_files['input_data']['simulation_configuration_files']['files']:
            if file.split('.')[-1] in exdf.grid_csv_extensions:
                data=exut.load_datafile(file)
                data=self.update_dataframe_paths(data, self.mapped_directory_files)
                exut.save_csv(file,data)
        # Covasim immunity data files
        for file in self.mapped_directory_files['input_data']['simulation_immunity_files']['files']:
            if file.split('.')[-1] in exdf.grid_csv_extensions:
                data=exut.load_datafile(file)
                data=self.update_dataframe_paths(data, self.mapped_directory_files)
                exut.save_csv(file,data)

    def get_current_directory(self):        
        try:
            current_directory=str(Path(os.environ.get('SCRATCHDIR')).joinpath(self.grid_keys['default_base_directory']))
        except:
            current_file_path = Path(__file__).resolve()
            current_directory = current_file_path.parent
        return str(current_directory)    

    def dirToDict(self, dirPath):
        d = {}
        for i in [os.path.join(dirPath, i) for i in os.listdir(dirPath) if os.path.isdir(os.path.join(dirPath, i))]:
            d[os.path.basename(i)] = self.dirToDict(i)  # Keep basename for dictionary keys
        d['files'] = [os.path.join(dirPath, i) for i in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, i))]  # Use full path for file names in the list
        return d
        

    def update_dataframe_paths(self, df, mapped_dict):
        # Go through each cell in the dataframe
        for col in df.columns:
             if col.lower() in exdf.grid_csv_replace_keys or col.lower() in exdf.grid_conf_replace_keys or col.lower() in exdf.grid_csv_immunity_replace_keys:  # Check if the column name suggests it contains file paths
                df[col] = df[col].apply(lambda x: self.find_in_mapped_dict(mapped_dict, os.path.basename(x)) if isinstance(x, str) else x)
        return df

    def find_in_mapped_dict(self, mapped_dict, filename):
        # Recursive search for the filename in the mapped directory dictionary
        for key, value in mapped_dict.items():
            if key == 'files' and isinstance(value, list):
                for file in value:
                    if os.path.basename(file) == filename and 'original_confs' not in file: # Just to be sure, that it's not the original file directory
                        return file
            elif isinstance(value, dict):
                result = self.find_in_mapped_dict(value, filename)
                if result:
                    return result
        return None

    def update_config_paths(self, config, mapped_dict):
        # Recursive function to update the paths in the config
        for key, value in config.items():
            if key.lower() in exdf.grid_conf_replace_keys and isinstance(value, str):  # Check if the key suggests it's a file path
                if key.lower() == 'location':
                    config[key] = str(Path(os.environ.get('SCRATCHDIR')).joinpath(self.grid_keys['default_base_directory']).joinpath("output_data"))                 
                new_path = self.find_in_mapped_dict(mapped_dict, os.path.basename(value))
                if new_path:
                    config[key] = new_path
            elif isinstance(value, dict):
                self.update_config_paths(value, mapped_dict)
        return config
      

if __name__=="__main__":
    # os.environ['SCRATCHDIR']="/home/user/sandbox" Just for testing
    neco=Grid_change_path()
    print("Grid change path is done.")
