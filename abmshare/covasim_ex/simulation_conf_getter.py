import abmshare.utils as exut
import abmshare.defaults as exdf
import numpy as np
import pandas as pd

def get_popfiles(config:dict|str,code:str=None,popfile:str=None):
    """Get population files from configuration, single popfile, or as override from save_pars

    Args:
        config (dict/dict): configuration or path to configuration
        code (str, optional): code of the region. Defaults to None.
        popfile (str, optional): path to population file. Defaults to None. 
    Returns:
        list: list of population files paths, if only config provided
        str: path to population file, if code provided
        str: path to population file, if popfile provided
    """
    config=exut.load_config_dict(config)
    try:
        data=exut.load_datafile(exut.get_nested_value_from_dict(dictionary=config,
                                            keys=exdf.covasim_region_parameters_confkeys).get(exdf.confkeys['filepath'],None))
        id=exut.get_index_by_column_and_value(data,exdf.covasim_region_csv_columns['location_code'],code)
        if id == None and popfile ==None: # For grid compute returner
            return list(data[exdf.covasim_region_csv_columns['popfile']])
        return data[exdf.covasim_region_csv_columns['popfile']][id] if popfile==None else popfile
    except Exception as e:
        print(f"Error in get_popfiles\n{e}")
        return None
    

def get_mobility_filepath(config:dict|str)->str|None:
    """Get mobility file filepath

    Args:
        conf (dict | str): configuration

    Returns:
        str | None: path to mobility, if exists
    """
    config=exut.load_config_dict(config)
    try:
        if exut.get_nested_value_from_dict(dictionary=config,keys=exdf.covasim_mobility_confkeys).get(exdf.confkeys['value'],None):
            return exut.get_nested_value_from_dict(dictionary=config,keys=exdf.covasim_mobility_confkeys).get(exdf.confkeys['filepath'],None)
        else: # When there is not provided mobility data, just return none            
            return None
    except:
        print("There is problem with get_mobility_filepath")
        return None


def get_population_filepath(config:dict|str)->str|None:
    """Get population file filepath

    Args:
        conf (dict | str): configuration

    Returns:
        str | None: path to population file, if exists
    """
    config=exut.load_config_dict(config)
    try:
        return exut.get_nested_value_from_dict(dictionary=config,keys=exdf.covasim_population_size_confkeys).get(exdf.confkeys['filepath'],None)
    except:
        print("There is problem with get_population_filepath")
        return None

def get_number_of_regions(config:dict|str)->int|None:
    """Get number of regions

    Args:
        conf (dict | str): configuration

    Returns:
        int: number of regions
    """
    config=exut.load_config_dict(config)
    valid_true=exdf.valid_true_values
    try:
        data = exut.load_datafile(exut.get_nested_value_from_dict(dictionary=config,
                                        keys=exdf.covasim_region_parameters_confkeys).get(exdf.confkeys['filepath'],None))
        return len(data.loc[data['use'].isin(valid_true),'location_code'].values)
    except:
        print("There is problem with get_number_of_regions")
        return None

def get_num_of_population(config:dict|str)->int|None:
    """Get number of population from all given region interested in

    Args:
        conf (dict | str): configuration

    Returns:
        int: number of population files
    """
    config=exut.load_config_dict(config)
    valid_true=exdf.valid_true_values
    try:
        data = exut.load_datafile(exut.get_nested_value_from_dict(dictionary=config,
                                        keys=exdf.covasim_region_parameters_confkeys).get(exdf.confkeys['filepath'],None))
        location_codes=data.loc[data['use'].isin(valid_true),'location_code'].values
        pop_data=exut.load_datafile(get_population_filepath(config))
        size=np.sum(pop_data.loc[data['location_code'].isin(location_codes),'population_size'].values)
        return size
    except:
        print("There is problem with number of population")
        return None


def get_pop_size_by_code(config:dict|str,code:str,mobility:bool=True)->int|None:
    """Get population size by given code

    Args:
        config (dict | str): _description_
        code (str): location code

    Returns:
        int: num of population size
    """
    config=exut.load_config_dict(config)
    valid_true=exdf.valid_true_values
    try:
        data = exut.load_datafile(exut.get_nested_value_from_dict(dictionary=config,
                                        keys=exdf.covasim_region_parameters_confkeys).get(exdf.confkeys['filepath'],None))
        location_codes=data.loc[data['use'].isin(valid_true),'location_code'].values
        pop_data=exut.load_datafile(get_population_filepath(config))
        if code in data.loc[data['use'].isin(valid_true),'location_code'].values:
            size = int(pop_data.loc[pop_data['location_code'] == code, 'population_size'].values[0])
        # Add if mobility 
        if get_mobility_filepath(config) is not None and mobility:
            mob_data=exut.load_datafile(get_mobility_filepath(config))
            size+=mob_data[mob_data['location_code'].isin(location_codes)][code].sum()
        elif get_mobility_filepath(config) is not None and not mobility: # to get size without mobility
            pass
        # else:
        #     print(f"There is no code {code} in the configuration")
        #     return None
        else:
            pass
        return size
    except:
        print(f"There is problem with number of population for location code: {code}")
        return None

def get_global_pars(config:dict|str,parameter:str=None)->dict|None: 
    """Get global pars from configuration. Datafile > config pars

    Args:
        conf (dict | str): configuration
        parameter (str, optional): parameter to get. Defaults to None (all

    Returns:
        dict | None: global pars
        value | None: value of given parameter
    """
    config=exut.load_config_dict(config)
    try:
        data=exut.load_datafile(exut.get_nested_value_from_dict(dictionary=config,
                                        keys=exdf.covasim_global_parameters_confkeys).get(exdf.confkeys['filepath'],None))
        additive_pars=exut.get_nested_value_from_dict(dictionary=config,
                                                        keys=exdf.covasim_global_parameters)
        data_pars = data.iloc[0].to_dict()
        combined_dict = {**additive_pars, **data_pars}
        keys_to_remove=[key for key in combined_dict.keys() if key not in exdf.covasim_pars_all]
        for key in keys_to_remove: 
            print(f"Removing invalid key: {key} from global pars.")
            del combined_dict[key] 
        if parameter is not None:
            return combined_dict.get(parameter,None)
        return combined_dict
    except Exception as e:
        print("There is problem with get_global_pars")
        print(f"Exception: {e}")
        return None

def get_pars_by_code(config:dict|str,code:str)->dict|None:
    """Get pars by code + merge them with global pars (if exists, but global consistency > region specific)
        Code can be location specific or parent code (e.g. CZ01, CZECHIA)
    Args:
        conf (dict | str): configuration

    Returns:
        dict: pars by code
    """
    config=exut.load_config_dict(config)
    valid_true=exdf.valid_true_values
    try:
        data=exut.load_datafile(exut.get_nested_value_from_dict(
                dictionary=config,keys= exdf.covasim_region_parameters_confkeys).get(exdf.confkeys['filepath'], None))
        if code in data.loc[data['use'].isin(valid_true),'location_code'].values:
            id = exut.get_index_by_column_and_value(
                data, exdf.covasim_region_csv_columns['location_code'], code)
            out_pars=dict()
            for key,value in data.iloc[id].items():
                if key in exdf.covasim_pars_all or key in exdf.covasim_region_csv_columns:
                    if key == 'popfile' and (value is not None and not pd.isna(value)):
                        out_pars[key] = value if exut.file_validator(value) else None
                        continue
                    else:
                        out_pars[key] = value
            global_pars=get_global_pars(config)
            out_pars = {**out_pars, **global_pars}             
        else:
            print(f"Region code: {code} is not enabled or does not exists")
            return None
        return out_pars
    except Exception as e:
        print(f"There is problem with get_pars_by_code for location code: {code}")
        print(f"Exception: {e}")
        return None

def get_region_codes(config:dict|str)->list|None:
    """Get region codes from configuration

    Args:
        conf (dict | str): configuration

    Returns:
        list: list of region codes
    """
    config=exut.load_config_dict(config)
    valid_true=exdf.valid_true_values
    try:
        data=exut.load_datafile(exut.get_nested_value_from_dict(dictionary=config,
                                        keys=exdf.covasim_region_parameters_confkeys).get(exdf.confkeys['filepath'],None))
        return data.loc[data['use'].isin(valid_true),'location_code'].values
    except:
        print("There is problem with get_region_codes")
        return None

def get_region_name(config:dict|str,code:str)->str|None:
    """Get region name by code

    Args:
        conf (dict | str): configuration
        code (str): location code

    Returns:
        str | None: region name
    """
    config=exut.load_config_dict(config)
    valid_true=exdf.valid_true_values
    try:
        data=exut.load_datafile(exut.get_nested_value_from_dict(dictionary=config,
                                        keys=exdf.covasim_region_parameters_confkeys).get(exdf.confkeys['filepath'],None))
        if code in data.loc[data['use'].isin(valid_true),'location_code'].values:
            id = exut.get_index_by_column_and_value(data, exdf.covasim_region_csv_columns['location_code'], code)
            return data.iloc[id][exdf.covasim_region_csv_columns['name']]
        else:
            print(f"Region code: {code} is not enabled or does not exists")
            return None
    except:
        print(f"There is problem with get_region_name for location code: {code}")
        return None

def get_region_parent_name(config:dict|str,code:str)->str|None:
    """Get region parent name by code

    Args:
        conf (dict | str): configuration
        code (str): location code

    Returns:
        str | None: region parent name
    """
    config=exut.load_config_dict(config)
    valid_true=exdf.valid_true_values
    try:
        data=exut.load_datafile(exut.get_nested_value_from_dict(dictionary=config,
                                        keys=exdf.covasim_region_parameters_confkeys).get(exdf.confkeys['filepath'],None))
        if code in data.loc[data['use'].isin(valid_true),'location_code'].values:
            id = exut.get_index_by_column_and_value(data, exdf.covasim_region_csv_columns['location_code'], code)
            return data.iloc[id][exdf.covasim_region_csv_columns['region_parent_name']]
        else:
            print(f"Region code: {code} is not enabled or does not exists")
            return None
    except:
        print(f"There is problem with get_region_parent_name for location code: {code}")
        return None
    
def get_interventions_by_code(config:dict|str,code:str)->dict|None:
    """Method for generating intervention dictionary by pars. Global + region specific

    Args:
        config (dict | str): _description_
        code (str): _description_

    Returns:
        dict|None: _description_ returns app_dict
    """
    config=exut.load_config_dict(config)
    valid_true=exdf.valid_true_values
    try:
        location_codes=[x.lower() for x in[code,get_region_parent_name(config,code),'global']] # to lowercase
        data=exut.load_datafile(exut.get_nested_value_from_dict(dictionary=config,
                                            keys=exdf.covasim_interventions_confkeys).get(exdf.confkeys['filepath'],None))
        indexes=data.loc[data['location_code'].str.lower().isin(location_codes)].index
        intervention_list=[]
        for row in indexes:
            row=data.iloc[row]
            row_dict={col:row[col] for col in data.columns if pd.notna(row[col]) and row[col]!=""}
            # Check consistency
            if row_dict[exdf.confkeys['intervention_type']] in exdf.interventions.keys() and row_dict[exdf.confkeys['use']]: # if its not use==true, it will not continue
                remaining_keys=set(row_dict.keys())-set(exdf.covasim_intervention_exclude_keys)
                remaining_keys.add('type')
                if remaining_keys.issubset(exdf.interventions[row_dict[exdf.confkeys['intervention_type']]]):
                    app_dict={key:row_dict[key] for key in remaining_keys if key != 'type'} # Change to another dict
                    app_dict['type']=row_dict[exdf.confkeys['intervention_type']]
                else:
                    print(f"There is inconsistency for intervention type: {row_dict[exdf.confkeys['intervention_type']]}, you can use only those keys:\n{exdf.interventions[row_dict[exdf.confkeys['intervention_type']]]}\n\
        but you provided:\n{remaining_keys}")
            else:
                continue
            # Check list values consistency
            for key in app_dict.keys():
                if (key in exdf.covasim_intervention_list_keys) and isinstance(app_dict[key],str) and (app_dict[key].startswith("[")):
                    try:
                        app_dict[key]=exut.convert_string_lists(app_dict[key])
                    except:
                        print(f"Cannot evaluate {app_dict[key]} to list")
                        app_dict[key]=None
            intervention_list.append(app_dict)
        return intervention_list
    except Exception as e:
        print(f"There is problem with get_interventions_by_pars for location code: {code}")
        print(f"Exception: {e}")
        return None

def get_mobility_data_by_code(config:dict|str,code:str)->dict|None:
    """Method for generating mobility dictionary. Based on code how many people travels there from this region code.

    Args:
        config (dict | str): _configuration file loaded or path
        code (str): region code

    Returns:
        dict|None: _description_ returns Dictionary of mobility to region codes
    """
    config=exut.load_config_dict(config)
    valid_true=exdf.valid_true_values
    region_codes=get_region_codes(config)
    output={}
    try:
        data=exut.load_datafile(exut.get_nested_value_from_dict(dictionary=config,
                                        keys=exdf.covasim_region_parameters_confkeys).get(exdf.confkeys['filepath'],None))
        if code in data.loc[data['use'].isin(valid_true),'location_code'].values:
            id = exut.get_index_by_column_and_value(data, exdf.covasim_region_csv_columns['location_code'], code)
        else:
            print(f"Region code: {code} is not enabled or does not exists")
            return None
        if get_mobility_filepath(config) is not None:
            mob_data=exut.load_datafile(get_mobility_filepath(config))
            for region_code in region_codes:
                output[region_code]=(mob_data[mob_data['location_code']==code].iloc[0])[region_code]
        else:
            raise Exception(f"There is no mobility data provided for location code:{code}")
        return output
    except:
        print(f"There is problem with get_region_parent_name for location code: {code}")
        return None 


def get_incoming_mobility_data_by_code(config:dict|str,code:str)->dict|None:
    """Method for generating mobility dictionary. Based on code how many people travels there TO this region code.

    Args:
        config (dict | str): _configuration file loaded or path
        code (str): region code

    Returns:
        dict|None: _description_ returns Dictionary of mobility to region codes
    """
    config=exut.load_config_dict(config)
    valid_true=exdf.valid_true_values
    region_codes=get_region_codes(config)
    output={}
    try:
        data=exut.load_datafile(exut.get_nested_value_from_dict(dictionary=config,
                                        keys=exdf.covasim_region_parameters_confkeys).get(exdf.confkeys['filepath'],None))
        if code in data.loc[data['use'].isin(valid_true),'location_code'].values:
            id = exut.get_index_by_column_and_value(data, exdf.covasim_region_csv_columns['location_code'], code)
        else:
            print(f"Region code: {code} is not enabled or does not exists")
            return None
        if get_mobility_filepath(config) is not None:
            mob_data=exut.load_datafile(get_mobility_filepath(config))
            for region_code in region_codes:
                 output[region_code]=mob_data.loc[mob_data['location_code'] == region_code, code].iloc[0]
        else:
            raise Exception("There is no mobility data provided.")
        return output
    except:
        print(f"There is problem with get_region_parent_name for location code: {code}")
        return None 

def get_variants(config:dict|str):
    """Get variants from configuration

    Args:
        conf (dict | str): configuration

    Returns:
        dict: variants
    """
    config=exut.load_config_dict(config)
    try:
        variants=exut.load_datafile(exut.get_nested_value_from_dict(dictionary=config,
                                        keys=exdf.covasim_immunity_confkeys).get(exdf.confkeys['filepath'],None))
        return variants
    except:
        print("There is problem with get_variants")
        return None

def get_immunity_files(config:dict|str):
    """Get immunity files from configuration

    Args:
        conf (dict | str): configuration

    Returns:
        dict: immunity files
    """
    config=exut.load_config_dict(config)
    output=[]
    try:
        immunity_files=exut.load_datafile(exut.get_nested_value_from_dict(dictionary=config,
                                        keys=exdf.covasim_immunity_confkeys).get(exdf.confkeys['filepath'],None))
        output.append(exut.get_nested_value_from_dict(dictionary=config,
                                        keys=exdf.covasim_immunity_confkeys).get(exdf.confkeys['filepath'],None))
        for file in exdf.covasim_immunity_files:
            if exut.file_validator(immunity_files[file][0]):
                output.append(immunity_files[file][0])
            else:
                print(f"File {file} is not valid")
                return []
        return output
    except:
        print("There is problem with get_immunity_files")
        return []

def get_all_csv_files(config:dict|str): 
    "Get filepaths to all data csvs"
    config = exut.load_config_dict(config)
    output=[]
    for file in exdf.covasim_data_files:
        if "immunity" in file: # for immunity files
            continue # output.extend(get_immunity_files(config))
        if exut.file_validator(exut.get_nested_value_from_dict(dictionary=config,keys=file)):
            output.append(exut.get_nested_value_from_dict(dictionary=config,keys=file))
    return list(set(output))


# if __name__=="__main__":
#     config="/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/simulation_with_variants.json"
#     get_all_data=get_immunity_files(config)
#     print()
#     code="CZ01"
#     # test_get_popfiles=get_popfiles(config)
#     # test_get_popfiles2=get_popfiles(config,code=code)
#     # test_get_popfiles3=get_popfiles(config,popfile="/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/synthpops_input_data/CZ01/CZ01_synthpops_pops_2021-03-01_2021-03-31.csv")
#     # test_get_mobility_filepath=get_mobility_filepath(config)
#     # test_get_number_of_regions=get_number_of_regions(config)
#     # test_get_num_of_population=get_num_of_population(config)
#     # test_get_pop_size_by_code=get_pop_size_by_code(config,code)
    # test_get_global_pars=get_global_pars(config,'start_day')
#     # test_get_pars_by_code=get_pars_by_code(config,code)
#     # test_get_region_parent_name=get_region_parent_name(config,code)
#     test_get_interventions_by_pars=get_interventions_by_code(config,code)
#     # test_get_region_codes=get_region_codes(config)
#     # test_get_mobility_dict=get_mobility_data_by_code(config,code)
#     # test_get_to_mobility_dict=get_incoming_mobility_data_by_code(config,code)
    # print()
