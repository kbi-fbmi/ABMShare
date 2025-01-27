# Interventions

For defining special interaction in simulation such as contact tracing, testing agents, or region lockdowns, you can use Covasim interventions. Intervention can be stacked, so there can be the same intervention defined several times with different parameters such as different start day of the intervention, changes across layers affected by the intervention, or other different values related to a specific intervention. More information about interventions can be found in [T5.2 Simulation - Intervention types](./exampleE5A_2.md).

As other simulation parameters, an intervention can be defined in several ways: globally for all regions, for each region of the same `region_parent_name` (for example, *Czechia*), or separately for each region of the simulation. 

**Note: Some interventions are dependent on a different intervention as mentioned in their description**

Interventions are defined in `*.csv` or `*.xlsx` file, which contains the correct attributes (columns) for each intervention and valid data. You can define multiple interventions and turn them on/off by *key:use* in the file. It can be also defined as global/state or it can be region-specific.

**Interventions are defined in [Simulation intervention file](../downloads/simulation_data/simulation_interventions.csv)**.

## How to define an intervention

Specific interventions with basic information and requirements are available in [T5.2 Simulation - Intervention types](./exampleE5A_2.md#intervention-types) section.
The core element is to have a proper `csv`/`xlsx` file with correctly defined attributes. Necessary attributes for each intervention are:

- **location_code** *(str)*  related to region/country or global (states are based on *key:region_parent_name* which is defined in [Region specific parameters](./exampleE5.md#region-specific-parameters))
- **use** *(bool)*  `true` for an intervention, `false` if it is to be ignored 
- **label** *(str)* for the intervention, user defined
- **intervention_type** *(str)* such as `mobility_change`, `beta_change` etc. described in [Intervention types](./exampleE5A_2.md#intervention-types)

**An example of intervention attributes:**

|location_code|use  |label      |intervention_type|start_day |num_days|end_day   |beta_change|
|-------------|-----|-----------|-----------------|----------|--------|----------|-----------|
|CZ01         |true |mob_change |mobility_change  |2020-03-01|        |2020-05-19|           |
|Czechia      |false|mob_change |mobility_change  |          |[10,25] |          |           |
|global       |true |beta_change|mobility_change  |          |[10,25] |          |"[0.5]"    |

## Intervention timeline settings

For the most user-friendly experience there is a complex method that calculates the correct timeline of the intervention.
You can supply information about starting/ending time of intervention in two ways:

- Format for date time is in "YYYY-MM-DD" format
- Format for number of days (takes effect from the start date of the simulation) is integer.

You can combine starting and ending definitions like in the example for a simulation defined in `simulation_global_pars` file:

- **start_day** : "2020-01-01", **end_day** : "2020-01-25"
- **start_day** : 10, **end_day** : 25
- **start_day** : "2020-01-01", **num_days** : 25|"[25]"
- **num_days** : "[1,25]"
- **start_day** : 1, **num_days** : "2020-01-25"
- **num_days** : 1|"[10]". **end_day** : "2020-01-25"

Examples above are all possible combination for calculating the exact same timeline of intervention, which will be from 2020-01-01 to 2020-01-25.

## Settings for beta interventions 

Beta changes in specific intervention can be set as a list of values, or as a single value. 
When single value is used, it can be used for whole intervention period, or defined as the starting point for the whole simulation period.
When list of values is used, it must be the same length as the number of days of intervention. 

**Examples:**

- **beta_change** : 0.7, start_day : *defined*, end_day : *defined* 
<br>-> beta will be 0.7 since start day of intervention period, after end day, it returns to 1
- **beta_change** : 0.7, start_day : *defined*, end_day : *not defined* 
<br>-> beta will be 0.7 since start day of intervention period for the rest of simulation period
- **beta_change** : [0.7,0.9], start_day : *defined*, end_day : *defined* 
<br>-> beta will be 0.7 since start day of **intervention** period, after that it will be 0.9 for the rest of intervention period, after end day, it returns to 1
- **beta_change** : [0.7,0.9], start_day : *not defined*, end_day : *defined* 
<br>-> beta will be 0.7 since start day of **simulation**, after end day it will be set to 0.9 for the rest of simulation period

## Definition of intervention region 

There are three ways to define intervention in specific regions.
Also you can defined multiple intervention, and enable only a selected ones by explicitly setting the *use* parameter to *true/false*:

Example for a region defined in `csv`:

|location_code|use  |region_parent_name|name   |popfile                       |pop_infected|
|-------------|-----|------------------|-------|------------------------------|------------|
|CZ01         |true |Czechia           |Region1|/absolute/path/to/popfile0.pop|2           |

Example for a region defined by `location_code`:

|location_code|use  |
|-------------|-----|
|CZ01         |true |

Example for an intervention to all regions enabled in the simulation:

|location_code|use  |
|-------------|-----|
|global       |true |

Example for regions defined by the *region_parent_name* in the main region `csv` file:

|location_code|use  |
|-------------|-----|
|Czechia      |true |

## Definition of multiple interventions

In the intervention file you can define multiple intervention by simply adding a column/keys/attributes for each of them and indicating only keys which are correspond to the intervention type. For example, if you want to define two interventions, one for mobility and one for a beta change:

|location_code|use  |label  |intervention_type|start_day                     |num_days|end_day   |beta_change|layers|
|-------------|-----|-------|-----------------|------------------------------|--------|----------|-----------|------|
|CZ01         |true |Region lockdown CZ01|mobility_change  |2020-03-01                    |        |2020-05-19|           |      |
|CZ02         |true |Region lockdown CZ02|mobility_change  |                              |[10,25] |          |           |      |
|global       |true |Beta change for specific time|beta_change      |2020-01-01                    |        |2020-03-19|[0.5]      |[w,s] |
|global       |true |Beta change from start to end of simulation|beta_change      |2020-01-10                    |15      |          |0.7        |      |



