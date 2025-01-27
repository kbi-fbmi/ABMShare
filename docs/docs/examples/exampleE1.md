# Installation and Remote Access

## Installation at your desktop computer


## Connection to server and sandbox folder structure

To run abmSHARE remotely, you will need a login and a password. Please contact the administrators for access and support.

1. In a terminal window, login to the server via ssh.
2. Locate sandbox in your home directory: `/home/"username"/sandbox`
3. The sandbox folder contains all necessary files for running abmSHARE. Default configuration can be modified in several configuration and parameter files. Several examples are presented in the [Tutorial](./exampleE3.md). 
4. For any specification, run the model by typing `./start.sh`
5. All results are stored in the output folder `sandbox/outputs`

## The sandbox folder
The sandbox folder contains all the necessary files for running abmSHARE. The folder is updated for all users after each system update. Previous version of the system are stored with the system update date appended as `sandbox_[date]`. The sandbox folder always contains the updated settings. Please check new/old keys in new and old configuration files for possible changes. Changes are documented in the [Changelog page](../ChangeLog.md).

### Structure of the sandbox folder
```tree
sandbox
    |   
    +-- input_data
    |   +-- data
        |   +-- Czechia.json
        |   +-- NUTS2_mobility_data.csv
        |   +-- population_age_distribution.csv
    |   +-- simulation_configuration_files
        |   +-- simulation_interventions.csv
        |   +-- simulation_global_pars.csv
        |   +-- simulation_region_pars.csv
        |   +-- simulation_vacciness.csv
        |   +-- simulation_variants.csv
    |   +-- simulation_immunity_files
        |   +-- immunity_input_files.csv
        |   +-- vaccine_dose_pars.csv
        |   +-- vaccine_variant_pars.csv
        |   +-- variants_cross_immunity.csv
        |   +-- variants_pars.csv
    |   +-- synthpops_configuration_files
        |   +-- pars_file.csv
        |   +-- synthpops_input_files.csv
        |   +-- synthpops_region.csv
    |   +-- synthpops_input_data
        |   +-- Various files in here        
    |   +-- main_configuration.json
    |   +-- report_configuration.json
    |   +-- main_configuration.json
    |   +-- simulation_configuration.json
    |   +-- synthpops_configuration.json
    +-- logs
    +-- outputs
        | 
    +-- parameters.py
    +-- results.sh
    +-- start.sh
```
### Input data folder

This folder contains all configuration files for each module as well as all input data needed for the abmSHARE model to run.
These inputs are defined in `json` and/or `csv` files.

#### Configuration files 

-  `main_configuration.json` file contains all important parameters for all other modules. More information can be found <a href="../../Extension_settings">here</a>.
-  `synthpops_configuration.json` file is the synthetic population module configuration file responsible for creating synthetic populations that can serve as inputs into the abmSHARE model. More information can be found <a href="../../Synthetic_pop_settings">here</a>.
-  `simulation_configuration.json` file defines the main features of the simulation. It can specify the population created by synthetic population model. More information about settings of this module can be found <a href="../../Simulation_settings">here</a>.
-  `report_configuration.json` file creates outputs of each simulation in csv format as well as a summary of the simulation. More information about this module can be found <a href="../../Report_settings">here</a>.
- Other files are available at [download page](../Downloads.md).

#### Data folder
> **Folder name:** *data* <br>
> This folder contains three files by default, which can be shared across simulation and synthetic population module.

- `Czechia.json` contains the geographic data for Czechia. It is used for creating synthetic populations and for running simulations.
- `NUTS2_mobility_data.csv` contains the mobility data for Czechia. It is used for creating synthetic populations and for running simulations.
- `population_age_distribution.csv` contains the age distribution data for Czechia. It is used for creating synthetic populations and for running simulations.

#### Simulation configuration files folder
> **Folder name:** *simulation_configuration_files*<br>
> These files are used for defining the simulation parameters. They are used in the simulation module. More info about thouse files you can find [T5 Simulation](./exampleE5.md).

- `simulation_interventions.csv` contains the interventions for the simulation. It is used for defining interventions in the simulation module.
- `simulation_global_pars.csv` contains the global parameters for the simulation. It is used for defining global parameters in the simulation module.
- `simulation_region_pars.csv` contains the region-specific parameters for the simulation. It is used for defining region-specific parameters in the simulation module.
- `simulation_vaccines.csv` contains the vaccine parameters for the simulation. It is used for defining vaccine parameters in the simulation module.
- `simulation_variants.csv` contains the variant parameters for the simulation. It is used for defining variant parameters in the simulation module.

#### Simulation immunity files folder
> **Folder name:** *simulation_immunity_files*<br>
> These files are used for defining the immunity parameters. They are used in the simulation module. More info about thouse files you can find [T5.3 Simulation - Immunity and variants](./exampleE5B.md).

- `immunity_input_files.csv` contains the input files for the immunity. It is used for defining the input files in the immunity module.
- `vaccine_dose_pars.csv` contains the vaccine dose parameters for the immunity. It is used for defining the vaccine dose parameters in the immunity module.
- `vaccine_variant_pars.csv` contains the vaccine variant parameters for the immunity. It is used for defining the vaccine variant parameters in the immunity module.
- `variants_cross_immunity.csv` contains the cross-immunity parameters for the immunity. It is used for defining the cross-immunity parameters in the immunity module.
- `variants_pars.csv` contains the variant parameters for the immunity. It is used for defining the variant parameters in the immunity module.

#### Synthetic population configuration files folder
> **Folder name:** *synthpops_configuration_files*<br>
> These files are used for defining the synthetic population parameters. They are used in the synthetic population module. More info about thouse files you can find [Synthetic popilation configuration file](../Synthetic_pop_settings.md) and on [T4 Creating population](./exampleE4.md).

- `pars_file.csv` contains the parameters for the synthetic population. It is used for defining the parameters in the synthetic population module.
- `synthpops_input_files.csv` contains the input files for the synthetic population. It is used for defining the input files in the synthetic population module.
- `synthpops_region.csv` contains the region-specific parameters for the synthetic population. It is used for defining the region-specific parameters in the synthetic population module.

#### Synthetic population other specific input data folder
> **Folder name:** *synthpops_input_data*<br>
> These files are used for defining more specific parameters for synthetic population creator. More info about thouse files you can find on [T4.1 Population input data](./exampleE4_1.md).


### Outputs folder

This folder contains several outputs from a simulation. The `outputs` folder can be set as a default folder in <a href="../../Extension_settings#Auto save settings">Auto save settings</a>, or it can be used for manually saved outputs defined in various configuration files. Each simulation output is saved to a new folder with a time stamp in the folder name `(YY_mm_DD_HH_MM)`
```tree
    |
    +-- outputs
        |   +-- Output_2023_01_31_24_00
            |   +-- Configuration   
            |   +-- output_reports
            |   +-- pop_configurations
            |   +-- pops
            |   +-- sims
```
Each simulation result folder has its own subdirectories:

- `Configuration` holds all input configuration files used for the simulation.
- `output_reports` contains all generated `csv` and `xlsx` outputs defined in the [Report module](../Report_settings.md).
- `pop_configuration` contains configuration files used as inputs in the [Synthetic population module](../Synthetic_pop_settings.md) for creating population.
- `pops` holds all generated population objects from [Synthetic population module](../Synthetic_pop_settings.md#settings-for-population-creator). These can be used in [Simulation module](../Simulation_settings.md) as *popfile* key.
- `sims` saves instances of simulations for later analysis and exploration. These are `covasim.MultiSim()` objects.

### Other individual files 

#### Start file
*(file: start.sh)*

After editing all configuration files, a abmSHARE simulation is started by typing `./start.sh` in the command line. It is important to be in the located (`cd`) in the sandbox directory or to insert an absolute path for the `start.sh` file. 
If you want to validate the input configuration for the model, run `./start.sh -v`. The validation process will check for correct input data types and file paths.

#### Start file for grid computing
*(file: meta_start.sh)*

For large-scale simulations, the abmSHARE can be run on a grid, using 
`./start_meta.sh` in the command line, again in the appropriate sandbox directory or by using an absolute path. Input configuration and paths can be validated by 
Input configuration and paths can be validated by `./start_meta -v true`. 

There is also an option to specify a different main configuration file by typing `./start_meta.sh -c <path_to_main_config_file>`. In the validation mode, 
use the flag as `./start_meta.sh -c <path_to_main_config_file> -v true`.

Input and output data for grid computing are stored in `/home/<username>/sandbox/meta`.
Outputs files are automatically downloaded every 30 min from remote computing server.

**NOTE** In case the server asks for a password or gives an error message, type `source ~/.profile`. If the problem persists, please contact the administrator.


