# Changelist
## XX. May 2024 UpdateLog v0.3.1

**Documentation update**
- Updated typing, few section are renamed.


## 1. May 2024 UpdateLog v0.3.0
Sandbox has been updated to new version. Also default sandbox is available in your home directory.

**Introducting Immunity and variants module**
- New immunity module for specifying new variants and new immunity parameters such as new types of vaccination. For more information look to [immunity settings](./examples/exampleE5B.md).

**Introducing validation module**

- Validation module can be used for validating configuration files and input csv/xlsx files. The module check for valid input data types and for correct paths to the configuration files.

**Documentation update**

- Documentation is being updated based on new changes, also old stuff is refactored and updated.
- Added new input Czech Synthetic population data - available in Downloads section.
- Added and updated section for:
    - running meta-simulation on grid.
    - added new intervention for sample vaccination
    - immunity
- Updated configuration files for
    - simulation
    - test runs

**Immunity intervention**
- Vaccination and Virus variant intervention as well as applying new parameters or updating original parameters has been introduced.
- More info about the extension can be found in - #TODO

**Testing sandbox**
- Testing sandbox was added to the user folder, also with the new configuration files for testing. It can be used for testing the validation module and also for testing the simulation module.
- Simulation is set to run in "test" mode, that means 20k agents per region, which makes tetsing simulation parameters and tetsing options of the extension much faster.

**Fixes**

- Grid computing sender improvements, and minor fixes.
- Fixed Grid computing validation 
- Report module fixes and improvements.
- Variants are now fully functional
- Fixed no mobility settings and tst settings

**Other Changes**
- All auto-save generated folders are now named by the name with the date and time of the creation. Now it will not further use only name without timestamp. 

**Upcoming changes**

- Variant and vaccine fixes and improvements.
- Extensions for validation module - such as checking for the correct scenarios. 

## 22. September 2023 UpdateLog v0.2.4
Look for new configuration files for simualtion and synthetic population, also sandbox has been updated to new version.

**Configuration_keys_changes**
- In population_age_distribution file -> 'population' changed to => 'population_size', and 'code' changed to => 'location_code'
- In mobility csv file -> 'code' changed to => 'location_code'

**Simulation module changes**

- Now you can use new input data management system. Instead of defining every single process through configuration files, now you can use *.csv or .*xlsx files, which are more user friendly. For more information look to [simulation settings](./Simulation_settings.md).
- New mobility indexes generation - now it will choose agents randomly across all the population. Not only based on the the population size distribution.
- Various updates to the simulation module. **NOTE: *code* was changes across all csv files to *location_code***
- Multiple variants of intervention parameters defining

**Documentation update**
- Documentation is being updated based on new changes, also old stuff is refactored and updated.

**Upcoming changes**

- Variant and vaccine fixes and improvements.
- Subtarget functions for more specific interventions.
- Grid computing sender improvements. Also with custom folder structure improvements.
- Dynamic layers intervention
- Functions for more specific data management (subtargets)


**Known Issues**

- If is mobility turned only on specific regions in simulation, it can make problems with synthetic population creation. It is recommended to use mobility in all regions or none. This issue will be fixed in next update.
- Grid computing - multiple occurence of same files in different folders - Like mobility and population files
- Grid computing - if there is sending on grid, synthpops must have full path to the parent configuration file. Cannot be merged from dirpath and name.


## 14. July 2023 UpdateLog v0.2.3
> Look for new configuration files for synthetic population, also sandbox has been updated to new version.
> **ATTENTION** - Please use basic folder structure naming and usage conventions. Like synthpops_input data in ../sandbox/input_data/synthpops_input_data and so on. It can make problems with actual grid computing implementation. Its allowed for now to use different naming of input_folder, but it needs to be named as 'input_folder_*something*'.

**Upcoming changes**

- Simulation module refactoring and improvements.
- Simplifying input data interface
- Variant and vaccine fixes and improvements.
- Grid computing sender improvements.

**Synthetic population module changes**

- **BRAND NEW** input interface for synthetic population creator. For more info look to [synthetic population settings](./Synthetic_pop_settings.md).
- Various updates to the original synthetic population package.
- **Look for change in mobility data and age distribution data changeg column** - not the *code* is changed to *location_code*.

**BugFixes**

- Code refactoring and bug fixes.
- Fixed bug with wrong calculation of filepaths when grid computing is enabled.


## 30. June 2023 UpdateLog v0.2.2
**Upcoming changes**

- Synthpops refactoring and improvements.
- Simplifying input data interface
- Parameters and function combination for input_data
- Variant and vaccine fixes and improvements.

**Synthetic population module changes**

- Now you can use new input data also for specified regions. Info about this can be found in [T4.1 Population input data](./examples/exampleE4_1.md)
- Checker for consistency of selected input data.
- Added copying files for region specific input_data

**BugFixes**

> Code refactoring and bug fixes.

## 26. June 2023 UpdateLog v0.2.1
**Upcoming changes**

> Synthetic population creation with more specific data for each region, not only for single run of simulation - with particular input data.

**Introducing Grid computing**

> Due to limited amount of resources on local server we did an automaticall sender/downloader for abmShare simulations. We reccomend this approach as its significantly faster and will not overload our local server, which will be now used as client for sending requests. For more information about running those simulation look for [Grid computing start](./examples/exampleE1.md#start-file-for-grid-computing)

**Python version update**

> Application is now tested with python version 3.10.X and also with 3.11.3. Due to new syntax features it is neccessary to use python >3.10.0. 

**Synthetic population input data**

> There was added more optionf for adding synthetic population data and also were added examples to the new chapter [T4.1 Population input data](./examples/exampleE4_1.md)
> Imported all possible input files for creating synthetic population.

## 19. April 2023 UpdateLog v0.1.8

**Upcoming changes**
> Synthetic population generator refactor to supply new features and to be more user friendly.

**Synthetic population changes**
> Now you can use new data for maintaining various synthetic population input files. such as:
  
  - employment_rates_by_age **DESCRIPTION WILL BE PROVIDED**

**Configuration change**
> If you want to work with pregenerated synthetic population with auto_save settings (With running Big runs with all modules), now is required to use new key *(key: location_code)* in each simulation for right simulation sorting.
> Now you can use not only *.json configuration files, but as well *.yaml files. Look for example files in download section.
> Synthpops now requires in region the *key:sheet* which is based on [Country names in MUestimate excels](./Downloads.md#muestimates---country-name-holder)
> Synthpops pop creation process in *key: state_location* is neccessary for full run and unlocking full performance potencial. Always use names like: NameOfRegion_CODE, like *Czechia_CZ01*. Code with name is splited by underscore. This code should match later the simulation location_code.

**Notable Fixes** <br>
*AutoSave Settings change*

> Now the path is not limited with use of underscores in the whole path. 
> Increment option for generating autosave_name is deprecated, if folder name exists, then the increment will always be Datetime.
*Other fixes*
> Various bug fixes.

**HPC integration**
> HPC integration is now manually working. Now we are developing a system for easier task sending.

**Simulation now runs FULLY parallel**
> No need to change anything in configuration files. Now the simulation run fully parallel if the *key:parallel_run* in simulation configuration is enabled.
> This is significantly faster up to 300% from previous single core runs.
> Also there is a faster improvement for full_run with creating synthetic population. up to 50% 

## 21. February 2023 UpdateLog v0.1.7

**New documentation**
Documentation now contains example usages of abmSHARE in more detail.

**New Interventions**
> More information about those new interventions can be found [T5.1 Simulation - Interventions](./examples/exampleE5A_1.md)

- Isolate contact intervention - for isolating overall contacts such as when schools are closed.
- Daily testing intervention - for testing given number of people per day.
- Testing probability - each person has assigned probability of being tested based on their states such as symptom, quarantine state etc.
- Contact tracing - if there was a contact with infected one, then place them in to quarantine.
- Probability based vaccination - apply vaccine to agents based on daily probability of being vaccinated.
- Alocate vaccines - allocate vaccines in pre-computed order of distribution. Specified rate of doses per day.

 **Note:** Vaccination intervention are still in development and does not properly work with custom created variants, because for every custom defined variant its 100% efficient.

**BugFixes**

-  Various changes
-  Minor bug fixes

**Incoming Features**

-  More specific data changes for synthetic population creation. (now its only various age-distribution) More options incoming. **Since V0.1.8**
-  Documentation improvements and more examples of usage. **Since V0.1.8**

**Future Plans**

-  Docker implementation
-  Performance improvements

## 13. February 2023 UpdateLog v0.1.6

**New documentation**
Documentation now contains example usages of abmSHARE in more detail.

**BugFixes**
-  Various changes
-  Minor bug fixes

**Incoming Features**

-  Vaccination **V0.1.7**
-  Tutorial examples of usage on website. **Since V0.1.6**
-  More specific data changes for synthetic population creation. (now its only various age-distribution) More options incoming. **Since V0.1.6**

**Future Plans**

-  Docker implementation
-  Performance improvements

## 25. January 2023 UpdateLog v0.1.5
Life quality improvements. Multiple ways for variant configuration.
**Important** With new variants, there is a significant increase of simulation time. Be aware of that.

**New configurations**

ABM simulation model new keys in variants. Be aware to this change in configuration files. Especially for including different variants
Report module configuration has new keys fo whole and separated variant output result creation.

**Variants**

Now can be different variants applied to each simulation model. You can configure not only global variants, which will start on day D with number of infection N in all regions/sims, but you can also define the starting points, which can be any region/sim you choose. So you can set a variant to only one region and when there is a mobility option ON, the variant will spread across other regions. Also you can set multiple days and multiple imports of choosen variant across sim/regions. Those variants are value and label sensitive. So variant with same label cannot have different values of beta,symp_prob etc... Also you can include global variants with those individual. More information can be seen on <a href="../Simulation_settings"> ABM module configuration. </a>

**Report by variants**

Now we can create reports for each variant by each sim/region or the whole sum of the all sims/regions.

**Downloads**

Now also contains example datasets for synthetic population creation.

**BugFixes**
-  Various changes
-  Minor bug fixes

**Incoming Features**

-  Vaccination **V0.1.7**
-  Tutorial examples of usage on website. **Since V0.1.6**
-  More specific data changes for synthetic population creation. (now its only various age-distribution) More options incoming. **Since V0.1.6**

**Future Plans**

-  Docker implementation
-  Performance improvements

## 9. January 2023 UpdateLog v0.1.4
Life quality improvements. Variants Introduced.
**Important** With new variants, there is a significant increase of simulation time. Be aware of that.

**New configurations**
ABM simulation model new key - variants

**Introducing variants**
Now can be different variants applied to each simulation model. For now there is an option to make a global variants. That means that on given day D (by user input) there are imports to every simulation with given number of infections by new variant. More information can be seen on <a href="../Simulation_settings"> ABM module configuration. </a>

**BugFixes**
-  Various changes
-  Minor bug fixes

**Incoming Features**

-  Vaccination **V0.1.7**
-  Variant apply for every simulation on different day **V0.1.5**
-  Better reporting for various variants. **V0.1.5**
-  Tutorial examples of usage on website. **Since V0.1.5**
-  More specific data changes for synthetic population creation. (now its only various age-distribution) More options incoming. **Since V0.1.5**

**Future Plans**

-  Docker implementation
-  Performance improvements


## 4. January 2023 UpdateLog V0.1.3
Life quality improvements. Changes for preventing usage of different port on Apache zeppelin for every user. Changes for sandbox.

**New configurations**

- Parent configuration file - can define path to a parent configuration file in synthetic region configuration

**BugFixes**

-  Waning calculation fixed. Now can be enabled used in ABM simulation as *'use_waning'* parameter
-  Configurations for creating synthetic population are now loaded and passed to the module. Now its not needed to copy those files into module.
-  Various changes

**New online documantation**

-  This documentation will stands for hot information about developing.  
-  Also Configuration files added for download on documentation page

**Incoming Features**

-  Vaccination 
-  New variants planned for **V0.1.4**
-  Tutorial examples of usage on website. 
-  More specific data changes for synthetic population creation. (now its only various age-distribution) More options incoming. 

**Future Plans**

-  Docker implementation
-  Performance improvements


## 12.12 UpdateLog V0.1.2
After every new update is also updated whole sandbox with changes in configuration files and manuals. **It's reccomended to check every setting (especially paths) from new configuration files**

## 29.11 UpdateLog V0.1.1
**Introducing Report module**
Report module generates .csv or .xlsx reports from every simulation and one sum report containing summary.


## 23.11 UpdateLog V0.1
**Popfile loading** If auto save - then is popfile loaded based on the sorted name from autocreated populations. If popfiles are provided, nothing changes and those popfiles are used for simulation.

**Upcoming changes**

**Popfile loading** from specific location also with auto save settings.
**Vaccination**
**Virus variants** defining them in configuration and also use more variants in simulation

