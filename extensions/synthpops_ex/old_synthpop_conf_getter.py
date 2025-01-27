import extensions.utils as exut
import extensions.defaults as exdf

# This utils script is for getting selected values from configuration

def get_mobility_filepath(config:dict|str):
    """Get mobility filepath
    Args:
        conf (dict): synthpops configuration
    
    Returns:
        str/none: path to mobility file, or None
    """
    config=exut.load_config_dict(config)
    output=config.get(exdf.confkeys['mobility_path'],None)
    if output != "" and not None:
        return output
    return None

def get_parent_location(config:dict|str):
    """Get parent json location file

    Args:
        conf (dict): synthpops configuration

    Returns:
        str/none: path to parent json config, or None
    """
    config=exut.load_config_dict(config)
    output=config.get(exdf.confkeys['pop_creator_config'],None).get(exdf.confkeys['pops'],None).get(exdf.confkeys['parent_location'],None)
    if output!="" and not None:
        return output
    return None

def get_pop_creator_configs(config:dict|str): #pop_location
    """Get pop_location .json files

    Args:
        conf (dict): synthpops configuration

    Returns:
        list: list of paths pop_locations or None
    """
    config=exut.load_config_dict(config)
    output=config.get(exdf.confkeys['pop_creator_config'],None).get(exdf.confkeys['pops'],None).get(exdf.confkeys['pop_location'],None)
    if (output!="" and not None) and all(output):
        return output
    return None

def get_synthpops_csv_files(config:dict|str):
    """Get synthpops csv files

    Args:
        conf (dict): synthpops configuration

    Returns:
        list: list of paths synthpops csv files
    """
    config=exut.load_config_dict(config)
    output=list()
    for name in exdf.synthpops_csv_files:
        if config.get(name,False):
            output.append(config[name].get(exdf.confkeys['filepath']))
    return output

def get_region_specific_csv_files(config:dict|str):
    """Get region specific csv files

    Args:
        conf (dict): synthpops configuration

    Returns:
        list: list of paths region specific csv files
    """
    config=exut.load_config_dict(config)
    output=list()
    for region in config[exdf.confkeys['region_config']][exdf.confkeys['regions']]:
        for name in exdf.synthpops_one_file_data:
            if region.get(name,False):
                output.append(region[name].get(exdf.confkeys['filepath']))
    return output
   
getters=[get_mobility_filepath,get_parent_location,get_pop_creator_configs,get_synthpops_csv_files]

def get_all_synthpops_files(config:dict|str):
    """Get all files from the functions above

    Args:
        conf (_type_): synthpops configuration

    Returns:
        list: list of paths to all synthpops files
    """
    config=exut.load_config_dict(config)
    return [getter(config) for getter in getters if getter(config) is not None]



# if __name__=='__main__':
#     test=get_region_specific_csv_files("/storage/ssd2/sharesim/share-covasim/Tests/data/test_synthpops_configuration.json")
#     print()