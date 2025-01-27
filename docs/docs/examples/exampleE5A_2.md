# Intervention types

This section describes the intervention types and their parameters.

**Interventions are defined in the proper [simulation intervention file](../downloads/simulation_data/simulation_interventions.csv)**

## Mobility intervention

Mobility intervention can be used to simulate region lockdowns. 
When some region is locked down, agents cannot travel in and out of the region. 
This intervention can take effect only if **mobility feature** is enabled and defined with proper mobility input data (for details see [here](./exampleE5.md#core-features)).

Example of valid keys for [parameters](../Parameters.md#parameters-for-mobility-intervention)

|location_code|use  |label     |intervention_type|start_day |num_days  |end_day   |
|-------------|-----|----------|-----------------|----------|----------|----------|
|CZ01         |true |mob_change|mobility_change  |2020-03-01|          |2020-05-19|
|CZ02         |false|mob_change|mobility_change  |          |"[10,25]" |          |


## Change in beta (overall transmission) intervention

This intervention can be used to specify transmission by a certain amount for given day/days. Can be used for school closures/restrictions, home office, wearing masks etc. These changes affect the overall transmission parameter in the selected layers.

Example of valid keys for [parameters](../Parameters.md#parameters-for-changing-beta-intervention)

|location_code|use  |label  |intervention_type|start_day                     |num_days|end_day   |beta_change|layers|
|-------------|-----|-------|-----------------|------------------------------|--------|----------|-----------|------|
|global       |false|mah    |beta_change      |2020-01-01                    |        |2020-03-19|[0.5]      |[w,s] |
|global       |true |meh    |beta_change      |2020-01-10                    |15      |          |[0.5,0.7]  |      |

## Contact isolation intervention

Isolate contacts from simulation by, for example, removing contacts for school or for every contact layer. 
When intervention ends contacts will be restored. Can affect putting people to quarantine, if there is testing and tracking, because of contact removal. Can be used for example for school closures, home offices etc. 
Compared to the change in beta, contact isolation intervention removes contacts while preserving the transmission value.

Example of valid keys for [parameters](../Parameters.md#parameters-for-contact-isolation)

|location_code|use  |label  |intervention_type|start_day                     |num_days|end_day   |beta_change|layers|
|-------------|-----|-------|-----------------|------------------------------|--------|----------|-----------|------|
|CZ01         |true |contact isolation interv|isolate_contacts |25                            |        |83        |[0.7,1]    |[s,w] |
|Global       |true |contact isolation interv global|isolate_contacts |25                            |        |          |0.7        |[s,w] |


## Daily testing intervention

Intervention for daily testing specifies the number of agents tested per day. 
Its value can be also dependent on other values such as the probability of testing people who are quarantined etc. More info can be found in parameters.

Example of valid keys for [parameters](../Parameters.md#parameters-for-daily-testing)

|location_code|use  |label  |intervention_type|start_day                     |num_days|end_day   |daily_tests|symp_test|sensitivity|test_delay|
|-------------|-----|-------|-----------------|------------------------------|--------|----------|-----------|---------|-----------|----------|
|CZ01         |false|Per day testing intervention CZ01|per_day_testing  |10                            |        |2020-01-30|           |1.5     |1.0        |5         |
|Global       |false|Per day testing intervention global|per_day_testing  |2020-01-01                    |        |2020-01-30|1000       |1.0      |1.0          |1          |


## Testing probability intervention

This intervention assigns to each person a probability of being tested based on the person's symptom state etc. 
The total number of tests is not specified as in [Daily testing intervention](./exampleE5A_1.md#daily-testing-intervention), but it influences the probability of being tested. Can be used as a substitute to the daily testing intervention.

Example of valid keys for [parameters](../Parameters.md#parameters-for-testing-probability)

|location_code|use  |label  |intervention_type|start_day                     |num_days|end_day   |symp_prob|symp_quar_prob|asymp_prob|
|-------------|-----|-------|-----------------|------------------------------|--------|----------|---------|--------------|----------|
|global       |false|Testing probability CZ01    |testing_probability|20                            |        |2020-03-30|0.1      |0.3           |0.01      |
|CZ01         |false|Tetsing probability CZ01    |testing_probability|2020-01-01                    |30      |          |0.1      |0.3           |0.01      |


## Contact tracing intervention

Contact tracing of agents who are already diagnosed positive by a testing intervention. Contacts are contacted and put in the quarantine (depends on simulation *key:quar_factor* parameter) for a certain period of time. If there is a probability of testing intervention, there can be significant increase of testing of contact-traced agents.

Example of valid keys for [parameters](../Parameters.md#parameters-for-contact-tracing). Note that there must be testing intervention (such as [Daily testing](./exampleE5A_1.md#daily-testing-intervention) or [Probability testing](./exampleE5A_1.md#testing-probability-intervention)) before/on day D of starting the contact tracing intervention, otherwise this intervention will not work.

|location_code|use  |label  |intervention_type|num_days                      |capacity|trace_probs|quar_period|
|-------------|-----|-------|-----------------|------------------------------|--------|-----------|-----------|
|Cz01         |false|contact tracing|contact_tracing  |                              |0.5     |6          |6          |
|global       |false|contact tracing|contact_tracing  |[10,30]                       |0.5     |6          |6          |


## Simple vaccination

Can be used to apply a simple vaccine to a subset of the population. 
This intervention can be added to changing the relative susceptibility and the probability of developing symptoms if still infected. 
More info about vaccination can be found in [T5.3 Simulation - Immunity and variants](./exampleE5B.md).

Example of valid keys for [parameters](../Parameters.md#parameters-for-simple-vaccination)

|location_code|use |label            |intervention_type |prob|rel_sus|rel_symp|
|-------------|----|-----------------|------------------|----|-------|--------|
|global       |true|simple_vac_interv|simple_vaccination|0.9 |1.0    |1.0     |


### Intervention stacking

You can define multiple interventions and it is not necessary to use all the keys. 
In the intervention `csv`/`xlsx` file you can define multiple intervention with its corresponding keys and those while leaving empty those interventions that are not used. **Do not define user custom keys which are not corresponding to the allowed keys for each intervention.**

Example of intervention stacking:

|location_code|use  |label  |intervention_type|start_day                     |num_days|end_day   |beta_change|layers|vaccine|sequence|num_doses|symp_prob|symp_quar_prob|asymp_prob|capacity|trace_probs|quar_period|daily_tests|symp_test|sensitivity|test_delay|
|-------------|-----|-------|-----------------|------------------------------|--------|----------|-----------|------|-------|--------|---------|---------|--------------|----------|--------|-----------|-----------|-----------|---------|-----------|----------|
|CZ01         |true |TestLabel|mobility_change  |2020-03-01                    |        |2020-05-19|           |      |       |        |         |         |              |          |        |           |           |           |         |           |          |
|global       |true |TestLabel|beta_change      |2020-01-10                    |15      |          |[0.5,0.7]  |      |       |        |         |         |              |          |        |           |           |           |         |           |          |
|global       |false|TestLabel|testing_probability|2020-01-01                    |        |2020-03-30|           |      |       |        |         |0.1      |0.3           |0.01      |        |           |           |           |         |           |          |
|global       |false|TestLabel|contact_tracing  |10                            |        |          |           |      |       |        |         |         |              |          |0.5     |6          |6          |           |         |           |          |
|CZ01         |false|TestLabel|per_day_testing  |10                            |        |2020-01-30|           |      |       |        |         |         |              |          |        |           |           |900       |1.0      |1          |1          |
|global       |false|TestLabel|testing_probability|20                            |        |2020-03-30|           |      |       |        |         |0.1      |0.3           |0.01      |        |           |           |           |         |           |          |
|global       |false|TestLabel|contact_tracing  |                              |[10,30] |          |           |      |       |        |         |         |              |          |0.5     |6          |6          |           |         |           |          |


### Requirements

Valid keys with values must be provided for each intervention, along with the necessary keys.

- [Neccessary keys](./exampleE5A_1.md#how-to-define-intervention) 
- Remaining of [parameters keys](../Parameters.md#intervention-parameters)


