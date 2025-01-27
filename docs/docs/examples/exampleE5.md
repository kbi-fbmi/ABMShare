# Creating a Simulation

## How it works
The simulation module is based on the Covasim model developed by the [Institute for Disease Modeling](https://idmod.org/) available at [https://github.com/InstituteforDiseaseModeling/covasim](https://github.com/InstituteforDiseaseModeling/covasim) and extends its functionality without changing the core model. This module is invoked by enabling the option *key:simulation_initialize* in the [Main configuration settings](../Extension_settings.md) and defined by its own configuration settings, which are in detail described at [Simulation module configuration](../Simulation_settings.md). 

**Example configuration and input files for download**

- <a href="/default_confs/simulation_configuration.json" download="simulation_configuration.json">Configuration file for simulation module</a>
- [Global parameters csv file](../downloads/simulation_data/simulation_global_pars.csv)
- [Region parameters csv file](../downloads/simulation_data/simulation_region_pars.csv)
- [Intervention parameters csv file](../downloads/simulation_data/simulation_interventions.csv)
- [Variants parameters csv file](../downloads/simulation_data/simulation_variants.csv)


All possible configurations for this module are in [Simulation module configuration](../Simulation_settings.md).

### Core features
- **Running a simulation**

The main purpose of the abmSHARE model is to run a simulation of the Covasim model across several geographic regions specified in the input data. For example, you can run it in one country (Czechia with 8 NUTS 2 regions) or in Europe with *N* countries. Each region can be defined separately in terms of its own parameters (see [Different parameters](./exampleE5.md#different-parameters)) or all or some regions can share some or all parameters (see [Global parameters](./exampleE5.md#global-parameters)). Also you can combine some of the global parameters and include different parameters for only some regions. Of course, the model allows for a simulation of a single region or one country.
    
- **Mobility**

The abmSHARE model allows for the possibility of allowing a number of agents travelling across regions in multisim. This enables the user to track how the illness is spreading across regions during the simulation. An example of the mobility dataset can be downloaded from a [Download page](../Downloads.md). When the mobility feature is turned on and you want to use a pregenerated synthetic population object, you have to use **pregenerated synthethic population which includes mobility** described in [T4 Creating population](./exampleE4.md) and [Synthetic population module](../Synthetic_pop_settings.md). You cannot run simulation with mobility feature and use pregenerated synthetic population object without the mobility feature.

The mobility feature works such that a number of agents who travel across regions are added to that region where their mobility is specified so that they have connection in both regions. After every simulation step they are synchronized; therefore, they can spread the infection in home region as well as in other region.

- **Interventions**

Interventions represent a feature for defining an intervention into the model at a specific day of simulation. For now there are two ways for defining intervention. They can be defined globally for all regions, or differently for a subset of regions.

One new intervention was introduced based on new mobility feature:

-   You can specify a quarantine for one or more regions by disabling mobility from and to the selected region(s) for a given time period (date from - date to). 

Please see more for interventions in [T5.1 Simulation Interventions](./exampleE5A_1.md).

- **Disease variants**

Variants can be used with the default settings of the simulation module described in [Parameters original simulation variants](../Parameters.md#parameters-for-covasim-variants). Users can redefine and add their own variants according to [T5.3 Simulation - Immunity and variants](./exampleE5B.md).

In multisimulation, a user can include the original Covasim disease variants described in [Parameters original simulation variants](../Parameters.md#parameters-for-covasim-variants) and update its parameters on your own. Variants can be defined globally for each region of the multisimulation or differently for each subset of regions.

Variants must be defined in its own file in the simulation configuration file.

```json 
  "variants": {
    "filepath": "/home/user/sandbox/input_data/simulation_configuration_files/simulation_variants.csv"
  },
```

|location_code|variant|use |label           |days|start_day|end_day|num_days|number_of_imports|rescale|
|-------------|-------|----|----------------|----|---------|-------|--------|-----------------|-------|
|global       |omicron|True|omicron_variant|    |         |       |[5,90]  |100              |       |


## Parameters

You can specify parameters for each simulation separately or define them globally for each region in multisimulation, or combine them. Most parameters are based on the original Covasim model, but also contains some custom parameters. For all parameters see [Simulation parameters](../Parameters.md#parameters-for-simulation). Below is the description how to define parameters globally for all multisimulation or separately for each simulation.

### Global parameters
Parameters can be defined globally. That means you can choose parameters and assign them value to take effect in every region of of the multisimulation. This approach can allow the parameters to be defined conveniently only in one place in [Simulation_settings global parameters](../Simulation_settings.md#global-simulation-parameteres). Please see the detailed description there. For global parameters turn the *key: different_pars value* to `false`.

#### Usage
For defining parameters you have to write them into the *simulation_global_pars.csv* file which is described [here](../Simulation_settings.md#global-parameters). Global parameters takes effect in all regions of the simulation. So it is necessary to share the same `start_day`, number of days to simulate and also you can use other parameters, which are described in [Parameters](../Parameters.md#allowed-parameters-for-global-settings). Also you can specify various other parameters, which are available for the **Parameters for Simulation** in [Parameters](../Parameters.md#parameters-for-simulation), but be carefull with the parameters which are location specific.


**Definition of parameters in the configuration file**

```json
...
"global_parameters":
{
    "filepath":"/<Path_to_sandbox>/input_data/data/simulation/simulation_global_pars.csv"
}
...
```

**Definition of global parameters in a `.csv` file saved in the file path in *global_parameters***

|n_days|start_day|use_waning|unique_mobility_indexes|
|------|---------|----------|-----------------------|
|90    |2020-01-1|true      |True                   |



### Region-specific parameters
You can define region-specific parameters along with global parameters. In this case, parameters can be specified differently for each region *key:pars* section. Also region specific input file has few necessary keys to describe simulation.

**How to define input `csv`/`xlsx` file in the simulation configuration**
```json
{
    "region_parameters":
    {
        "filepath":"/<Path_to_sandbox>/input_data/data/simulation/simulation_region_pars.csv"
    },
}
```

|location_code|use |region_parent_name|name   |popfile|pop_infected|
|-------------|----|------------------|-------|-------|------------|
|CZ01         |true|Czechia           |Region1|       |2           |
|CZ02         |true|Czechia           |Region2|       |0           |
|CZ03         |true|Czechia           |Region3|       |0           |
|CZ04         |true|Czechia           |Region4|       |0           |
|CZ05         |true|Czechia           |Region5|       |2           |
|CZ06         |true|Czechia           |Region6|       |2           |
|CZ07         |true|Czechia           |Region7|       |0           |
|CZ08         |true|Czechia           |Region8|       |0           |

As you can see, this regions has only `pop_infected` parameter as the additional parameter, which will be also combined with global parameters defined in the global parameters file.
Note: This approach is the most effective because most often there will be only a few region-specific parameters.

**Note: If some parameters are outside their valid range, a warning is issued. Always check the [parameters section](../Parameters.md)**


## How to run a simulation 
As explained in [T3 Running a simulation](./exampleE3.md), you can run an abmSHARE simulation with all combinations described in T3. 
It is also recommended to enable *key:parallel_run* to take advantages of parallel population object loading.

### Complex run with a synthetic population
A [full run](./exampleE3.md#full-run) simulation of all modules automatically loads newly created synthetic population object in multisimulation. 

### Complex run without synthetic population run
To use the already created synthetic population objects, turn off synthetic population module as in [Recommended combination](./exampleE3.md#recommended-combination). In this case, a path to the population objects for each region must be specified in *key:popfile*.



