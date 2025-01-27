# Creating a Population 

The Synthetic population module is based on [IDM SynthPops](https://docs.idmod.org/projects/synthpops/) available at [Synthpops](https://github.com/InstituteforDiseaseModeling/synthpops), and extends its functionality. There are two submodules responsible for creating population objects usable in the abmSHARE model. Because the population creation process is computationally demanding, there is an option for a parallel run in which each population is created in a separate CPU core.

All possible configurations are described in the [Synthetic population configuration file](../Synthetic_pop_settings.md).

## Input data
For creating a synthetic population there are two main input data sections. First one is for creating a population based on the necessary input arguments. The second is for creating a more specific population based on additional input data that can reflect region specific population distributions across multiple parameters.

### Basic input data for creating synthetic population
Basic input data consist of 

- `pars_file.csv` contains the parameters for the synthetic population. It is used for defining the parameters in the synthetic population module. The file can be downloaded [here](../downloads/synthpops_data/pars_file.csv).
- `synthpops_input_files.csv` contains the input files for the synthetic population. It is used for defining the input files in the synthetic population module. The file can be downloaded [here](../downloads/synthpops_data/synthpops_input_files.csv).
- `synthpops_region.csv` contains the region-specific parameters for the synthetic population. It is used for defining the region-specific parameters in the synthetic population module. The file can be downloaded [here](../downloads/synthpops_data/synthpops_region.csv).

#### Parameters file (pars_file.csv)
Parameters file is a `csv` file that contains the parameters for the synthetic population. It is used for defining the parameters in the synthetic population module

All possible input data are described in the [Synthetic population configuration file](../Synthetic_pop_settings.md). Basically it needs the main `.csv` or `.xlsx` configuration file *synthpops_configuration* file. This files can further contain links to four other parameter files that are described in [Synthetic population input_data](./exampleE4_1.md#input-data-for-creating-synthetic-population).

More info about it can be found in [Synthetic population configuration file](../Synthetic_pop_settings.md#pop-creator-settings).

Example file structure

| location | household_method | smooth_ages |
|----------|------------------|-------------|
| Czechia  | fixed_ages       | 1           |
| Default  | fixed_ages       | 1           |
| CZ01     | fixed_ages       | 1           |

#### Region pattern file (synthpops_region.csv)
Region pattern file is a csv file that contains the region-specific parameters for the synthetic population. It is used for defining the region-specific parameters in the synthetic population module and enabling regions to be created.

All possible input data are described [Synthetic population configuration file](../Synthetic_pop_settings.md). Basically it needs the main .csv or .xlsx configuration file *synthpops_region* file. This files can further contain links to four other parameter files that are described in [Synthetic population input_data](./exampleE4_1.md#input-data-for-creating-synthetic-population).

More info about it can be found in [Synthetic population configuration file](../Synthetic_pop_settings.md#population-region-creator-synthpops_regioncsv).

Example file structure

| location_code | use  | region_name  | ... | parent_dirpath           | parent_filename | parent_filepath        |
|---------------|------|--------------|-----|--------------------------|-----------------|------------------------|
| CZ01          | true | Czechia_CZ01 | ... |                          |                 | path_to/Czechia.json |
| CZ02          | true | Czechia_CZ02 | ... |   path_to_parent_dirpath | Czechia         |                        |

### Additional input data for creating synthetic population
Additional input data can be used to specify various attributes such as age distribution, employment rate, enrollment rate, school distributions etc.

Those data can be on the global level (specified by `region_parent_name` or default) or on the region level (specified by `location_code`). If there is a region specific data, it will be used instead of the global data. If there is no region specific data, the global data will be used. **Age distribution file is necessary for creating a synthetic population, otherwise you can specify number of agents in pars_file.csv**

For this approach there is a chapter [T4.1 Population input data](./exampleE4_1.md) which describes all possible input data for creating synthetic population.


### Population creation
Population creation works in two steps. First one is responsible for creating region pattern configuration file and the other one is creating population object based on this region pattern file and based on additional parameters. There are several option to define parameters (in detail its explained in [Synthetic pop settings](../Synthetic_pop_settings.md#settings-for-population-creator)). As its mentioned in section above - if there is any new data for integrating into population creation, they will take effect only when population is re-created with those new input data. Output populations are by default saved as the '*.pop' files, which are used in simulation module.

### Parallel simulation 
There is a option to run this module in sequence or in parallel, which can utilize more than one CPU core and improve the performance. 

### Full-scale simulation 
Full run needs to have defined a csv/xlsx files in [Synthetic pop settings](../Synthetic_pop_settings.md). Those files are available to download here:

- [Synthetic population base region info](../downloads/synthpops_data/synthpops_region.csv)
- [Synthetic population parameters file](../downloads/synthpops_data/pars_file.csv)
- [Synthetic population aditional input files description file](../downloads/synthpops_data/synthpops_input_files.csv)
- [Synthetic population adfitional input files in zip](../downloads/synthpops_additional_input_data.zip)
