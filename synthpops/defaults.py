"""Defaults for synthpops files and data types.
"""
import os

import numpy as np
import sciris as sc

default_pop_size = 20000

# specify default valid probability distributions - users can easily supply
# their own list if interested in other properties
valid_probability_distributions = [
    "population_age_distributions",
    "household_size_distribution",
    # 'ltcf_resident_to_staff_ratio_distribution',
    # 'ltcf_num_residents_distribution',
    # 'school_size_distribution',
]

#TODOCZ: change only for czech data as default in future
default_data = {
    "defaults": {
        "country_location": "usa",
        "state_location": "Washington",
        "location": "seattle_metro",
        "sheet_name": "United States of America",
        "nbrackets" : 20,
    }
    ,
    "Czechia": {
        "country_location": "Czechia",
        "state_location": "Czechia_CZ01",
        "location": "CZ01",
        "sheet_name": "Czech Republic",
        "nbrackets" : 20,
    },
}


default_layer_info = dict(
    member_uids=np.array([], dtype=int),
    )


def default_datadir_path(filepath=None):
    """Return the path to synthpops internal data folder."""
    if filepath:
        return filepath
    thisdir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(thisdir, "data")



# available globally if needed or via defaults.py --- stores information about
# location information to search for data when unavailable for the location
# specified or the parent locations specified
settings = sc.objdict()

settings.thisdir = os.path.dirname(os.path.abspath(__file__))
settings.localdatadir = default_datadir_path()
settings.datadir = settings.localdatadir
settings.config_dirpath = None

settings.relative_path = []


settings.max_age = 101
settings.nbrackets = 20
settings.valid_nbracket_ranges = [16, 18, 20]

settings.country_location = None
settings.state_location = None
settings.location = None
settings.sheet_name = None
#Added above original synthpops
settings.region_config=None
settings.parent_config=None


def reset_settings_by_key(key, value):
    """Reset a key in the globally available settings dictionary with a new value.

    Returns:
        None

    """
    settings[key] = value


def reset_settings(new_config):
    """Reset multiple keys in the globally available settings dictionary based on a new
    dictionary of values.

    Args:
        new_config (dict) : a dictionary with new values mapped to keys

    Returns:
        None.

    """
    for key, value in new_config.items():
        if key in settings.keys():
            reset_settings_by_key(key, value)
        else:
            print(f"Key:{key} does not exists in:{settings.keys}")


def reset_default_settings():
    """By default, synthpops uses default settings for Seattle, Washington, USA.
    After having changed the values in the settings dictionary, calling this
    method can easily reset the settings dictionary to the values for Seattle,
    Washington, USA.

    Returns:
        None

    """
    reset_settings(default_data["defaults"]) # pragma: no cover
