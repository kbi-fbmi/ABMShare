## Imminuty and variants

In the simulation module you can integrate different [covasim-based](https://github.com/InstituteforDiseaseModeling/covasim) variants or introduce new variants of covid or different diseases by defining them in the [Simulation module](../Simulation_settings.md#variants). Those variants are based on five parameters:

- rel_beta  - Relative transmissibility variation by strain. (1.0 = 100%)
- rel_symp_prob - Scale factor for the proportion of symptomatic cases. (1.0 = 100%)
- rel_severe_prob - Scale factor for the proportion of symptomatic cases that become severe. (1.0 = 100%)
- rel_crit_prob - Scale factor for the proportion of severe cases that become critical. (1.0 = 100%)
- rel_death_prob - Scale factor for the proportion of critical cases that result in death. (1.0 = 100%)

Of course, there are several other parameters which influence the model behavior, but the above parameters are the most essential in simulation.
Based on those variants you can use or define custom variants that are already implemented in [covasim](https://github.com/InstituteforDiseaseModeling/covasim). Information about these variants and their values can be found in [parameters](../Parameters.md#parameters-for-covasim-variants).
You can also define multiple interventions and integrate them in the simulation; you can define variants in the same way.

For updating values for existing or for providing new variants you have to specify various input files specified below.
The structure of the variant folder is:
```
|   +-- simulation_immunity_files
    |   +-- immunity_input_files.csv
    |   +-- vaccine_dose_pars.csv
    |   +-- vaccine_variant_pars.csv
    |   +-- variants_cross_immunity.csv
    |   +-- variants_pars.csv
```
Each file has its own structure and meaning. All those files are then loaded based on definition in *immunity_input_files.csv*

|vaccine_dose_pars           |vaccine_variant_pars            |variant_pars             |variant_cross_immunity             |
|----------------------------|--------------------------------|-------------------------|-----------------------------------|
|path/vaccine_dose_pars.csv| path/vaccine_variant_pars.csv| path/variants_pars.csv| path/variants_cross_imunnity.csv|



#### Define new variants
You can update the default variant parameters, or provide new variants with immunity module.

- In *variant_pars.csv* 
file you can define 
new variants and its base parameters:

|variant|rel_beta|rel_symp_prob|rel_severe_prob |rel_crit_prob|rel_death_prob|
|-------|--------|-------------|----------------|-------------|--------------|
|omicron| 0.015  |0.3          |0.1             |0.1          |0.01          |

- In *variants_cross_immunity.csv* 
file you can define 
cross immunity between variants: It also adds to existing ones the same, as is specified in its cross definition.

|variant|wild   |alpha|beta            |gamma|delta|omicron|
|-------|-------|-----|----------------|-----|-----|-------|
|omicron| 0.05  | 0.06| 0.07           | 0.08| 0.09| 1     |

#### Define new vaccines
You can update default vaccine parameters, or provide a new vaccines with immunity module.

- In *vaccine_dose_pars.csv* 
you can define
new vaccines and its base parameters:

|vaccine|dist   |par1|par2            |nab_boost|doses|interval|
|-------|-------|----|----------------|---------|-----|--------|
|pfizer_new |normal |-1.5|2               |2        |3    |10      |

- In *vaccine_variant_pars.csv* you can define new vaccines or update existing ones.
you can define vaccine parameters for each variant.
Also when there are new variants you should specify new cross vaccine parameters. This can be used only when there is a new vaccination in the simulation, because only when new variant is introduced, the model needs to know how to react with the existing vaccines.

|vaccine|wild   |alpha|beta            |gamma|delta|omicron|
|-------|-------|-----|----------------|-----|-----|-------|
|pfizer |       |     |                |     |     |1/2    |
|moderna|       |     |                |     |     |1/3    |
|az     |       |     |                |     |     |1/4    |
|jj     |       |     |                |     |     |1/5    |
|novavax|       |     |                |     |     |1/6    |
|sinovac|       |     |                |     |     |1/7    |
|sinopharm|       |     |                |     |     |1/8    |
|pfizer_new|1/3    |2/3  |3/3             |1/3  |2/3  |3/3    |

 
