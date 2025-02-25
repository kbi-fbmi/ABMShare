import pandas as pd

import abmshare.defaults as exdf
import abmshare.utils as exut

# This utils script is for getting selected values from configuration


def get_mobility_filepath(config: dict | str):
    """Get mobility filepath
    Args:
        conf (dict): synthpops configuration

    Returns:
        str/none: path to mobility file, or None

    """
    config = exut.load_config_dict(config)
    output = exut.get_nested_value_from_dict(dictionary=config,keys=exdf.synthpops_mobility_confkeys).get(exdf.confkeys["filepath"], None)
    if output != "" and not None:
        return output
    return None


def get_parent_location(config: dict | str, code: str = None):
    """Get parent json location file

    Args:
        conf (dict): synthpops configuration

    Returns:
        str/none: path to parent json config, or None

    """
    config = exut.load_config_dict(config)
    try:
        data = exut.load_datafile(exut.get_nested_value_from_dict(
            config, exdf.synthpops_creator_confkeys).get(exdf.confkeys["filepath"], None))
        id = exut.get_index_by_column_and_value(
            data, exdf.synthpops_region_csv_columns["location_code"], code)
        if id == None:
            output = []
            for i in range(len(data)):
                if data["use"][i]:
                    output.append(calculate_filepath(data=data, i=i, dirpath=exdf.synthpops_region_csv_columns["parent_dirpath"], filename=exdf.synthpops_region_csv_columns["parent_filename"],
                                                    filepath=exdf.synthpops_region_csv_columns["parent_filepath"], region_parent_name=exdf.synthpops_region_csv_columns["region_parent_name"]))
        else:
            output = calculate_filepath(data, id, dirpath=exdf.synthpops_region_csv_columns["parent_dirpath"], filename=exdf.synthpops_region_csv_columns["parent_filename"],
                                        filepath=exdf.synthpops_region_csv_columns["parent_filepath"], region_parent_name=exdf.synthpops_region_csv_columns["region_parent_name"])
    except:
        print("There is not provided parent location")
    if output != "" and not None:
        if isinstance(output, list):
            return list(set(output))
        return output
    return None


def calculate_filepath(data: pd.DataFrame, i: int, dirpath: str = None, filename: str = None, filepath: str = None, region_parent_name: str = None) -> str|None:
    """_summary_

    Args:
        data (pd.DataFrame): dataframe
        i (int): num of row
        dirpath (str, optional): dirpath, if exists. Defaults to None.
        filename (str, optional): filename if exists - can look to dirpath or to the defaults. Defaults to None.
        filepath (str, optional): if full filepath exists. Defaults to None.
        region_parent_name (str, optional): _description_. Defaults to None.

    Returns:
        str|None: filepath

    """
    if exut.is_none_or_empty(data[filepath][i]) and exut.file_validator(data[filepath][i]):
        output = data[filepath][i]
    elif exut.is_none_or_empty(data[dirpath][i]) and exut.is_none_or_empty(data[filename][i]) and exut.file_validator(exut.merge_twoPaths(data[dirpath][i], data[filename][i])):
        output = exut.merge_twoPaths(data[dirpath][i], data[filename][i])
    else:
        if exut.is_none_or_empty(data[filename][i]) and exut.file_validator(exut.merge_filepathSP(data[filename][i])):
            output = exut.merge_filepathSP(data[filename][i])
        elif exut.is_none_or_empty(data[region_parent_name][i]) and exut.file_validator(exut.merge_filepathSP(f"data/{data[region_parent_name][i]}.json")):
            output = exut.merge_filepathSP(
                f"data/{data[region_parent_name][i]}.json")
        else:
            print("Cannot find parent location,using default")
            output=exut.merge_filepathSP(exdf.default_synthpops_parent_configuration)
    return output


def get_region_true(config: dict | str, code:int|str):
    """Get if region is true and enabled

    Args:
        config (dict | str): configuration file or dictionary
        code (int): _description_

    Returns:
        _type_: _description_

    """
    config = exut.load_config_dict(config)
    valid_true=exdf.valid_true_values
    try:
        data = exut.load_datafile(exut.get_nested_value_from_dict(
            dictionary=config,keys= exdf.synthpops_creator_confkeys).get(exdf.confkeys["filepath"], None))
        id = exut.get_index_by_column_and_value(
            data, exdf.synthpops_region_csv_columns["location_code"], code)
        if data[exdf.synthpops_region_csv_columns["use"]][id] in valid_true:
            return True
    except:
        return False
    return False

def get_all_regions(config:dict|str,return_codes:bool=True):
    """Get all regions which are true and enabled

    Args:
        config (dict | str): configuration file or dictionary
        return_cored (bool): if return codes when true, otherwise return IDs of rows
    Returns:
        _type_: _description_

    """
    config = exut.load_config_dict(config)
    output = list()
    try:
        data = exut.load_datafile(exut.get_nested_value_from_dict(
            dictionary=config,keys= exdf.synthpops_creator_confkeys).get(exdf.confkeys["filepath"], None))
        for id in range(len(data)):
            if get_region_true(config,data[exdf.synthpops_region_csv_columns["location_code"]][id]):
                    output.append(data[exdf.synthpops_region_csv_columns["location_code"]][id])
    except:
        print("There is an error durring parsing synthpops csv input files")
        return False
    return output


def get_region_specific_csv_files(config:dict|str,location_code:str=None,mapped_output:bool=False):
    """Get region specific csv files

    Args:
        conf (dict): synthpops configuration

    Returns:
        list: list of paths region specific csv files

    """
    config = exut.load_config_dict(config)
    output = list()
    mapped_output=dict()
    try:
        data=exut.load_datafile(exut.get_nested_value_from_dict(dictionary=config,
                            keys=exdf.synthpops_global_input_data_confkeys).get(exdf.confkeys["filepath"], None))
        region_data=exut.load_datafile(exut.get_nested_value_from_dict(
                dictionary=config, keys=exdf.synthpops_creator_confkeys).get(exdf.confkeys["filepath"], None))
        pattern={"location_code":"","region_parent_name":""}
        temp=list()
        i=exut.get_index_by_column_and_value(region_data,exdf.synthpops_region_csv_columns["location_code"],location_code)
        if region_data["use"][i]:
            pattern[exdf.synthpops_region_csv_columns["location_code"]]=region_data[exdf.synthpops_region_csv_columns["location_code"]][i]
            pattern[exdf.synthpops_region_csv_columns["region_parent_name"]]=region_data[exdf.synthpops_region_csv_columns["region_parent_name"]][i]
            temp.append(pattern)

        for i in range(len(temp)): # Get all used global csv files
            if exut.get_index_by_column_and_value(data,exdf.synthpops_region_csv_columns["location_code"],temp[i][exdf.synthpops_region_csv_columns["location_code"]]) is not None:
                id= exut.get_index_by_column_and_value(data,exdf.synthpops_region_csv_columns["location_code"],temp[i][exdf.synthpops_region_csv_columns["location_code"]])
                for col_name,value in data.items():
                    if col_name in exdf.synthpops_csv_files:
                        output.append(data[col_name][id]) if data[col_name][id]!="" else None
                        mapped_output[col_name]=data[col_name][id] if data[col_name][id]!="" else None
            elif exut.get_index_by_column_and_value(data,exdf.synthpops_region_csv_columns["location_code"],temp[i][exdf.synthpops_region_csv_columns["region_parent_name"]]) is not None:
                id=exut.get_index_by_column_and_value(data,exdf.synthpops_region_csv_columns["location_code"],temp[i][exdf.synthpops_region_csv_columns["region_parent_name"]])
                for col_name,value in data.items():
                    if col_name in exdf.synthpops_csv_files:
                        output.append(data[col_name][id]) if data[col_name][id]!="" else None
                        mapped_output[col_name]=data[col_name][id] if data[col_name][id]!="" else None
    except:
        print("There is an error durring parsing synthpops csv input files")
        return list()
    if mapped_output:
        return mapped_output
    output=list(set(output))
    return output

def get_synthpops_parameters(config:str|dict,location_code:str=None,region_parent_name:str=None):
    config = exut.load_config_dict(config)
    pars=dict()
    # try:
    filepath = exut.get_nested_value_from_dict(dictionary=config,keys=exdf.synthpops_parameters_confkeys).get(exdf.confkeys["filepath"],None)
    data = exut.load_datafile(filepath) if filepath is not None else print("There is no filepath for synthpops parameters") # Pars data

    if location_code is not None and exut.get_index_by_column_and_value(data,exdf.synthpops_region_csv_columns["location_code"],location_code) is not None:
        row=exut.get_index_by_column_and_value(data,exdf.synthpops_region_csv_columns["location_code"],location_code)
        for key, value in data.items():
            if key in exdf.synthpops_pars["pop_creator_pars"]:
                pars[key]=value[row]
    elif region_parent_name is not None and exut.get_index_by_column_and_value(data,exdf.synthpops_region_csv_columns["location_code"],region_parent_name) is not None:
        row=exut.get_index_by_column_and_value(data,exdf.synthpops_region_csv_columns["location_code"],region_parent_name)
        for key, value in data.items():
            if key in exdf.synthpops_pars["pop_creator_pars"]:
                pars[key]=value[row]
    elif len(data[exdf.synthpops_region_csv_columns["location_code"]].isin(exdf.global_values))>0:
        row=exut.get_index_by_column_and_value(data,exdf.synthpops_region_csv_columns["location_code"],exdf.global_values)[0] # First occurence of default value
        for key, value in data.items():
            if key in exdf.synthpops_pars["pop_creator_pars"]:
                pars[key]=value[row]
    return pars
    # except:
    #     print(f"There is an error durring parsing synthpops csv input files")
    #     return None


def get_all_synthpops_csv_files(config:dict|str):
    """Get all input csv files

    Args:
        config (dict | str): configuration file or dictionary

    Returns:
        list: list of paths to all input csv files

    """
    config = exut.load_config_dict(config)
    output = list()
    for file_keys in exdf.synthpops_data_files:
        try:
            output.append(exut.get_nested_value_from_dict(dictionary=config,keys=file_keys)) if exut.file_validator(exut.get_nested_value_from_dict(dictionary=config,keys=file_keys)) else None
        except:
            print(f"Cannot find {exut.get_nested_value_from_dict(dictionary=config,keys=file_keys)} in host")
    return output

def get_popsize(config:dict|str, location_code:str, age_distribution_filepath:str):
    """Method for creating list of population sizes.
    filepath (string)                       : filepath to age_distribution file if provided, or load via config path
    """
    config = exut.load_config_dict(config)
    # try:
    data = exut.load_datafile(age_distribution_filepath) if exut.file_validator(age_distribution_filepath) else print(f"There is no valid filepath :{age_distribution_filepath}")
    id=exut.get_index_by_column_and_value(data,exdf.synthpops_region_csv_columns["location_code"],location_code)
    return data[exdf.confkeys["population_size"]][id]

def get_all_data_based_on_input_csv(config:dict|str):
    config = exut.load_config_dict(config)
    data=exut.load_datafile(exut.get_nested_value_from_dict(dictionary=config,
                        keys=exdf.synthpops_global_input_data_confkeys).get(exdf.confkeys["filepath"], None))
    output=[]
    for key, val in data.items():
        if key in ["location_code","code"]:
            continue
        if key in exdf.synthpops_input_files.keys():
                output.append(val[0])
        else:
            pass
    return list(set(output))


# if __name__ == '__main__':
#     config = "/storage/ssd2/sharesim/share-covasim/Tests/new_confs/synthpops.json"
    # test=get_mobility_filepath(config)
    # test = get_parent_location(config, "CZ01")
    # test2 = get_parent_location(config, "CZ02")
    # test3 = get_parent_location(config, "CZ03")
    # test4 = get_parent_location(config)
    # test5=get_region_true(config,"CZ01")
    # test6=get_region_true(config,"CZ02")
    # test7=get_synthpops_csv_files(config)
    # test8=get_region_specific_csv_files(config,"CZ01")
    # test9=get_region_specific_csv_files(config,"CZ02")
    # test10=get_all_regions(config)
    # test11=get_synthpops_parameters(config)
    # test12=get_synthpops_parameters(config,"CZ01")
    # test13=get_synthpops_parameters(config,"CzeChia")
    # test14=get_all_synthpops_csv_files(config)
    # test15=get_popsize(config=config,location_code="CZ01",age_distribution_filepath="/storage/ssd2/sharesim/share-covasim/Tests/data/CZ_NUTS2_population_distrib.xlsx")
    # test16=get_all_data_based_on_input_csv(config)
    # print()
