# Settings for Synthetic population module

There is a list of possible parameters for configuration file **synthpops_configuration.json** responsible for creating the synthetic population as the input for the simulation module. An example of configuration file is below. It can also be downloaded <a href="../default_confs/synthpops_configuration.json" download="synthpops_configuration.json"> here</a>.

## Simulation settings
The simulation run parameters define how the resulting population objects will be named and created. 

- test *(bool)* **Options - true,  false** - **OPTIONAL PARAMATER** only for debugging purposes. It sets the maximum size of population to 20,000 agents. If mobility is enabled, it adds 200 more people to the population based on the number of regions.
- parallel_run *(bool)* **Options - true,  false** - to run more efficient generation of population objects. It will use one core per region and it is significantly faster than a single-core simulation. **Note: it is recommended to have RAM available at approximately 1 agent= 10kB**

# Population creation settings
These options define input data and parameters for population creation.

## Pop output naming *(dict)*
- value *(bool)* **Options - true,  false** - to change the name of population object, set it to `true` and define the prefix and suffix of the name.
- pop_name_prefix *(str)* **Options - any string** - prefix of the population object name. **Note: Optional**
- pop_name_suffix *(str)* **Options - any string** - suffix of the population object name. **Note: Optional**
- pop_output_type *(str)* **Options - obj/json** - type of the population object to be created. **Note: Obj is much faster and recommended way**
- pop_output_dirpath *(str)* **Options - any string** - path to the directory where population object will be saved. **Note: not needed when autosave_settings enabled**

## Parameters *(pars_file.csv)*
Parameters for defining region parameters. 
It can be defined as default option, specified by `location_code` or `region_parent_name`. Example: 'default', 'Czechia', 'CZ01'. **NOTE: it is not case sensitive**

Example file for parameters can be found [here](../downloads/synthpops_data/pars_file.csv). 

Necessary parameters are: **location_code,  household_method,  smooth_ages**. 

Also you can define optional parameters: 
*max_contacts, ltcf_pars, shool_pars, with_industry_code, with_facilities, 
use_two_group_reduction, average_ltcf_degree, with_school_types, school_mixing_type, 
average_class_size, inter_grade_mixing, average_student_teacher_ratio, 
average_teacher_teacher_degree, teacher_age_min, teacher_age_max, 
with_non_teaching_staff, average_student_all_staff_ratio, average_additional_staff_degree, 
staff_age_min, staff_age_max, rand_seed, sheet_name, household_method, 
smooth_ages, household_method, windows_length.*

More info about those additional parameters you can find at the official [Synthpops documentation](https://docs.idmod.org/projects/synthpops)

- filepath *(str)* **Options - any string** - path to the parameters file for population creation. **Note: Necessary**

File structure with different location codes:

| location | household_method | smooth_ages |
|----------|------------------|-------------|
| Czechia  | fixed_ages       | 1           |
| Default  | fixed_ages       | 1           |
| CZ01     | fixed_ages       | 1           |


## Population region creator *(synthpops_region.csv)*

This file is responsible for defining main region characteristics used for population creation. 
It is location code oriented and it uses various input data for each region. 
An example file can be found [here](../downloads/synthpops_data/synthpops_region.csv).

Necessary columns are:

- location_code *(str)* **Options - any string** - location code of the region used for population creation. For example 'CZ01' **Note: Necessary**
- use default *(bool)* **Options - true,  false** - to use default parameters for population creation. **Note: Necessary,  it also provides and option to hold multiple regions,  but to create only a selected ones**
- region_name *(str)* **Options - any string** - name of the region used for population creation. For example 'Czechia_CZ01' **Note: Necessary**
- untrimmed_name *(str)* **Options - any string** - name of the region used for population creation. For example 'Hlavní město Praha' or 'Capital city Prague' **Note: Necessary**
- sheet_name *(str)* **Options - any string** - name of the sheet in the input file used for population creation. For example 'Czech Republic' **Note: Necessary and those codes are based on contact matrices,  which you can find [here](./synthpops_data/MUestimates_all_locations_1.xlsx) and [here the part 2](./synthpops_data/MUestimates_all_locations_2.xlsx).**
- region_parent_name *(str)* **Options - any string** - name of the parent region used for population creation. For example 'Czechia' **Note: Necessary**
- notes *(str)* **Options - any string** - notes for the region used for population creation. For example 'Capital city' **Note: Optional**
- parent_dirpath *(str)* **Options - any string** - path to the parent directory used for population creation. For example 'CZ01' **Note: Optional**
- parent_filename *(str)* **Options - any string** - name of the parent file used for population creation based on parent_dirpath. For example 'CZ01' **Note: Optional**
- parent_filepath *(str)* **Options - any string** - path to the parent file used for population creation. For example 'CZ01' **Note: Optional**

**Note: It is recommended to provide a full path to the parent file, instead of using parent_dirpath and parent_filename.**

**Note: Parent configuration file is necessary - you can use a default file that can be downloaded [here](./synthpops_data/Czechia.json) and rename it to your needs. It is used to define all input data if specific input data you can find [at synthpops input data](./examples/exampleE4_1.md) are not provided. The best approach is to define a filepath to the file but you can also define a `parent_dirpath` which has multiple parent files and then specify the name of the file in `parent_filename`. The model will calculate and select the file which fits your defined requirements.**

File structure with different location codes:

| location_code | use  | region_name  | ... | parent_dirpath           | parent_filename | parent_filepath        |
|---------------|------|--------------|-----|--------------------------|-----------------|------------------------|
| CZ01          | true | Czechia_CZ01 | ... |                          |                 | path_to/Czechia.json |
| CZ02          | true | Czechia_CZ02 | ... |   path_to_parent_dirpath | Czechia         |                        |


### Input data global *(dict)*
This file is responsible for defining additional input data for population creation. It is location code oriented and it uses various input data for each region. Example file can be found [here](../downloads/synthpops_data/synthpops_input_files.csv). It can be defined globally or separately for location codes as: 'Default', Czechia' or 'CZ01'.

More information about these data can be found [here](./examples/exampleE4_1.md) and downloaded [as zip file here](./downloads/synthpops_additional_input_data.zip).

The only necessary file is [age distribution file](./examples/exampleE4_1.md#age-distribution-file).

File structure with different location codes:

| location_code | population_age_distribution | ... | enrollment_rates_by_age | ... |
|---------------|-----------------------------|-----|-------------------------|-----|
| CZ01          |   path_to_file              | ... |   path_to_file          | ... |
| Czechia       |   path_to_file              | ... |   path_to_file          | ... |

### Mobility data *(dict)*

This file is responsible for defining mobility data for population creation. It is location code oriented and it uses various input data for each region. Example file can be downloaded [here](../downloads/synthpops_data/NUTS2_mobility_data.csv). Another description can be found [here](./examples/exampleE4_1.md#mobility-data). **Note: mobility data are OPTIONAL**

File structure can be found [here](./examples/exampleE4_1.md#mobility-data).
```json
{
    "test":true, 
    "parallel_run":true,  
    "pop_creator_settings":{
        "pop_output_naming":
        {
            "value":true, 
            "pop_name_prefix":"", 
            "pop_name_suffix":"", 
            "pop_output_type":"obj", 
            "pop_output_dirpath":"", 
            "pop_creator_dirpath":""
        }, 
        "parameters":
        {
            "filepath":"<Path_to_sandbox>/sandbox/input_data/data/pars_file.csv"
        },      
        "pop_creator":
        {
            "pop_creator_file":
            {
                "value":true, 
                "filepath":"<Path_to_sandbox>/sandbox/input_data/data/synthpops_region.csv"
            }, 
            "input_data_global":
            {
                "value":true, 
                "filepath":"<Path_to_sandbox>/sandbox/input_data/data/synthpops_input_files.csv",
                "mobility_data":
                    {
                        "value":true, 
                        "filepath":"<Path_to_sandbox>/sandbox/input_data/data/NUTS2_mobility_data.csv"
                    }                                   
            }
        }
    }            
}

```
