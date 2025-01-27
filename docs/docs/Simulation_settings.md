# Simulation module configuration

There is a list of possible parameters for file `simulation_configuration.json` responsible for creating simulation of defined regions. Example of the configuration file can be found below and is also for download <a href="../default_confs/simulation_configuration.json" download="simulation_configuration.json"> here</a>.
## Settings for running a simulation
- parallel_run: **(bool)**  - to enable a parallel simulation that will use as many cores as many sims are defined. Used to load population and initialize simulation much faster.
- test: **(bool)** **OPTIONAL**- to enable running the simulation in test mode. It will override test settings both for population size and population type also with mobility.

## Region parameters
Input `csv` file responsible for selecting regions to be included in the simulation. There can be multiple regions defined, but it really depends on the *true* value of each row. 

Recommended keys are:
- location_code
- use
- region_parent_name
- pop_infected

** Other allowed parameters are described [here](./Parameters.md#simulation-parameters)**
Example file for download available <a href="./downloads/simulation_data/simulation_region_pars.csv" download="simulation_region_pars.csv"> here</a>.

Example of `csv`/`xlsx` file structure:

|location_code|use |region_parent_name|name   |popfile                       |pop_infected|
|-------------|----|------------------|-------|------------------------------|------------|
|CZ01         |true|Czechia           |Region1|/absolute/path/to/popfile0.pop|2           |
|CZ02         |true|Czechia           |Region2|/absolute/path/to/popfile1.pop|0           |
|CZ03         |true|Czechia           |Region3|                              |0           |

## Global parameters
Input `csv` file responsible for defining global parameters for simulation. There can be only one row defined that will be used for all regions.
Global parameters can also be defined inside configuration file. In case of same key are defined in both the `csv` and the configuration file, the **`csv` file has priority**. 

Recommended keys are [here](./Parameters.md#allowed-parameters-for-global-settings)
Example file for download is available <a href="./downloads/simulation_data/simulation_global_pars.csv" download="simulation_global_pars.csv"> here</a>.

Example `csv`/`xlsx` file structure:

|n_days|start_day|use_waning|unique_mobility_indexes|
|------|---------|----------|-----------------------|
|90    |2020-01-1|true      |True                   |

## Interventions
Input `csv` file responsible for defining policy interventions during the simulation. There can be multiple interventions depending on the *true* value of each row.
More info about intervention can be found [here](./examples/exampleE5A_1.md) and [here](./examples/exampleE5A_2.md).
Example file for download available <a href="./downloads/simulation_data/simulation_interventions.csv" download="simulation_interventions.csv"> here</a>.

# Example configuration `json`
```json
{
    "parallel_run": true,
    "region_parameters":
    {
        "filepath":"<Path_to_sandbox>/input_data/simulation_configuration_files/simulation_region_pars.csv"
    },
    "interventions":
    {
        "filepath":"<Path_to_sandbox>/input_data/simulation_configuration_files/simulation_interventions.csv"
    },
    "variants":
    {
        "filepath":""
    },
    "mobility":
    {
        "value":true,
        "filepath":"<Path_to_sandbox>/input_data/simulation_configuration_files/NUTS2_mobility_data.csv"
    },
    "population_size":
    {
        "filepath":"<Path_to_sandbox>/input_data/data/population_age_distributions.csv"
    },
    "global_parameters":
    {
        "filepath":"<Path_to_sandbox>/input_data/simulation_configuration_files/simulation_global_pars.csv"
    }
}
```
