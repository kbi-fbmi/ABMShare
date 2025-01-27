# Report configuration and report module system stands for getting data in chosen format.
## Configuration file keys
- create_report **(bool)** - This key decides about getting the whole report and calling the report system<br>
- output_format **(string) OPTIONS: csv, xlsx** - this key is for chosen the output data format<br>
- output_path **(string)** - path for saving output files **It can be overwritten, when auto_settings save is enabled**<br>
- input_multisim **(string)** - it serves for more specific defining the input simulation and parameters for output. **It can be overwritten by Auto_saving system, which will load the actual simulation object**
    - filepath **(str)** - filepath to specific sim object.
    - allkeys **(bool)** - if an output files with all the keys should be created
    - keys **(list of strings)** - output file will have only those keys
    - whole_simulation **(bool)** - if output csv should have information about the whole simulation **Can be also combined with separated_simulation**
    - separated_simulation **(bool)** - output csvs will be for every region/simulation separately **Can be also combined with whole_simulation**
    - whole_variants **(bool)** - specifies if user want to create report with variant specific data for all provided sims/regions. **Can be also combined with separated_variants**
    - separated_variants **(bool)** - specifies if user want to create report with variant specific data for every sim/region each separately
- reports **(list of objects)** - reports will be standing for more accurate reports of given variables. **Can also be combined with whole_variants**
    - keys **(list of strings)** - output file will have only those keys
    - output_format **(string) Available OPTIONS: csv, xlsx** - this key is for chosen the output data format **Overrides basic output_format for this report**



# Example json configuration file
```json 
{
    "create_report":true,
    "output_format":"csv",
    "input_multisim":
    {
        "filepath":"",
        "all_keys":true,
        "keys":
        [

        ],
        "whole_simulation":true,
        "separated_simulation":true,
        "whole_variants":true,
        "separated_variants":true
    },
    "reports":
    [
        {
          "keys": ["t","new_deaths","n_dead"],
          "output_format":""
        }
    ]
}
```
