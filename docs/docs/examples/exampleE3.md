# How to run an abmSHARE simulation 

This chapter contains information about different ways of running an abmSHARE simulation. 

## Geospatial Input Data System

abmSHARE extends the Covasim model in two important dimensions. First, it can simulate the model across user-specified geographic regions. Second, it can import parameters obtained from external data sources. These parameters determine the behavior of the model in one or more user-specified geographic regions. These regional and parametric specification can be imported in a table format using `csv` or `xlsx` files.
Examples of these input files can be seen and downloaded in the [Download](../Downloads.md) section.

**Note:** Do **not** remove non-optional keys from any configuration file or any columns from a csv file from the configuration files. Do **not** rename files. If a file is missing or a column is empty, the model will use default parameters.

## A short testing simulation 
Since the full abmSHARE model is computationally demanding, it is better to try the model on a small scale, testing simulation.
For the test, you can/must turn on one or more modules (set to `true`) with the appropriate configuration files fully configured. Also you have to specify key `test` to `true` in the [Main configuration file](../Extension_settings.md). This test run will generate fixes the size of the population to 20,000 (also with mobility). 

In the `main_configuration.json` file:
```json
"initialize":
    {
        "synthpop_initialize":true,
        "simulation_initialize":true,
        "report_module_initialize":true,
        "test":true
    }
```

## A full scale simulation 
For a full scale simulation turn on the first three modules to `true` with the appropriate configuration files fully configured. The `test` atribute is set to `false` (or can be removed from the configuration file):

In the `main_configuration.json` file:
```json
"initialize":
    {
        "synthpop_initialize":true,
        "simulation_initialize":true,
        "report_module_initialize":true,
        "test":false
    }
```

## Recommended configuration

For the first time, run a synthetic population first or use a pre-generated population from a previous simulation. To use such an existing population, turn the synthetic population module to `false` and use a pre-generated population for next runs of the Simulation module. In this case, when you already have created population objects (more can be found at [T4 Creating population](./exampleE4.md)) you need to specify in the [Simulation region configuration file](./exampleE5.md#region-specific-parameters) values for the key *popfile* which will hold the full path to the pre-generated population file for specific region. Below is an example of the popfile setting in the region configuration file. This configuration is recommended for faster simulation processing (the same population is not generated in each run).

In the `main_configuration.json` file:
```json
"initialize":
    {
        "synthpop_initialize":false,
        "simulation_initialize":true,
        "report_module_initialize":true,
        "test":false
    }
```

**Key "popfile" setting in the Simulation module configuration**

In the following example, in the first two regions, CZ01 and CZ02, the model will use already generated populations. For the other regions, new populations will be crated. 

|location_code|use |region_parent_name|name   |popfile                       |pop_infected|
|-------------|----|------------------|-------|------------------------------|------------|
|CZ01         |true|Czechia           |Region1|/absolute/path/to/popfile0.pop|2           |
|CZ02         |true|Czechia           |Region2|/absolute/path/to/popfile1.pop|0           |
|CZ03         |true|Czechia           |Region3|                              |0           |
|CZ04         |true|Czechia           |Region4|                              |0           |
|CZ05         |true|Czechia           |Region5|                              |2           |
|CZ06         |true|Czechia           |Region6|                              |2           |
|CZ07         |true|Czechia           |Region7|                              |0           |
|CZ08         |true|Czechia           |Region8|                              |0           |


## Simulating only a specific module
You are not limited to use all modules for every run. This approach is useful when you already have generated populations as above in [Recommended configuration](./exampleE3.md#recommended-configuration). Also, you can generate new reports with  [report module](../Report_settings.md) after loading files from an already generated simulation. You can also combine those settings for:

- Only Synthetic population module
- Only Simulation module
- Only Report module
- Combination of Synthetic population module + Simulation module
- Combination of Simulation module + Report module
- Full run of all modules


### Simulating a synthetic population module

For simulating only a synthetic population module, set the value in [Main configuration file](../Extension_settings.md) for the key `synthpop_initialize` to `true` and other keys to `false`. In this particular case, you need to specify the path to the `main_configuration.json` file:
```json
"initialize": {
        "synthpop_initialize": true,
        "simulation_initialize": true,
        "report_module_initialize": true,
        "test":false
    },
    "synthpops_settings": {
        "filepath": "<Path_to_sandbox>/input_data/synthpops_configuration.json"
    }
```

### Simulation module

For running only the Simulation module, in the [Main configuration file](../Extension_settings.md) `simulation_initialize` to `true` and other keys to `false`. Again, the actual path to the configuration file must be provided. As mentioned in [Recommended configuration](./exampleE3.md#recommended-configuration) you can run only this setup or in a combination with report module for a faster process after the population was created and defined in [Simulation module configuration](../Simulation_settings.md).

In the `main_configuration.json` file:
```json
"initialize":
    {
        "synthpop_initialize":false,
        "simulation_initialize":true,
        "report_module_initialize":false,
        "test":false
    },
"simulation_settings":
    {
        "filepath":"<Path_to_sandbox>/input_data/covasim_configuration.json"
    }
```

### To run the report module

You can run the report module for an already completed simulation. Set the value in [Main configuration file](../Extension_settings.md)  of the key `report_module_initialize` to `true` and other keys to `false` with the actual path to the configuration file key `report_settings`.

In the `main_configuration.json` file:
```json
"initialize":
    {
        "synthpop_initialize":false,
        "simulation_initialize":false,
        "report_module_initialize":true,
        "test":false
    },
"report_settings":
    {
        "filepath":"<Path_to_sandbox>/input_data/report_configuration.json"
    }
```
