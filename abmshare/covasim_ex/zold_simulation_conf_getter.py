import abmshare.utils as exut
import abmshare.defaults as exdf
import numpy as np

def get_popfiles(config:str|dict):
    """Get population files from configuration

    Args:
        conf (str/dict): configuration
    Returns:
        list: list of population files paths
    """
    config=exut.load_config_dict(config)
    return [pop.get(exdf.confkeys['simulation_pars']).get(exdf.confkeys['popfile']) for pop in config.get(exdf.confkeys['different_pars']).get(exdf.confkeys['regions'])]

def get_mobility_filepath(config:dict|str):
    """Get mobility file filepath

    Args:
        conf (dict | str): configuration

    Returns:
        str | None: path to mobility, if exists
    """
    config=exut.load_config_dict(config)
    return config.get(exdf.simulation_files_keys['mobility'],None).get(exdf.confkeys['filepath'],None) if config.get(exdf.simulation_files_keys['mobility'],None).get('value',None) else None


def get_population_filepath(config:dict|str):
    """Get population file filepath

    Args:
        conf (dict | str): configuration

    Returns:
        str | None: path to population file, if exists
    """
    config=exut.load_config_dict(config)
    return config.get(exdf.simulation_files_keys['population'],None).get(exdf.confkeys['filepath'],None) if config.get(exdf.simulation_files_keys['population'],None).get('value',None) else None
    

def get_number_of_regions(config:dict|str):
    """Get number of regions

    Args:
        conf (dict | str): configuration

    Returns:
        int: number of regions
    """
    config=exut.load_config_dict(config)
    return len(config.get(exdf.confkeys['different_pars'],None).get(exdf.confkeys['regions'],None))

def get_num_of_population(config:dict|str):
    """Get number of population files

    Args:
        conf (dict | str): configuration

    Returns:
        int: number of population files
    """
    config=exut.load_config_dict(config)
    array=np.array((exut.load_datafile(config[exdf.confkeys['population_pars']]['filepath'])).population,dtype=np.int32)
    return np.sum(array)


getters=[get_mobility_filepath,get_population_filepath,get_popfiles,get_number_of_regions,get_num_of_population]

# def get_all_synthpops_files(conf:dict|str):
def get_all_simulation_files(config:dict|str):
    """Get all files from the simulation files functions above

    Args:
        conf (dict): configuration

    Returns:
        list: list of files
    """
    output=list()
    config=exut.load_config_dict(config)
    for getter in getters:
        output.append(getter(config))
    return output

