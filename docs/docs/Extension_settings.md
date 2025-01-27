# Main configuration file settings

## Initialize module settings
- synthpop_initialize **(bool)** - to enable synthetic population module (creating `jsons` or pop creation)
- simulation_initialize **(bool)** - to enable simulation module
- report_module_initialize **(bool)** -  to enable report module for generating `csv`/`xlsx` outputs
- test **(bool)** **OPTIONAL** -  to enable the test mode of a simulation. Recommended approach for debugging or for fast testing (loads 20,000 agents per region) 

## Auto save settings
Auto save settings stands for a system for creating smart outputs. **IMPORTANT there cannot be an underscore in the filepath. Please avoid naming of your folders with underscore.** <br>

- value **(bool)** - to enable auto saving <br>
- auto_increment **(bool)** - to enable the same name of output folder with date-time suffix <br>
- dirname **(string)** - to enable the output into named directory<br>
- location **(string)** -  path to output directory where all outputs will be saved. In this newly created directory the one specified with `dirname` will be used for all files needed in the simulation<br>
- copy_files **(object)** - object which can hold information about various items to copy, even when the original module was not initialized<br>
- copy_loaded_pop **(bool)** - option for copy population objects, which were created in previous runs and were not created in actual process of the abmSHARE simulation<br>

## Settings for Synthetic population module
- filepath **(string)** - path to Synthetic population configuration file <br>
## Settings for Simulation module
- filepath **(string)** - path to Simulation configuration file<br>
## Settings for Report module
- filepath **(string)** - path to Report configuration file <br> 

# Example configuration json
```json
{
    "initialize":
    {
        "synthpop_initialize":true,
        "simulation_initialize":true,
        "report_module_initialize":true
    },
    "auto_save_settings":
    {
        "value":true,
        "auto_increment":true,
        "dirname":"NoTestValues",
        "location":"/<Path_to_sandbox>/share-covasim/Outputs",   
        "copy_files":
        {
            "copy_loaded_pop":true
        }
    },
    "synthpops_settings":
    {
        "filepath":"/<Path_to_sandbox>/data/synthpops_configuration.json"
    },
    "simulation_settings":
    {
        "filepath":"/<Path_to_sandbox>/data/covasim_configuration.json"
    },    
    "report_settings":
    {
        "filepath":"/<Path_to_sandbox>/data/test_report_configuration.json"
    }
}
```
