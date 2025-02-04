import json
import pandas as pd
import numpy as np
import os
import pathlib
from datetime import datetime
import abmshare.defaults as exdf
import time
import shutil
import copy
import yaml
from pathlib import Path
import re
import ast


def load_config(filepath=None,report_conf=False):
    filepath = filepath or "config/config.yaml"
    if isinstance(filepath, dict):
        return filepath
    file, ext = os.path.splitext(filepath)
    if ext == ".yaml":
        return load_config_yaml(filepath)
    elif ext == ".json":
        return load_config_json(filepath)
    elif report_conf:
        return []
    else:
        raise ValueError(f"Check configuration file at {filepath}, look for syntax error.")


def load_config_json(filepath):
    try:
        with open(filepath, 'r', encoding="utf-8") as jsonfile:
            config = json.load(jsonfile)
        return config
    except:
        print(f"Cannot load json config file from{filepath}")

def load_config_yaml(filepath):
    with open(filepath, 'r', encoding="utf-8") as yamlfile:
        config = yaml.load(yamlfile, yaml.FullLoader)
    return config

# Method for validating keys


def validate_pars(given_par, default_pars):
    '''
        Method for validating key/s with default keys
        given_par(list of string/s)         : can be one string, which should be compared if its in some collection of keys
                                              can also be list of strings, which are compared if every one of them is in some collection of keys
        default_pars(list of strings)       : default key collection                                            
    '''
    if isinstance(given_par, list):
        for key in given_par:
            if key not in default_pars:
                return False
        return True
    elif isinstance(given_par, str):
        for key in default_pars:
            if given_par == key:
                return True
            # If its not, then return False
        return False
    else:
        try:
            for key in default_pars:
                if given_par == key:
                    return True
            # If its not, then return False
            return False
        except:
            print("Not implemented validating pars")

# Method for loading csv or *xlsx files


def trim_spaces(x):
    try:
        return x.strip()
    except AttributeError:
        return x
    

def load_datafile(filepath: str|pd.DataFrame):
    '''
        Method for reading *xlsx or *csv file. Returns pd.dataframe.
        filepath(str)               : path to file 
    '''
    if isinstance(filepath, pd.DataFrame):
        return filepath
    file, ext = os.path.splitext(filepath)    
    try:
        if ext == ".csv":    
            df=pd.read_csv(filepath)                 
        elif ext == ".xlsx":
            df=pd.read_excel(filepath)
        # Strip whitespace from column names right after loading the data
        df.columns = [col.strip() for col in df.columns]
        # Iterate over each column and strip spaces from string columns
        for col in df.columns:
            if df[col].dtype == object:  # Typically, object type columns are strings
                df[col] = df[col].str.strip()
        return df         
    except NameError as e:
        raise NameError(f"You must use .xlsx or .csv datafiles, file:{filepath} is not supported.")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File {filepath} not found")


# def load_datafile(filepath: str|pd.DataFrame):
#     '''
#         Method for reading *xlsx or *csv file. Returns pd.dataframe.
#         filepath(str)               : path to file 
#     '''
#     if isinstance(filepath, pd.DataFrame):
#         return filepath
#     file, ext = os.path.splitext(filepath)    
#     try:
#         if ext == ".csv":    
#             df=pd.read_csv(filepath)  
#         elif ext == ".xlsx":
#             df=pd.read_excel(filepath)
#         # Trim rows
#         for col in df.columns:
#             if df[col].dtype == object:
#                 df[col] = df[col].str.strip()
#         # Trim columns
#         df.columns = [col.strip() for col in df.columns]
#         # Iterate over each column and strip spaces from string columns
#         for col in df.columns:
#             if df[col].dtype == object:  # Checking for string data type
#                 df[col] = df[col].str.strip()
#         return df
#     except NameError as e:
#         raise NameError(f"You must use .xlsx or .csv datafiles, file:{filepath} is not supported.")
#     except FileNotFoundError as e:
#         raise FileNotFoundError(f"File {filepath} not found")


# Get absolute file path of script


def merge_file_path(path):
    '''
        Method for getting path of executed file and merged with given path.
        path(str)                           : path for merge with default
    '''
    this_dir = os.path.dirname(os.path.abspath(__file__))  # Example dir
    return os.path.join(this_dir, path)


def merge_default_path(path):
    '''
        Method for getting base project path with possibility to get into all structures and merging with given one.
        path(str)                           : path for merge with default
    '''
    this_dir = os.path.abspath(__file__+"/../../")  # Example dir
    return os.path.join(this_dir, path)


def merge_filepathSP(path):
    '''
        Method for getting synthetic_population component path and merging with given one .
        path(str)                           : path for merge with default
    '''
    this_dir = os.path.abspath(
        __file__+f"/../../{exdf.pathvalues['synthetic_population']}")  # Example dir
    return os.path.join(this_dir, path)


def merge_filepathCV(path):
    '''
        Method for getting simulation component path and merging with given one.
        path(str)                           : path for merge with default
    '''
    this_dir = os.path.abspath(
        __file__+f"/../../{exdf.pathvalues['simulation_model']}")  # Example dir
    return os.path.join(this_dir, path)


def merge_twoPaths(path0, path1):
    '''
        Method for merging two paths. For ex. dirpath and filename
        path0(str)                           : default first part of path for merge
        path1(str)                           : path for merge with default
    '''
    return os.path.join(path0, path1)

def merge_multiple_paths(base_path:str,paths:list):
    '''
        Method for merging multiple paths. For ex. dirpath and filename
        base_path(str)                           : default first part of path for merge
        paths(list)                              : list of paths for merge with default
    '''
    for path in paths:
        base_path=os.path.join(base_path,path)
    return base_path

def merge_filepathGC(path:str=None):
    '''
        Method for getting grid_compute component path and merging with given one.
        path(str)                           : path for merge with default
    '''
    if path is None:
        return  os.path.abspath(__file__+f"/../../")
    this_dir = os.path.abspath(
        __file__+f"/../../{exdf.pathvalues['grid_compute']}")  # Example dir
    return os.path.join(this_dir, path)

# Check if directory exists, otherwise create new
def directory_validator(path, create_new=True):
    '''
        Method for  validating dir path and possibility to also create specified dirpath
        path(str)                           : path for validation, if directory exists
        create_new(bool)                    : Default True / if path does not exists, then create this directory based on path
                                              If set to False, then it returns only a boolean, Exist -True, Doesnt Exist - False
    '''
    if os.path.exists(path):
        return True
    else:
        if create_new:
            os.makedirs(path)
            print(
                f"Directory:{path} originally did not exist, creating this directory.")
        return False


def filename_validator(filepath, i=0):
    '''
        Method for validating if specific file exists. Otherwise will return changed filename with increment.
        filepath(string)            :path to file
    '''
    try:
        if os.path.exists(filepath) or os.path.basename(filepath).split(".")[0] in [names for items in os.listdir(os.path.dirname(filepath)) for names in items.split(".")]:
            i += 1
            filename, extension = os.path.splitext(filepath)
            filename += str(i)
            filepath = f"{filename}{extension}"
            filename_validator(filepath)
        else:
            return filepath
        return filepath
    except FileNotFoundError:
        return filepath


def file_validator(filepath):
    '''
        Method for validating if specific file exists. Returns True/False;
        filepath(string)            : path to file
    '''
    if os.path.exists(filepath):
        return True
    else:
        return False

# Function for returning number of mobility people


def prepare_mobility(mobility:pd.DataFrame):
    '''
        mobility(pd.DataFrame)              : dataframe for calculating number of mobility people
    '''
    mobility_arr = np.asarray(mobility[mobility.columns[2:]])
    mobility_arr[np.isnan(mobility_arr)] = 0
    output={}
    for i,val in mobility.iterrows():        
        output[mobility['location_code'][i]]=mobility_arr[i]        
    return output

# Function for validating popsize from .pop file and covasim pars for simulation
def validate_pop_size(simulation_size, popfile_size):
    if simulation_size == popfile_size:
        return True
    else:
        # print(f"Size of people for simulation is:{simulation_size} and size of people from popfile is:{popfile_size}")
        return False

# Function for saving various filetypes


def save_file(dirpath, filename, extension, data):
    if not extension[0] == ".":
        extension = f".{extension}"
    path = os.path.join(dirpath, f"{filename}{extension}")
    #  For pandas dataframe we do not need to starts with : with open
    if extension == ".csv" or extension == "csv":
        data.to_csv(path, index=False)
        return
    elif extension == ".xlsx" or extension == "xlsx":
        data.to_excel(path, index=False)
        return
    with open(path, 'w') as f:
        if extension == ".txt" or extension == "txt":
            f.write(str(data))
            return
        elif extension == ".json" or extension == "json":
            pretty_json = json.dumps(data, indent=2)  # Default indent 2
            f.write(pretty_json)
            return
        else:
            pass  # Not implemented yet
        return
    
def save_csv(path:str,data:pd.DataFrame):
    """_summary_

    Args:
        path (str): path to save, with filename and extension
        data (pd.DataFrame): dataframe data
    """
    data.to_csv(path, index=False)

def save_json(path:str,data:dict|str):
    """_summary_

    Args:
        path (str): path to save, with filename and extension
        data (dict | str): dictionary data
    """
    if isinstance(data,dict):
        data=json.dumps(data,indent=2)
    with open(path, 'w') as f:
        f.write(data)

def delete_mobility(array: np.array, row_and_col):
    '''
        Method for editing mobility array based on sims, which have turned off mobility,
    '''
    output = np.copy(array)
    output = np.delete(output, row_and_col, 0)
    output = np.delete(output, row_and_col, 1)
    return output


def fill_list(list_variable, length):
    '''
        Method for creating python 2D list (list of lists) of given length
    '''
    for i in range(length):
        list_variable.append(list())
    return list_variable


def append_variant(base_variant_list, variants, id):
    '''
        Method for creating python 2D list (list of lists) of given length
        Args:
        variant_list(list)        : input list for appending variants
        variant(list)             : list of dict of variant keys
        id(int)                   : for those variants which must be included in sim, but has no imported illnes.
    '''
    for var in variants:
        diff_variant = copy.deepcopy(var)
        for key, value in exdf.default_empty_variant.items():  # Based on default values from defaults.py
            if key in var:
                diff_variant[key] = value
        for i, row in enumerate(base_variant_list):
            if i == id:
                base_variant_list[i].append(var)
            else:
                base_variant_list[i].append(diff_variant)


def check_variant(variant_list):
    positions_change = []
    positions_remove = []
    variants = []
    positions_change = fill_list(positions_change, len(variant_list))
    positions_remove = fill_list(positions_remove, len(variant_list))
    variants = fill_list(variants, len(variant_list))
    for row in range(len(variant_list)):
        for i, var1 in enumerate(variant_list[row]):
            for j, var2 in enumerate(variant_list[row]):
                if var1['label'] == var2['label'] and i != j and (i not in positions_remove[row] and j not in positions_remove[row]):
                    if var1['days'] > var2['days'] or var1['number_of_imports'] > var2['number_of_imports']:
                        variants[row].append(copy.deepcopy(var1))
                        positions_change[row].append(i)
                        positions_remove[row].append(j)
                    else:
                        variants[row].append(copy.deepcopy(var2))
                        positions_change[row].append(j)
                        positions_remove[row].append(i)
                else:
                    continue

    variant_order = []
    if len(positions_change) > 0:
        # Change values
        temp = np.array(variant_list)
        for row in range(len(variant_list)):
            for index, value in enumerate(positions_change[row]):
                # TODO check if it changes anything
                variant_list[row][value] = variants[row][index]
        # Remove values
        for row in range(len(variant_list)):
            np_row = np.delete(temp[row], positions_remove[row])
            if row == 0:  # for getting the right order:
                variant_order = [x['label'] for x in np_row]
                output_array = np.full(
                    (len(variant_list), np_row.shape[0]), {})
                output_array[row] = np_row
            else:
                output_array[row] = np_row
        output_array = output_array.tolist()
        sort_variants(variant_list=output_array, variant_order=variant_order)
    else:
        return
    return output_array


def sort_variants(variant_list, variant_order):
    '''
        Method for sorting variants based on first sim variant labels.
        variant_list (list)         :list of dict variants
        variant_order (list)        :list of variant labels strings
        Returns
            sorted variant_list
    '''
    for row in range(len(variant_list)):
        for index, value in enumerate(variant_order):
            if variant_list[row][index]['label'] == value:
                pass
            else:
                # right_position =  index
                for substitute, unused in enumerate(variant_list[row]):
                    if substitute == index:
                        continue
                    elif variant_list[row][substitute]['label'] == value:
                        temp = copy.deepcopy(variant_list[row][substitute])
                        variant_list[row][substitute] = variant_list[row][index]
                        variant_list[row][index] = temp
                    else:
                        continue
    return variant_list


def sort_sims(base_sim_list, new_sim_list, key="label"):
    '''
        Method for sorting lists based on second and base key.
    '''
    order = []
    for base_sim in base_sim_list:
        for i, new_sim in enumerate(new_sim_list):
            if isinstance(base_sim, type(new_sim)):
                if getattr(base_sim, key) == getattr(new_sim, key):
                    order.append(i)
                    break
            if isinstance(base_sim, dict):
                if base_sim[key] == getattr(new_sim, key):
                    order.append(i)
                    break
    return [new_sim_list[i] for i in order]


def sort_sims_by_synthpops_location(conf: dict, save_settings_location: str):
    '''
        Method for sorting sims based on synthpops location codes.
        conf(dict)                              : config dict
        save_settings_location(str)             : path to save settings
    '''
    file_list = os.listdir(os.path.join(
        save_settings_location, exdf.save_settings['population_path']))
    if len(file_list) == 0:  # If file list is empty - popfiles provided, no need to sort
        return
    try:
        location_codes = [x['location_code'] for x in conf]
        if location_codes == None or len(location_codes) == 0:
            raise Exception("An exception occurred")
    except Exception as e:
        print(f" There was not location_code key in region config file. Please check it.\
This can cause unexpected behaviour of the program.")
        file_list = sorted(file_list)
        return file_list
    length_of_code = len(location_codes[0])
    # num for extension like (.pop, .json)
    num = len(file_list[0].split(".")[-1]) + 1

    def extract_location_code(filename):
        # Remove the file extension and '_mob' suffix (if present)
        base_name = filename.rsplit(".", 1)[0].replace("_mob", "")
        # Extract the location code
        location_code = base_name[-length_of_code:]
        return location_code

    file_list.sort(key=lambda x: location_codes.index(
        extract_location_code(x)))
    return file_list


def name_generator(basepath: str = "", output_dirname: str = "", increment: str = ""):
    '''
        Method for creating new folder for outputs saves.
        If dirpath and dirname its provided, then its checked, if they already dont exists.
        If they exists, then its added increment, otherwise its based on given parameters.
        basepath(str)                           : path for dir, where are others instances of result outputs
        output_dirname(str)                     : name for a dir in dirpath to save result outputs
        increment(str)                          : feature not implemented yet
    '''
    increment = ""
    if not basepath:
        basepath = merge_default_path(exdf.pathvalues['output_path'])
    # Check if base directory exists, otherwise create it
    directory_validator(basepath)
    temp_dir = str(Path(basepath).joinpath(output_dirname))

    if output_dirname:
        # FIXME: Commented code can be removed after testing 
        # if already exists the same, add increment
        # if directory_validator(temp_dir, False):
        output_final_path = increment_folder_name(temp_dir)
        # else:  # if this folder does not exists, no problem with creating
        #     output_final_path = temp_dir
    else:
        dirpath = get_latest_dir(temp_dir)
        output_final_path = increment_folder_name(dirpath, increment)

    try:
        os.makedirs(output_final_path)
    except FileExistsError:
        time.sleep(60)
        os.makedirs(output_final_path)
    return output_final_path


def is_datetime_with_underscores(datetime_str):
    '''
        Method for checking if datetime_str is in format %Y_%m_%d_%H_%M otherwise its only a string
    '''
    try:
        datetime_obj = datetime.strptime(datetime_str, '%Y_%m_%d_%H_%M')
        return True
    except ValueError:
        return False


def increment_folder_name(dirpath: str):
    """
    Method for adding an increment to dirpath. First, look if there is no increment before.
    Increment is always added with an underscore. Looks for first underscore.
    dirpath(str): directory path
    """
    current_datetime = datetime.now().strftime("%Y_%m_%d_%H_%M")

    # Check for a valid datetime string in the folder name
    datetime_regex = re.compile(r"\d{4}_\d{2}_\d{2}_\d{2}_\d{2}")
    match = datetime_regex.search(str(Path(dirpath).name))

    if match:
        # If a valid datetime string is found, replace it with the new datetime string
        incremented_dirpath = datetime_regex.sub(current_datetime, dirpath)
    else:
        # If no valid datetime string is found, append the new datetime string to the folder name
        incremented_dirpath = dirpath + "_" + current_datetime

    return incremented_dirpath


def validate_folder_in_given_path(path, dirname, temp_dir):
    '''
        Method for validating, if path already contains as tha last folder the same given
        Return path withou dirname
        path(str)                       : dirpath
        dirname(str)                    : specified dirname
    '''
    if dirname == str(os.path.basename(os.path.normpath(path))):
        return os.path.dirname(os.path.dirname(path))
    elif dirname == str(os.path.basename(os.path.normpath(temp_dir))):
        return temp_dir
    return temp_dir


def get_latest_dir(dirpath):
    '''
        Get latest dir / file path and also single name, based on the last creation time.
        It returns dirpath without / on the end
        dirpath(str)                    : returns latest created directory based on dirpath of directories
    '''
    try:
        dirpath = str(
            max(pathlib.Path(dirpath).glob('*/'), key=os.path.getmtime))
        dirname = os.path.basename(os.path.normpath(dirpath))
    except ValueError:
        dirpath = os.path.join(dirpath, "Simulation1")
    return dirpath


def get_last_name_from_path(path):
    '''
        Method for returning the last folder/file in given path.
        path(str)                       : file/dirpath
    '''
    return os.path.basename(os.path.normpath(path))


def copy_files(base_file, new_file):
    '''
        Method for copying one file to another location.
    '''
    try:
        shutil.copyfile(base_file, new_file)
    except:
        print(f"Cannot copy {base_file} as: {new_file}")


def validate_items_in_lists(l1: list, l2: list) -> bool:
    '''
        Method for validating, if items from given l1 are also in l2.
        args:
            l1(list):list of items to compare
            l2(list):list of base items
        returns:
            True - items from l1 are also in l2
            False - at least one item from l1 are not in l2
    '''
    return all(i1 in l2 for i1 in l1)


def validate_key_and_value(d1: dict, s1: str):
    '''
        Method for validating key and value, Assign value, otherwise return none
    '''
    value = d1.get(s1)
    return value


def assign_intervention_keys(intervention: dict, default_keys: list, default_values: dict = None):
    '''
        Method for assigning specific keys to a intervention based on default values to
        fullfill intervention constructor needs. Otherwise it fill with None (when is possible)
        args:
            intervention(dict): dict of intervention key from configuration
            default_keys(list): list of default keys from exddf.defaults
            default_values(dict): dict of key values which are base in constructor of given intervention
        returns:
            None
    '''
    if default_keys is None:
        default_keys = {}
    for key in default_keys:
        try:
            if key not in intervention.keys():
                if key in default_values.keys():
                    intervention[key] = default_values[key]
                else:
                    intervention[key] = None
        except Exception as e:
            print(
                f"An error occured and cannot assign intervention_keys for {intervention}")


# def sort_synthpop_files(loaded_pops:list,conf:dict):
#     '''
#         Method for sorting synthpop files based on their names.
#         args:
#             synthpop_files(list): dict of synthpop files
#         returns:
#             sorted_synthpop_files(dict): sorted dict of synthpop files
#     '''
#     sorted_synthpop_files=[]
#     location_codes = [x['location_code'] for x in conf]
#     for i,pop in enumerate(loaded_pops):
#         name=pop.location_code
#     #TODO: implement first lcoation code in sp.POP()

def sort_synthpop_files(loaded_pops: list, conf: dict):
    """
        Method for sorting synthpop files based on their names.
        args:
            loaded_pops(list): list of objects with the 'location_code' attribute
            conf(dict): configuration dictionary
        returns:
            sorted_synthpop_files(list): sorted list of synthpop files
    """
    # Extract location codes from the conf dictionary
    location_codes = [x['location_code'] for x in conf]

    # Create a dictionary with the location code and its index in the location_codes list
    location_code_order = {code: index for index,
                           code in enumerate(location_codes)}

    # Custom sorting function
    def custom_sort(obj):
        return location_code_order.get(obj.location_code)

    # Sort the loaded_pops list in-place using the custom_sort function
    loaded_pops.sort(key=custom_sort)


def load_config_dict(conf) -> dict:
    '''
        Method for loading configuration file
        args:
            path(str/dict): path to configuration file
        returns:
            config(dict): configuration dictionary
    '''
    if isinstance(conf, dict):
        return conf
    elif isinstance(conf, str):
        return load_config(conf)
    else:
        return None

def create_dirs_based_on_dict(basepath:str,dir_structure:dict) -> None:
    '''
        Method for creating directories based on given dictionary
        args:
            basepath(str): basepath for creating directories
            dirs(dict): dictionary of directories
        returns:
            None
    '''
    for key, value in dir_structure.items():
        new_dir = os.path.join(basepath, key)
        os.makedirs(new_dir, exist_ok=True)
        if isinstance(value, dict):
            create_dirs_based_on_dict(new_dir, value)
        elif isinstance(value, list):
            for file in value:
                if file is not None:
                    try:
                        shutil.copy(file, new_dir)
                    except Exception as e:
                        print(f"Cannot copy {file} to {new_dir}")

def get_logging_file(folder_path:str):
    '''
        Method for getting logging file
    '''
    return os.path.join(folder_path,"logging.txt")

def find_directory(start_dir, dir_name):
    for root, dirs, files in os.walk(start_dir):
        if dir_name in dirs:
            return os.path.join(root, dir_name)
    return None

def get_target_key_in__conf(config:dict|str,path:str=None,target_key:str="num_bins"):
    """Function for getting all occurences of given key in dictionary

    Args:
        config (dict | str): Configuration dictionary or path to configuration dictionary
        path (str, optional): For recursive calling. Defaults to None.
        target_key(str)     : For searching specific key in config
    Yields:
        _type_: positions
    """
    if isinstance(config,str) and path is None:
        config=load_config(config)
    if path is None: path=[]
    # key="num_bins"
    if isinstance(config, dict):
        for key in config:
            new_path = path + [key]
            if key == target_key:
                yield new_path
            for result in get_target_key_in__conf(config[key], new_path):
                yield result
    elif isinstance(config, list):
        for index, item in enumerate(config):
            new_path = path + [index]
            for result in get_target_key_in__conf(item, new_path):
                yield result

def get_value_from_keys(nested_dict, keys):
    for key in keys:
        if isinstance(key, int):
            nested_dict = nested_dict[key]
        else:
            nested_dict = nested_dict[key]
    return nested_dict

def check_consistency(config:dict|str,target_key:str=None):
    if isinstance(config,str):
        config=load_config(config)
    values=list(get_target_key_in__conf(config=config,target_key=target_key))
    output=list()
    for keys in values:
        value = get_value_from_keys(config, keys)
        output.append(value)
    if len(set(output))>1:
        print(f"Values of {target_key} are not consistent across regions. Please check your configuration file. Default global value will be used, if its supplied")
        return False
    return True

def get_nested_value_from_dict(dictionary, keys:list):
    """Return a given value from dictionary based on list of keys

    Args:
        dictionary (_type_): base configuration
        keys (_type_): list of keys

    Returns:
        _type_: returns value on given key
    """
    try:
        current_item = dictionary
        for key in keys:
            current_item = current_item[key]
        return current_item
    except:
        print(f"An error occurred while getting nested value of {''.join(keys)} for dictionary: {dictionary}")
        return None

def is_none_or_empty(value)->bool:
    """
    Check if the value is None or an empty string, list, tuple, or dictionary
    Returns:
      bool (True) : if it has value
      bool (False): if it's none or empty
    """
    if value is None or pd.isna(value):
        return False
    # Check if the value is an empty string, list, tuple, or dictionary
    if isinstance(value, (str, list, tuple, dict)) and not value:
        return False
    return True

def get_index_by_column_and_value(df:pd.DataFrame,column:str,value:str|list):
    """Return index of row based on column and value

    Args:
        df (pd.DataFrame): dataframe
        column (str): column name
        value (str|list): value in column, or values

    Returns:
        int: index of row
    """
    temp=df.copy(True)
    temp[column]=temp[column].str.lower()
    column=column.lower()
    try:
        # If list values are provided
        if isinstance(value,list):
            value=[x.lower() for x in value]
            output=[]
            for val in value:
                try:
                    output.append(temp.set_index(column).index.get_loc(val))
                except:
                    pass
            return output
        # If str value is provided
        value=value.lower()
        return temp.set_index(column).index.get_loc(value)
    except:
        return None

def df_append_to_list(row,column_to_compare,column_to_return):
    """Append a column value to list

    Args:
        row (pd.Series): row of dataframe

    Returns:
        list: list of rows
    """
    valid_true=[1,"1",True,"True","true"]
    if row[column_to_compare] in valid_true:
        return row[column_to_return]
    return None

def get_mobility_num(mobility:dict,location_code:str,all_location_codes:list):
    """Return number of mobility people based on location code

    Args:
        mobility (dict): mobility dictionary
        location_code (str): location code

    Returns:
        int: number of mobility people
    """
    output=0
    id=list(mobility.keys()).index(location_code)
    for key,value in mobility.items():
        if key==location_code:
            continue
        elif key in all_location_codes:
            output+=value[id]
        else:
            continue
    return output


def generate_population_filename(region_name:str,prefix:str=None,suffix:str=None,test:bool=None):
    '''
        Method for handlind suffixes and preffixes from conf/kwargs value.
        Also change the extension based on mobility.
    '''
    filename=""
    prefix=prefix or ""
    suffix=suffix or ""        
    # Handle test default suffix, prefix
    if test:
        suffix=exdf.testsettings['suffix']
        prefix=exdf.testsettings['prefix']
    filename=f"{prefix}{region_name}{suffix}"
    return filename

def convert_str_to_date(date:str,format:str):
    '''
        Method for converting date to datetime object
    '''
    return datetime.strptime(date,"%Y-%m-%d")

def convert_date_to_str(date:datetime,format:str):
    '''
        Method for converting datetime object to string
    '''
    return date.strftime(format)

def convert_string_lists(s:str):
    '''
        Method for converting string to list
    '''
    try:
        # Remove outer quotes if present
        s = s.strip('\'"')

        # Helper function to convert string to float or int as appropriate
        def to_number(item):
            try:
                val = float(item)
                if val.is_integer():
                    return int(val)
                return val
            except ValueError:
                return item

        # If the string starts with [ and ends with ] 
        # and contains elements not enclosed in quotes, 
        # enclose them in single quotes.
        if s.startswith('[') and s.endswith(']'):
            s = '[' + ','.join([f"'{item.strip()}'" if not item.strip().replace('.', '', 1).isdigit() else item.strip() for item in s[1:-1].split(",")]) + ']'
        
        # Convert string representation to actual Python object
        obj = ast.literal_eval(s)
        
        # If the result is a list, convert to appropriate data type
        if isinstance(obj, list):
            return [to_number(item) if isinstance(item, str) else item for item in obj]
        else:
            return obj
    except Exception as e:
        print(f"An error occurred while converting string to list: {e}")
        return s

def compare_two_types(a,b):
    '''
        Method for comparing two types of variables
    '''
    return type(a) == type(b)

def deepcopy_object(object):
    '''
        Method for deepcopying object
    '''
    return copy.deepcopy(object)

def return_dictionary_index_basex_by_code(dictionary:dict,code:str):
    '''
        Method for returning index of dictionary based on code
    '''
    keys_list = list(dictionary.keys())
    position = keys_list.index(code) if code in keys_list else None
    return position

def get_all_files_in_directory(directory:str)->list:
    '''
        Method for getting all files in directory
    '''
    return  [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def get_filename(filepath:str)->str:
    '''
        Method for getting filename from filepath
    '''
    if isinstance(filepath,str):
        return os.path.basename(filepath)
    else:
        return None
    
def get_all_csv_files(config:dict|str,config_combos:list,return_dict:bool=False,filenames:list=None):
    "Get filepaths to all data csvs"
    config = load_config_dict(config)
    output=[] if not return_dict else {}
    for file in config_combos:
        if file_validator(get_nested_value_from_dict(dictionary=config,keys=file)) and return_dict:
            if not filenames:
                output[file[0]]=get_nested_value_from_dict(dictionary=config,keys=file)
            else:
                for f in filenames:
                    if f in file and not "mobility_data" in file: # Only for validator method in
                        output[f]=get_nested_value_from_dict(dictionary=config,keys=file)
        elif file_validator(get_nested_value_from_dict(dictionary=config,keys=file)):
            output.append(get_nested_value_from_dict(dictionary=config,keys=file))
    if return_dict:
        return output
    return list(set(output))

def safe_eval_fraction(fraction_str):
    """ Safely evaluate a string representing a fraction and convert it to a numpy float. """
    # Check if the input string is a valid fraction
    if not re.match(r'^-?\d+/-?\d+$', fraction_str):
        raise ValueError("Invalid input format for a fraction")

    # Evaluate the fraction
    result = eval(fraction_str, {"__builtins__": None}, {})

    # Convert to numpy float
    return np.float64(result)