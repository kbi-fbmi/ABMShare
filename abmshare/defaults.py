import os
import copy

def get_filepath(path):
    this_dir=os.path.dirname(os.path.abspath(__file__)) #Example dir 
    return os.path.join(this_dir,path)

def get_filepath_default(path):
    this_dir=os.path.abspath(__file__+"/../../")#Example dir 
    return os.path.join(this_dir,path)

def get_filepathSP(path):
    this_dir=os.path.abspath(__file__+"/../../synthpops") #Example dir 
    return os.path.join(this_dir,path)

def get_filepathCV(path):
    this_dir=os.path.abspath(__file__+"/../../covasim") #Example dir 
    return os.path.join(this_dir,path)

testsettings={
    "n_size":20000,
    "mobility_size":200,
    "suffix":"",
    "prefix":"test_"
}
test_n_people=20000
population_age_distributions_bins=[16,20]

population_age_distribution_default={ "num_bins": 0, "distribution":[] }

report_default_format="xlsx"

# Variables for variant changes based on being only included in sims. Values can be changed overtime
default_empty_variant={
    "number_of_imports":0,
    "days":0
}

variant_result_keys=['prevalence_by_variant',
 'incidence_by_variant',
 'cum_infections_by_variant',
 'cum_symptomatic_by_variant',
 'cum_severe_by_variant',
 'cum_infectious_by_variant',
 'new_infections_by_variant',
 'new_symptomatic_by_variant',
 'new_severe_by_variant',
 'new_infectious_by_variant',
 'n_exposed_by_variant',
 'n_infectious_by_variant'
]


modules={
    "synthpops":False,
    "multisim":False,
    "report":False,
}

pathvalues={
    'default_configuration' :'data/default_configuration.json', #default parent
    'mobility_path'         :'covasim_ex/data/CZ_NUTS2_mobility.xlsx',
    'population_path'       :'covasim_ex/data/CZ_NUTS2_population.xlsx',
    "output_path"           :'outputs',
    "default_synthpops_region_creator_datafiles":"data/default_csv",
    "synthetic_population"  :"synthpops",
    "simulation_model"      :"covasim",
    "grid_compute"          :"extensions/grid_compute_ex",
}

save_settings={
    'population_path':"pops",
    'population_configurations':"pop_configurations",
    'saved_multisim':'sims',
    'saved_images':'images',
    "output_reports":"output_reports"
}

# Key specified to json configuration
confkeys={
    'covasim_pars':'covasim_pars', 
    'synthpops_pars':'synthpops_pars',
    'global_pars':'global_pars',
    'region_pars':'region_pars',
    'different_pars':'different_pars',
    "regions":"regions",
    'mobility_pars':'mobility_pars',
    'population_pars':'population_pars',
    'interventions':'interventions',
    'pars':'pars',
    'popfile':'popfile',
    'simulation_pars':'sim_pars',
    'region_config':"region_settings",
    'pop_creator_config':"pop_creator_settings",
    "global_only":"global_only",
    "include_with_different":"include_with_different",
    "include_keys":"include_keys",
    "intervention_list":"intervention_list",
    "auto_save_settings":"auto_save_settings",
    "save_pars":"save_pars",
    "input_multisim":"input_multisim",
    "create_report":"create_report",
    "reports":"reports",
    "whole_simulation":"whole_simulation",
    "separated_simulation":"separated_simulation",
    "copy_files":"copy_files",
    "copy_loaded_pop":"copy_loaded_pop",
    "config_dirpath":"config_dirpath",
    "parent_location":"parent_location",
    "parent":"parent",
    "variants":"variants",
    "variant":"variant",
    "label":"label",
    "days":"days",
    "n_imports":"number_of_imports",
    "interventions_different":"interventions_different",
    "variants_different":"variants_different",
    "variant_list":"variant_list",
    "whole_variants":"whole_variants",
    "separated_variants":"separated_variants",
    "filepath":"filepath",
    "region_data_name":"region_data_name",
    "location_code":"location_code",
    "grid_compute":"grid_compute", # Just for development purposes
    "synthpop_initialize":"synthpop_initialize",
    "simulation_initialize":"simulation_initialize",
    "report_module_initialize":"report_module_initialize",
    "initialize":"initialize",
    "synthpops_settings":"synthpops_settings",
    "simulation_settings":"simulation_settings",
    "report_settings":"report_settings",
    "mobility_path":"mobility_path",
    "pops":"pops",
    "pop_location":"pop_location",
    "input_data":"input_data",
    "output_data":"output_data",
    "original_confs":"original_confs",
    "data":"data",
    "population_age_distributions":"population_age_distributions",
    "population_age_distributions_brackets":"population_age_distributions_brackets",
    "region_config_path":"region_config_path",
    "region_config_filename":"region_config_filename",
    "pars_file":"pars_file",
    "multiprocess":"parallel_run",
    "population":"population",
    "synthpops_input_data":"synthpops_input_data",
    "value":"value",
    "intervention_type":"intervention_type",
    "type":"type",
    "use":"use",
    "population_size":"population_size",
    "simulation_configuration_files":"simulation_configuration_files",
    "synthpops_configuration_files":"synthpops_configuration_files",
    "simulation_immunity_files":"simulation_immunity_files"
}


# Default file allowed for Synthpops/data
# If neccessary, there can be added another files, otherwise in every run will other be deleted.



default_synthpops_data_files=[
    "Czechia-Czechia_CZ01.json",
    "Czechia.json",
    "MUestimates_all_locations.obj",
    "MUestimates_home.obj",
    "MUestimates_other_locations.obj",
    "MUestimates_school.obj",
    "MUestimates_work.obj",
    "README.md",
    "usa-Washington-seattle_metro.json",
    "usa-Washington.json",
    "usa.json"
]

# Valid pars for simulation
# Source https://docs.idmod.org/projects/covasim/en/latest/parameters.html
covasim_pars={
    #Only for mobility sim validation
    'sim_pars':[
        'n_days',
        'start_day',
        'end_day',
        'pop_type',
        'pop_infected',
        'use_waning',# added before mobility fix
        "rand_seed"
    ],
    'sim_constructor':[
        'label',       
        'popfile',
    ],
    'global_pars_settings':[
        'global_only',
        'include_global',
        'include_keys'
    ],
    'population_pars':[
        'pop_file', #added for population .xlsx or .csv
        'pop_size',
        'pop_infected',
        'pop_type',
        'location',
    ],
    'simulation_pars':[
        'pop_file', # added for created .pop via synthpops
        'people', # added for reference to created and holded pop via synthpops
        'start_day',
        'end_day',
        'n_days',
        'rand_seed',
        'verbose',
        'label' # added for sim labeling
    ],
    'rescaling_pars':[
        'pop_scale',
        'scaled_pop',
        'rescale',
        'rescale_threshold',
        'rescale_factor'
    ],
    'basic_disease_trans':
    [
        'beta',
        'n_imports',
        'beta_dist',
        'viral_dist',
        'asymp_factor'
    ],
    'network_pars':
    [
        'contacts',
        'dynam_layer',
        'beta_layer'
    ],
    'multi_strain_pars':
    [
        'n_imports',
        'n_strains'
    ],
    'immunity_pars':
    [
        'use_waning',
        'nab_init',
        'nab_decay',
        'nab_kin',
        'nab_boost',
        'nab_eff',
        'rel_imm_symp',
        'immunity'
    ],
    'strain_specifis_pars':
    [
        'rel_beta',
        'rel_imm_strain'
    ],
    'time_for_disease_progression':
    [
        'exp2inf',
        'inf2sym',
        'sym2sev'        
    ],
    'time_for_disease_recovery':
    [
        'asym2rec',
        'mild2rec',
        'sev2rec',
        'crit2rec'        
    ],
    'severity_pars':
    [
        'rel_symp_prob',
        'rel_severe_prob',
        'rel_crit_prob',
        'rel_death_prob',
        'prog_by_age',
        'prognoses'
    ],
    'efficiacy_of_protection_measures':
    [
        'iso_factor',
        'quar_factor',
        'quar_period'
    ],
    'events_and_interventions':
    [
        'interventions',
        'analyzers',
        'timelimit',
        'stopping_func'
    ],
    'health_system_parameters':
    [
        'n_beds_hosp',
        'n_beds_icu',
        'no_hosp_factor',
        'no_icu_factor'
    ],
    "interventions":
    [
        "type",
        "start_day",
        "end_day",
        "start_change",
        "end_change",
        "layers"
    ],  
    "analyzers":
    [
        
    ]
}

interventions={
    "beta_change":
    [
        'type',
        'label',
        'start_day',
        'end_day',
        'num_days',
        'days', # is num_days
        'beta_change',
        'layers'
    ],  
    "mobility_change":
    [
        'type',
        'location_code',
        'label',
        'start_day',
        'end_day',
        'num_days'
    ],
    "isolate_contacts":
    [
        'type', 
        'label',
        'days', # can also be a list
        'start_day',
        'end_day',
        'num_days',
        'beta_change', # can also be a list
        'layers'
    ],
    "per_day_testing":
    [
        'type',
        'label',
        'daily_tests',
        'symp_test',
        'quar_test',
        'quar_policy',
        'subtarget',
        'ili_prev',
        'sensitivity',
        'loss_prob',
        'test_delay',
        'start_day',
        'end_day',
        'swab_delay'
        'num_days',
    ],
    "testing_probability":[
        "type",
        "label",
        "days",        
        "symp_prob",
        "asymp_prob",
        "symp_quar_prob",
        "asymp_quar_prob",
        "quar_policy",
        "subtarget",
        "ili_prev",
        "sensitivity",
        "loss_prob",
        "test_delay",
        "start_day",
        "end_day",
        "swab_delay",
        'num_days'
    ],
    "contact_tracing":
    [
        "type",
        "label",
        "trace_probs",   
        "trace_time",
        "start_day",
        "end_day",
        'num_days',
        "presumptive",
        "capacity",
        "quar_period",        
    ],
    "vaccinate_probability":
    [
        "type",
        "vaccine",
        "label",
        "days",
        "prob",
        "booster",
        "subtarget",
        'num_days',
        "start_day",
        "end_day",
        "vaccine_dict" # TODO: casem
    ],
    "vaccinate_distribution":
    [
        "type",
        "label",
        "vaccine",
        "num_doses",
        "booster",
        "subtarget",
        "sequence",
        'num_days',
        "start_day",
        "end_day"
    ],
    "simple_vaccination":
    [
        "type",
        "label",
        "days",
        "prob",
        "rel_sus",
        "rel_symp",
        "subtarget",
        "cumulative",
        'num_days',
        "start_day",
        "end_day"
    ],
    "base_vaccination":
    [
        "type",
        "vaccine",
        "label",
        "booster",        
        "days",
        "num_days",
        "start_day",
        "end_day",        
    ],
    "weekend_off":
    [
        'type',
        'label',
        'start_day',
        'end_day',
        'num_days',
        'days',
        'beta_change',
        'layers'
    ],
    "variant":
    [
        "variant",
        "days",
        "num_days",
        "start_day",
        "end_day",
        "label",
        "number_of_imports",
        "rescale"
    ]
}

covasim_pars_all=[
        'location_code',
        'unique_mobility_indexes',
        'n_days',
        'start_day',
        'end_day',
        'pop_type',
        'pop_infected',
        'use_waning',# added before mobility fix
        "rand_seed",
        'label',       
        'popfile',

        'pop_size',
        'pop_infected',
        'pop_type',
        'verbose',

        'pop_scale',
        'scaled_pop',
        'rescale',
        'rescale_threshold',
        'rescale_factor',

        'beta',
        'n_imports',
        'beta_dist',
        'viral_dist',
        'asymp_factor'

        'contacts',
        'dynam_layer',
        'beta_layer',

        'n_imports',
        'n_strains',

        'use_waning',
        'nab_init',
        'nab_decay',
        'nab_kin',
        'nab_boost',
        'nab_eff',
        'rel_imm_symp',
        'immunity',

        'rel_beta',
        'rel_imm_strain',

        'exp2inf',
        'inf2sym',
        'sym2sev',        

        'asym2rec',
        'mild2rec',
        'sev2rec',
        'crit2rec',        

        'rel_symp_prob',
        'rel_severe_prob',
        'rel_crit_prob',
        'rel_death_prob',
        'prog_by_age',
        'prognoses',

        'iso_factor',
        'quar_factor',
        'quar_period',

        'interventions',
        'analyzers',
        'timelimit',
        'stopping_func',

        'n_beds_hosp',
        'n_beds_icu',
        'no_hosp_factor',
        'no_icu_factor'
]

covasim_constructor_pars_mapping={
    "name":"label",
    "popfile":"popfile",
    "location_code":"location_code",
    "region_parent_name":"region_parent_name"
}

synchronization_pars=['n_infections','susceptible','naive','exposed','exposed_variant','infectious_variant','peak_nab','date_susceptible',#'exposed_by_variant','infectious_by_variant',
     'date_naive','date_exposed','date_infectious','date_symptomatic','date_severe','date_critical','date_tested','date_diagnosed','date_recovered','date_known_dead',
     'date_dead','date_known_contact','date_quarantined','date_vaccinated','date_pos_test','date_end_quarantine','dur_exp2inf','dur_inf2sym','dur_sym2sev',#'symp_imm','sev_imm',
     'dur_sev2crit','dur_disease','recovered_variant'
]
arraypars=['exposed_by_variant','symp_imm','sev_imm','infectious_by_variant','sus_imm']
synthpops_pars={
    "regions":
    [
        'name_with_diacritic',
        'name',
        'filename',
        'location_code',
        'sheet_name',
        'country_location',
        'state_location',
        'parent',
        "region_data_name",
        "config_dirpath", # Optional
        'population_age_distributions',
        'employment_rates_by_age',
        'enrollment_rates_by_age',
        'household_head_age_brackets',
        'household_head_age_distribution_by_family_size',
        'household_size_distribution',
        'school_size_brackets',
        'school_size_distribution',
        'school_size_distribution_by_type',
        'school_types_by_age',
        'workplace_size_counts_by_num_personnel'
    ],
    "age_distribution":
    [
        'num_bins',
        "filename"
    ],
    "load_pop_keys":
    [
        'num_bins',
        'distribution'
    ],
    "region_pars":
    [
        'location_name',
        'data_provenance_notices',
        'reference_links',
        'citations',
        # 'notes',
        'parent',
        'population_age_distributions',
        'employment_rates_by_age',
        'enrollment_rates_by_age',
        'household_head_age_brackets',
        'household_head_age_distribution_by_family_size',
        'household_size_distribution',
        'ltcf_resident_to_staff_ratio_distribution',
        'ltcf_num_residents_distribution',
        'ltcf_num_staff_distribution',
        'ltcf_use_rate_distribution',
        'school_size_brackets',
        'school_size_distribution',
        'school_size_distribution_by_type',
        'school_types_by_age',
        'workplace_size_counts_by_num_personnel'
    ],
    "pop_creator_pars": # For pars_file.csv
    [
        "n",
        "max_contacts",
        "ltcf_pars",
        "shool_pars",
        "with_industry_code",
        "with_facilities",
        "use_default",
        "use_two_group_reduction",
        "average_ltcf_degree",
        "ltcf_staff_age_min",
        "ltcf_staff_age_max",
        "with_school_types",
        "school_mixing_type",
        "average_class_size",
        "inter_grade_mixing",
        "average_student_teacher_ratio",
        "average_teacher_teacher_degree",
        "teacher_age_min",
        "teacher_age_max",
        "with_non_teaching_staff",
        "average_student_all_staff_ratio",
        "average_additional_staff_degree",
        "staff_age_min",
        "staff_age_max",
        "rand_seed",
        "country_location",
        "state_location",
        "location",
        "sheet_name",
        "household_method",
        "smooth_ages",
        "household_method",
        "windows_length",
        "do_make",
        "country_filepath",
    ],
    "pop_location_pars":
    [
        "state_location",
        "country_location",
        "sheet_name",
        "region_config_filename"
    ]
}
default_region_pars=[
    "location_name",
    "data_provenance_notices",
    "reference_links",
    "citations",
    "notes",
    "parent",
    "population_age_distributions",
    "employment_rates_by_age",
    "enrollment_rates_by_age",
    "household_head_age_distribution_by_family_size",
    "household_size_distribution",
    "ltcf_resident_to_staff_ratio_distribution",
    "ltcf_num_residents_distribution",
    "ltcf_num_staff_distribution",
    "ltcf_use_rate_distribution",
    "school_size_brackets",
    "school_size_distribution",
    "school_size_distribution_by_type",
    "school_types_by_age",
    "workplace_size_counts_by_num_personnel",
]

synthpops_csv_files=[
        'population_age_distributions',
        'employment_rates_by_age',
        'enrollment_rates_by_age',
        'household_head_age_brackets',
        'household_head_age_distribution_by_family_size',
        'household_size_distribution',
        'school_size_brackets',
        'school_size_distribution',
        'school_size_distribution_by_type',
        'school_types_by_age',
        'workplace_size_counts_by_num_personnel'
]

synthpops_one_file_data={
    'household_head_age_brackets':'load_household_head_age_brackets',
    'household_head_age_distribution_by_family_size':'load_household_head_age_distribution_by_family_size',
    'household_size_distribution':'load_household_size_distribution',
    'school_size_brackets':'load_school_size_brackets',
    'school_size_distribution':'load_school_distribution',
    'school_size_distribution_by_type':'load_school_size_distribution',
    'school_types_by_age':'load_school_types',
    'workplace_size_counts_by_num_personnel':'load_workplace_size_counts'
}

report_keys=[
"cum_infections",
"cum_reinfections",
"cum_infectious",
"cum_symptomatic",
"cum_severe",
"cum_critical",
"cum_recoveries",
"cum_deaths",
"cum_tests",
"cum_diagnoses",
"cum_known_deaths",
"cum_quarantined",
"cum_doses",
"cum_vaccinated",
"new_infections",
"new_reinfections",
"new_infectious",
"new_symptomatic",
"new_severe",
"new_critical",
"new_recoveries",
"new_deaths",
"new_tests",
"new_diagnoses",
"new_known_deaths",
"new_quarantined",
"new_doses",
"new_vaccinated",
"n_susceptible",
"n_exposed",
"n_infectious",
"n_symptomatic",
"n_severe",
"n_critical",
"n_recovered",
"n_dead",
"n_diagnosed",
"n_known_dead",
"n_quarantined",
"n_vaccinated",
"n_imports",
"n_alive",
"n_naive",
"n_preinfectious",
"n_removed",
"prevalence",
"incidence",
"r_eff",
"doubling_time",
"test_yield",
"rel_test_yield",
"frac_vaccinated",
"pop_nabs",
"pop_protection",
"pop_symp_protection",
"variant",
"date",
"t"
]

# and without variant
report_keys_without_date=[
"cum_infections",
"cum_reinfections",
"cum_infectious",
"cum_symptomatic",
"cum_severe",
"cum_critical",
"cum_recoveries",
"cum_deaths",
"cum_tests",
"cum_diagnoses",
"cum_known_deaths",
"cum_quarantined",
"cum_doses",
"cum_vaccinated",
"new_infections",
"new_reinfections",
"new_infectious",
"new_symptomatic",
"new_severe",
"new_critical",
"new_recoveries",
"new_deaths",
"new_tests",
"new_diagnoses",
"new_known_deaths",
"new_quarantined",
"new_doses",
"new_vaccinated",
"n_susceptible",
"n_exposed",
"n_infectious",
"n_symptomatic",
"n_severe",
"n_critical",
"n_recovered",
"n_dead",
"n_diagnosed",
"n_known_dead",
"n_quarantined",
"n_vaccinated",
"n_imports",
"n_alive",
"n_naive",
"n_preinfectious",
"n_removed",
"prevalence",
"incidence",
"r_eff",
"doubling_time",
"test_yield",
"rel_test_yield",
"frac_vaccinated",
"pop_nabs",
"pop_protection",
"pop_symp_protection"
]

person_keys=[
    #'uid',              # Int
    'age',              # Float
    'sex',              # Float
    'symp_prob',        # Float
    'severe_prob',      # Float
    'crit_prob',        # Float
    'death_prob',       # Float
    'rel_trans',        # Float
    'rel_sus',          # Float
    'n_infections',     # Int
    'n_breakthroughs',  # Int
]

person_states = [
    'susceptible',
    'naive',
    'exposed',
    'infectious',
    'symptomatic',
    'severe',
    'critical',
    'tested',
    'diagnosed',
    'recovered',
    'known_dead',
    'dead',
    'known_contact',
    'quarantined',
    'vaccinated',
]

person_variant_states = [
    'exposed_variant',
    'infectious_variant',
    'recovered_variant',
]

person_by_variant_states = [ # Array
    'exposed_by_variant',
    'infectious_by_variant',
]

person_imm_states = [ # Array
    'sus_imm',  # Float, by variant
    'symp_imm', # Float, by variant
    'sev_imm',  # Float, by variant
]

person_vacc_states = [ #Array
    'doses',          # Number of doses given per person
    'vaccine_source', # index of vaccine that individual received
]

person_nab_states = [ #Array
    'peak_nab',    # Float, peak neutralization titre relative to convalescent plasma
    'nab',         # Float, current neutralization titre relative to convalescent plasma
    't_nab_event', # Int, time since nab-conferring event
]

person_durs = [
    'dur_exp2inf',
    'dur_inf2sym',
    'dur_sym2sev',
    'dur_sev2crit',
    'dur_disease',
]

person_all_states=person_keys+person_states+person_variant_states+person_vacc_states+person_nab_states+person_durs
person_arrays=person_by_variant_states+person_imm_states

simulation_variant_keys=[
    "variant",
    "label",
    "days",
    "number_of_imports",
    "rescale"
]

custom_variant_keys=[
    "rel_beta",
    "rel_symp_prob",
    "rel_severe_prob",
    "rel_crit_prob",
    "rel_death_prob"
]

default_variants=[
    "wild",
    "alpha",
    "beta",
    "gamma",
    "delta"
]

# For intervention per_day_testing
default_per_day_testing_values={
    "symp_test":100.0,
    "quar_test":1.0,
    "sensitivity":1.0,
    "loss_prob":0,
    "test_delay":0,
    "start_day":0,
    "quar_policy":None
}

# For intervention testing probability
default_prob_testing_values={
    "asymp_prob":0.0,
    "sensitivity":1.0,
    "loss_prob":0.0,
    "test_delay":0,
    "start_day":0,
    "quar_policy":'start'
}
default_contact_tracing_values={
    "start_day":0,
    "presumptive":False,
    "quar_period":None,
    "capacity":None
}

default_vaccinate_probability_values={
    "booster":False,
    "prob":None
}
default_vaccinate_distribution_values={
    "booster":False
}

default_simple_vaccination_values={
    "prob":1.0,
    "rel_sus":0.0,
    "rel_symp":0.0
}

vaccine_keys=[
    "nab_eff",
    "nab_init",
    "nab_boost",
    "target_eff",
    "doses",
    "interval"
]

# Default input folder structure for grid sending
input_folder_structure={
    "input_data":
    {
        "data":[],
        "original_confs":[],
        "synthpops_input_data":[],
        "simulation_configuration_files":[],
        "synthpops_configuration_files":[],
        "simulation_immunity_files":[]
    },
    "output_data":
    {
        "Simulation":
        {
            "Configuration":[],
            "output_reports":[],
            "pop_configurations":[],
            "pops":[],
            "sims":[]
        }
    }            
}

config_list=["mainconfig","synthpops","simulation","report"]

# Simulation files
simulation_files_keys={
    "mobility":confkeys["mobility_pars"],
    "population":confkeys["population_pars"],
}

def base_local_input_path(user):
    """Returns the base path for the input folder of the user"""
    return f"/home/{user}/sandbox/meta/inputs"

def base_local_output_path(user):
    """Returns the base path for the output folder of the user"""
    return f"/home/{user}/sandbox/meta/outputs"

base_simulation_name="Simulation"

# grid default settings
grid_base_conf_name="grid_base_configuration"
grid_add_to_queue_name="grid_add_to_queue"
queue_default_path="/srv/queue.json"
grid_confkeys={"username":"username","server":"server","kerberos_user":"kerberos_user","remote_script_path":"remote_script_path",
               "input_path_server":"input_path_server","output_path_server":"output_path_server"}
grid_base_conf_structure={
    "username":"",
    "server":"",
    "input_path_server":"",
    "output_path_server":"",
}

# grid_data_sender_script="grid_send_data.sh"
# grid_credential_checker="grid_credentials_checker.sh"
grid_process_script="grid_process.sh"
grid_script_functions={
    "credentials":"check_credentials",
    "copy_to_remote":"scp_copy_to_remote",
    "send_qsub":"send_qsub_to_remote",
    "append_to_queue":"append_to_queue"
}
# Name of bash script to be remotely executed on grid
grid_start_pattern="meta_start_pattern.sh"
queue_download_config={
    "queue_list":[
     {      "user_name":"user_name",
            "local_location":"local_location",
            "remote_location":"remote_location",
            "error":False,
            "processed":False
     }
    ]
}

queue_download_config_single={
        "user_name":"user_name",
        "local_location":"local_location",
        "remote_location":"remote_location",
        "error":False,
        "processed":False
     }

# Confkeys list synthpops
synthpops_mobility_bool=["pop_creator_settings","pop_creator","input_data_global","mobility_data","value"]
synthpops_mobility_confkeys=["pop_creator_settings","pop_creator","input_data_global","mobility_data"]
synthpops_creator_confkeys=["pop_creator_settings","pop_creator","pop_creator_file"]
synthpops_global_input_data_confkeys=["pop_creator_settings","pop_creator","input_data_global"]
synthpops_parameters_confkeys=["pop_creator_settings","parameters"]
synthpops_naming_confkeys=["pop_creator_settings","pop_output_naming"]

synthpops_data_files=[
    copy.deepcopy(synthpops_parameters_confkeys)+['filepath'],
    copy.deepcopy(synthpops_creator_confkeys)+['filepath'],
    copy.deepcopy(synthpops_global_input_data_confkeys)+['filepath'],
    copy.deepcopy(synthpops_mobility_confkeys)+['filepath']
] 

global_values=['default','all']

synthpops_region_csv_columns={
    "location_code":"location_code",
    "use":"use",
    "region_name":"region_name",
    "untrimmed_name":"untrimmed_name",
    "sheet_name":"sheet_name",
    "region_parent_name":"region_parent_name",
    "notes":"notes",
    "parent_dirpath":"parent_dirpath",
    "parent_filename":"parent_filename",
    "parent_filepath":"parent_filepath",
}
synthpops_input_files={
    "location_code":"location_code",
    "population_age_distributions":"population_age_distributions",
    "employment_rates_by_age":"employment_rates_by_age",
    "enrollment_rates_by_age":"enrollment_rates_by_age",
    "household_head_age_brackets":"household_head_age_brackets",
    "household_head_age_distribution_by_family_size":"household_head_age_distribution_by_family_size",
    "household_size_distribution":"household_size_distribution",
    "school_size_brackets":"school_size_brackets",
    "school_size_distribution":"school_size_distribution",
    "school_size_distribution_by_type":"school_size_distribution_by_type",
    "school_types_by_age":"school_types_by_age",
    "workplace_size_counts_by_num_personnel":"workplace_size_counts_by_num_personnel"
}

synthpops_region_pars_mapped={
    "region_name":"location_name",
    "data_provenance_notices":"data_provenance_notices",
    "reference_links":"reference_links",
    "citations":"citations",
    "notes":"notes",
    "region_parent_name":"parent",
}

synthpops_creator_pars_mapped={
        "pop_size":"n",
        "location_code":"location",
        "region_config_output_path":"region_config_path",
        "sheet_name":"sheet_name",
        "parent_config":"parent_config_path", # Not needed
        "region_name":"country_location",
        "config_dirpath":"config_dirpath", #Deprecated
}

synthpops_naming_keys_mapped={
    "value":"value",
    "pop_name_prefix":"pop_name_prefix",
    "pop_name_suffix":"pop_name_suffix",
    "pop_output_type":"pop_output_type",
    "pop_output_dirpath":"pop_output_dirpath",
    "pop_creator_dirpath":"pop_creator_dirpath",
}

synthpops_data_names=["pars_file.csv","synthpops_input_files.csv","synthpops_region.csv"]

default_synthpops_parent_configuration="data/Czechia.json"

# Confkeys list covasim
covasim_region_parameters_confkeys=["region_parameters"]
covasim_interventions_confkeys=["interventions"]
covasim_immunity_confkeys=["immunity"]
covasim_variants_confkeys=["variants"]
covasim_mobility_confkeys=["mobility"]
covasim_mobility_bool=["mobility","value"]
covasim_population_size_confkeys=["population_size"]
covasim_global_parameters_confkeys=["global_parameters"]
covasim_global_parameters=["global_parameters","pars"]

covasim_data_files=[
    copy.deepcopy(covasim_region_parameters_confkeys)+['filepath'],
    copy.deepcopy(covasim_interventions_confkeys)+['filepath'],
    copy.deepcopy(covasim_immunity_confkeys)+['filepath'],
    copy.deepcopy(covasim_variants_confkeys)+['filepath'],
    copy.deepcopy(covasim_mobility_confkeys)+['filepath'],
    copy.deepcopy(covasim_population_size_confkeys)+['filepath'],
    copy.deepcopy(covasim_global_parameters_confkeys)+['filepath']
]

covasim_immunity_files=[    
    "vaccine_dose_pars",
    "vaccine_variant_pars",
    "variant_pars",
    "variant_cross_immunity"
]

covasim_region_csv_columns={
    "location_code":"location_code",
    "use":"use",
    "region_parent_name":"region_parent_name",
    "name":"name",
    "popfile":"popfile",
    "pop_infected":"pop_infected",
    "pop_size":"pop_size",
    "rand_seed":"rand_seed",
    "pop_scale":"pop_scale",
    "beta":"beta",
    "asymp_factor":"asymp_factor",
    "n_imports":"n_imports",
    "use_waning":"use_waning",
    "nab_boost":"nab_boost",
    "rel_beta":"rel_beta",
    "rel_symp_prob":"rel_symp_prob",
    "rel_severe_prob":"rel_severe_prob",
    "rel_crit_prob":"rel_crit_prob",
    "rel_death_prob":"rel_death_prob",
    "prog_by_age":"prog_by_age",
    "iso_factor":"iso_factor",
    "quar_factor":"quar_factor",
    "quar_period":"quar_period",
    "n_beds_hosp":"n_beds_hosp",
    "n_beds_icu":"n_beds_icu",
    "no_hosp_factor":"no_hosp_factor",
    "no_icu_factor":"no_icu_factor",
}

covasim_check_consistency_keys=[
    "use_waning",
    "pop_scale",
    "n_days",
    "start_day",
    "end_day"
]

covasim_intervention_exclude_keys=[
    "location_code",
    "use",
    "intervention_type"
]

covasim_intervention_list_keys=[
    "beta_change",
    "num_days",
    "layers",
    "changes"
]

covasim_exclude_simulation_pars=[
    "use",
    "location_code",
    "region_parent_name",
    'unique_mobility_indexes',
]

covasim_global_keys=covasim_pars_all

covasim_default_datetime="2020-03-01"
covasim_datetime_format="%Y-%m-%d"

valid_true_values=[1,"1",True,"True","true"]

intervention_names_mapping={
    "beta_change":"beta_change",
    "mobility_change":"mobility_change",
    "isolate_contacts":"isolate_contacts",
    "per_day_testing":"per_day_testing",
    "testing_probability":"testing_probability",
    "contact_tracing":"contact_tracing",
    "vaccinate_probability":"vaccinate_probability",
    "vaccinate_distribution":"vaccinate_distribution",
    "simple_vaccination":"simple_vaccination",
    "base_vaccination":"base_vaccination"
}

intervention_mapping={
    "beta_change":{
        "keys":interventions['beta_change'],  
        "defaults":None,
    },
    "mobility_change":{
        "keys":interventions['mobility_change'],  
        "defaults":None,
    },
    "isolate_contacts":{
        "keys":interventions['isolate_contacts'],
        "defaults":None,
    },
    "per_day_testing":{
        "keys":interventions['per_day_testing'],
        "defaults":default_per_day_testing_values, 
    },
    "testing_probability":{
        "keys":interventions['testing_probability'],
        "defaults":default_prob_testing_values,
    },
    "contact_tracing":{
        "keys":interventions['contact_tracing'],
        "defaults":default_contact_tracing_values,
    },
    "vaccinate_probability":{
        "keys":interventions['vaccinate_probability'],
        "defaults":default_vaccinate_probability_values,
    },
    "vaccinate_distribution":{
        "keys":interventions['vaccinate_distribution'],
        "defaults":default_vaccinate_probability_values,
    }
    # Simple vaccination TODO
    # "simple_vaccination":{
    #     "keys":interventions['simple_vaccination'],
    #     "defaults":default_simple_vaccination_values,
    #     "function":cv.simple_vaccine
    # }
}

default_multisim_object_rel_path="sims/simulation.msim"

grid_dict_info={
    "default_base_directory":"ABM_share_meta",
    "input_directory":"input_data",
    "output_auto_settings":"output_data"
}

grid_configuration_extensions=["json","yaml","yml"]
grid_csv_extensions=["csv","xlsx"]
grid_conf_replace_keys=['filepath','mobility_filepath','mobility_path','parent_location','location']
grid_csv_replace_keys=list(synthpops_input_files.keys())[1:]
grid_csv_immunity_replace_keys=['vaccine_dose_pars','vaccine_variant_pars','variant_pars','variant_cross_immunity']
grid_conf_replace_keys.extend(['parent_filepath','popfile','parent_dirpath'])
