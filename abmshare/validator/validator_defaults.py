import abmshare.defaults as exdf


class ValidationError(Exception):
    pass

class TypeValidationError(ValidationError):
    pass

class MissingKeyError(ValidationError):
    pass

class InvalidCombinationError(ValidationError):
    pass

simulation_json_validation={
    "parallel_run": {"type": bool},
    "test":{"type":bool,"optional":True},
    "region_parameters": {"filepath": {"type": str, "allowed": (".csv",".xlsx")}},
    "interventions": {"filepath": {"type": str, "allowed": (".csv",".xlsx"),"optional":True}},
    "variants": {"filepath": {"type": str, "allowed": (".csv",".xlsx"),"optional":True}},
    "immunity": {"filepath": {"type": str, "allowed": (".csv",".xlsx"),"optional":True}},
    "mobility": {
        "value": {"type": bool},
        "filepath": {"type": str, "allowed": (".csv",".xlsx"),
        "optional":True},
    },
    "population_size": {"filepath": {"type": str, "allowed": (".csv",".xlsx")}},
    "global_parameters": {
        "pars": {
            "n_days": {"type": int, "optional": True},
        },
        "filepath": {"type": str, "allowed": (".csv",".xlsx"),
                     "optional":True},
    },
}

synthpops_json_validation = {
    "parallel_run": {"type": bool},
    "test": {"type": bool, "optional": True},
    "pop_creator_settings": {
        "pop_output_naming": {
            "value": {"type": bool},
            "pop_name_prefix": {"type": str, "optional": True},
            "pop_name_suffix": {"type": str, "optional": True},
            "pop_output_type": {"type": str},
            "pop_output_dirpath": {"type": str, "optional": True},
            "pop_creator_dirpath": {"type": str, "optional": True},
        },
        "parameters": {
            "filepath": {"type": str, "allowed": (".csv", ".xlsx")},
        },
        "pop_creator": {
            "pop_creator_file": {
                "value": {"type": bool},
                "filepath": {"type": str, "allowed": (".csv", ".xlsx")},
            },
            "input_data_global": {
                "value": {"type": bool},
                "filepath": {"type": str, "allowed": (".csv", ".xlsx")},
                "mobility_data": {
                    "value": {"type": bool},
                    "filepath": {"type": str, "allowed": (".csv", ".xlsx")},
                },
            },
        },
    },
}

share_extension_json_validation = {
    "initialize": {
        "synthpop_initialize": {"type": bool},
        "simulation_initialize": {"type": bool},
        "report_module_initialize": {"type": bool},
        "test":{ "type": bool, "optional": True},
    },
    "auto_save_settings": {
        "value": {"type": bool},
        "auto_increment": {"type": bool},
        "dirname": {"type": str},
        "location": {"type": str},
        "copy_files": {
            "copy_loaded_pop": {"type": bool},
        },
    },
    "synthpops_settings": {
        "filepath": {"type": str, "allowed": (".json",".yaml")},
    },
    "simulation_settings": {
        "filepath": {"type": str, "allowed": (".json",".yaml")},
        "test": {"type": bool, "optional": True},
    },
    "report_settings": {
        "filepath": {"type": str, "allowed": (".json",".yaml")},
    },
}

report_json_validation = {
    "create_report": {"type": bool},
    "output_format": {"type": str, "allowed": ["csv", "xlsx"]},
    "output_path": {"type": str, "optional": True},
    "input_multisim": {
            "filepath": {"type": str, "optional": True},
            "all_keys": {"type": bool},
            "keys": {"type": list, "element_type": str},
            "whole_simulation": {"type": bool},
            "separated_simulation": {"type": bool},
            "whole_variants": {"type": bool},
            "separated_variants": {"type": bool},
    },
    "reports": {
            "keys": {"type": list, "element_type": str,"optional":True},
            "output_format": {"type": str, "optional": True, "allowed": ["csv", "xlsx"]},
            "filename": {"type": str, "optional": True},
    },
}

simulation_data_files=exdf.covasim_data_files

simulation_data_files_names=[x[0] for x in exdf.covasim_data_files]
# [
#     exdf.covasim_region_parameters_confkeys,
#     exdf.covasim_interventions_confkeys,
#     exdf.covasim_variants_confkeys,
#     exdf.covasim_mobility_confkeys,
#     exdf.covasim_population_size_confkeys,
#     exdf.covasim_global_parameters_confkeys
# ]]

simulation_input_files=["popfile"]

simulation_region_cols={
    "location_code":str,
    "use":[bool,str],
    "region_parent_name":str,
    "name":str,
    "popfile":str,
}

simulation_parameters = {
    "pop_size": int,
    "unique_mobility_indexes":bool,
    "pop_infected": int,
    "pop_type": str,
    "location": str,
    "start_day": str,
    "end_day": str,
    "n_days": int,
    "rand_seed": int,
    "verbose": int,
    "pop_scale": float,
    "scaled_pop": int,
    "rescale": bool,
    "rescale_threshold": float,
    "rescale_factor": float,
    "beta": float,
    "n_imports": int,
    "beta_dist": [str,dict],  # or dict, depending on the representation of the distribution
    "viral_dist": [str,dict],  # or dict
    "asymp_factor": float,
    "contacts": [dict,list],  # or list, depending on structure
    "dynam_layer": [dict,list],  # or list
    "beta_layer": [dict,list],  # or list
    "use_waning": bool,
    "nab_init": [dict,list],  # or list
    "nab_decay": [dict,list],  # or list
    "nab_kin": [dict,list],  # or list
    "nab_boost": float,
    "nab_eff": [dict,list],  # or list
    "rel_imm_symp": [dict,list],  # or list
    "immunity": [dict,list],  # or list
    "exp2inf": float,
    "inf2sym": float,
    "sym2sev": float,
    "asym2rec": float,
    "mild2rec": float,
    "sev2rec": float,
    "crit2rec": float,
    "crit2die": float,
    "rel_symp_prob": float,
    "rel_severe_prob": float,
    "rel_crit_prob": float,
    "rel_death_prob": float,
    "prog_by_age": bool,
    "prognoses": [dict,list],  # or list
    "iso_factor": float,
    "quar_factor": float,
    "quar_period": int,
    "interventions": list,
    "analyzers": list,
    "timelimit": int,
    "n_beds_hosp": int,
    "n_beds_icu": int,
    "no_hosp_factor": float,
    "no_icu_factor": float,
}


simulation_region_csv_cols_with_types= {**simulation_region_cols,**simulation_parameters}
simulation_empty_allowed=[
    "popfile",
    "pop_size",
    "pop_infected",
    "pop_type",
    "location",
    "start_day",
    "end_day",
    "n_days",
    "rand_seed",
    "verbose",
    "pop_scale",
    "scaled_pop",
    "rescale",
    "rescale_threshold",
    "rescale_factor",
    "beta",
    "n_imports",
    "beta_dist",
    "viral_dist",
    "asymp_factor",
    "contacts",
    "dynam_layer",
    "beta_layer",
    "use_waning",
    "nab_init",
    "nab_decay",
    "nab_kin",
    "nab_boost",
    "nab_eff",
    "rel_imm_symp",
    "immunity",
    "exp2inf",
    "inf2sym",
    "sym2sev",
    "asym2rec",
    "mild2rec",
    "sev2rec",
    "crit2rec",
    "crit2die",
    "rel_symp_prob",
    "rel_severe_prob",
    "rel_crit_prob",
    "rel_death_prob",
    "prog_by_age",
    "prognoses",
    "iso_factor",
    "quar_factor",
    "quar_period",
    "interventions",
    "analyzers",
    "timelimit",
    "n_beds_hosp",
    "n_beds_icu",
    "no_hosp_factor",
    "no_icu_factor",
]

simulation_interventions_csv_cols_with_types = {
    "mobility_change": {
        "location_code": {"allowed_type": str, "optional": False},
        "use": {"allowed_type": bool, "optional": False, "default": True},
        "intervention_type": {"allowed_type": str, "optional": False, "default": "mobility_change"},
        "label": {"allowed_type": str, "optional": True},
        "start_day": {"allowed_type": [str, int], "optional": False},
        "end_day": {"allowed_type": [str, int], "optional": False},
        "num_days": {"allowed_type": [int, list], "optional": False},
    },
    "beta_change": {
        "location_code": {"allowed_type": str, "optional": False},
        "use": {"allowed_type": bool, "optional": False, "default": True},
        "intervention_type": {"allowed_type": str, "optional": False, "default": "beta_change"},
        "label": {"allowed_type": str, "optional": True},
        "start_day": {"allowed_type": [str, int], "optional": False},
        "end_day": {"allowed_type": [str, int], "optional": False},
        "num_days": {"allowed_type": [int, list], "optional": False},
        "beta_change": {"allowed_type": [float, list], "optional": False},
        "layers": {"allowed_type": list, "optional": True},
    },
    "isolate_contacts": {
        "location_code": {"allowed_type": str, "optional": False},
        "use": {"allowed_type": bool, "optional": False, "default": True},
        "intervention_type": {"allowed_type": str, "optional": False, "default": "isolate_contacts"},
        "label": {"allowed_type": str, "optional": True},
        "num_days": {"allowed_type": [int, list], "optional": False},
        "changes": {"allowed_type": [float, list], "optional": False},
        "layers": {"allowed_type": list, "optional": False},
        "start_day": {"allowed_type": [str, int], "optional": False},
        "end_day": {"allowed_type": [str, int], "optional": False},
    },
    "per_day_testing": {
        "location_code": {"allowed_type": str, "optional": False},
        "use": {"allowed_type": bool, "optional": False, "default": True},
        "intervention_type": {"allowed_type": str, "optional": False, "default": "per_day_testing"},
        "label": {"allowed_type": str, "optional": True},
        "daily_tests": {"allowed_type": [int, list], "optional": False},
        "symp_test": {"allowed_type": float, "optional": True, "default": 100.0},
        "quar_test": {"allowed_type": float, "optional": True, "default": 1.0},
        "quar_policy": {"allowed_type": str, "optional": True},
        "subtarget": {"allowed_type": dict, "optional": True},
        "ili_prev": {"allowed_type": [float, list], "optional": True},
        "sensitivity": {"allowed_type": float, "optional": True, "default": 1.0},
        "loss_prob": {"allowed_type": float, "optional": True, "default": 0},
        "test_delay": {"allowed_type": int, "optional": True, "default": 0},
        "start_day": {"allowed_type": [int,str], "optional": True, "default": 0},
        "end_day": {"allowed_type": [int,str], "optional": True},
        "num_days": {"allowed_type": [int, list], "optional": False},
    },
    "testing_probability": {
        "location_code": {"allowed_type": str, "optional": False},
        "use": {"allowed_type": bool, "optional": False, "default": True},
        "intervention_type": {"allowed_type": str, "optional": False, "default": "testing_probability"},
        "label": {"allowed_type": str, "optional": True},
        "symp_prob": {"allowed_type": float, "optional": False},
        "asymp_prob": {"allowed_type": float, "optional": True, "default": 0.0},
        "symp_quar_prob": {"allowed_type": float, "optional": True},
        "asymp_quar_prob": {"allowed_type": float, "optional": True},
        "quar_policy": {"allowed_type": str, "optional": True},
        "subtarget": {"allowed_type": dict, "optional": True},
        "ili_prev": {"allowed_type": [float, list], "optional": True},
        "sensitivity": {"allowed_type": float, "optional": True, "default": 1.0},
        "loss_prob": {"allowed_type": float, "optional": True, "default": 0.0},
        "test_delay": {"allowed_type": int, "optional": True, "default": 0},
        "start_day": {"allowed_type": [int,str], "optional": True, "default": 0},
        "end_day": {"allowed_type": [int,str], "optional": True},
        "num_days": {"allowed_type": [int, list], "optional": False},
    },
    "contact_tracing": {
        "location_code": {"allowed_type": str, "optional": False},
        "use": {"allowed_type": bool, "optional": False, "default": True},
        "intervention_type": {"allowed_type": str, "optional": False, "default": "contact_tracing"},
        "label": {"allowed_type": str, "optional": True},
        "trace_probs": {"allowed_type": [float, dict], "optional": True, "default": 0.4},
        "trace_time": {"allowed_type": [float, dict], "optional": True, "default": 0},
        "start_day": {"allowed_type": [int,str], "optional": True, "default": 0},
        "end_day": {"allowed_type": [int,str], "optional": True},
        "presumptive": {"allowed_type": bool, "optional": True, "default": False},
        "capacity": {"allowed_type": int, "optional": True},
        "quar_period": {"allowed_type": int, "optional": True},
        "num_days": {"allowed_type": [int, list], "optional": True},
    },
    "vaccinate_distribution":
    {
        "location_code": {"allowed_type": str, "optional": False},
        "use": {"allowed_type": bool, "optional": False, "default": True},
        "start_day": {"allowed_type": [int,str], "optional": True, "default": 0},
        "intervention_type": {"allowed_type": str, "optional": False, "default": "vaccinate_distribution"},
        "end_day": {"allowed_type": [int,str], "optional": True},
        "num_days": {"allowed_type": [int, list], "optional": True},
        "vaccine":{ "allowed_type": str, "optional": False},
        "num_doses":{ "allowed_type": [int,float], "optional": False},
        "booster":{ "allowed_type": bool, "optional": True, "default": False},
        "sequence":{ "allowed_type": str, "optional": True},
        "label":{ "allowed_type": str, "optional": True},
    },
    "simple_vaccination":
    {
        "location_code": {"allowed_type": str, "optional": False},
        "use": {"allowed_type": bool, "optional": False, "default": True},
        "label":{ "allowed_type": str, "optional": True},
        "intervention_type": {"allowed_type": str, "optional": False, "default": "simple_vaccination"},
        "start_day": {"allowed_type": [int,str], "optional": True, "default": 0},
        "end_day": {"allowed_type": [int,str], "optional": True},
        "num_days": {"allowed_type": [int, list], "optional": True},
        "rel_sus":{ "allowed_type": float, "optional": False},
        "rel_symp":{ "allowed_type": float, "optional": False},
        "prob":{ "allowed_type": float, "optional": True},
    },

}



# Synthpops part
synthpops_input_files_cols={x:str for x in exdf.synthpops_input_files.values()}
synthpops_input_data_files=[x for x in exdf.synthpops_input_files.values() if x !="location_code"]

synthpops_region_cols={
    "location_code":str,
    "use":bool,
    "region_name":str,
    "untrimmed_name":str,
    "sheet_name":str,
    "region_parent_name":str,
    "notes":str,
    "parent_dirpath":str,
    "parent_filename":str,
    "parent_filepath":str,
}

synthpops_region_config_files=exdf.synthpops_region_csv_columns["parent_filepath"]
synthpops_pars_cols={
    "location_code":str,
    "n": int,  # The number of people to create
    "ltcf_pars": dict,  # LTCF parameters, if supplied
    "school_pars": dict,  # School parameters, if supplied
    "with_industry_code": bool,  # Assign industry codes for workplaces (US only)
    "with_facilities": bool,  # Create long term care facilities (US only)
    "use_default": bool,  # Use default data from settings
    "use_two_group_reduction": bool,  # LTCF with reduced contacts across groups
    "average_LTCF_degree": float,  # Average degree in LTCFs
    "ltcf_staff_age_min": int,  # LTCF staff minimum age
    "ltcf_staff_age_max": int,  # LTCF staff maximum age
    "with_school_types": bool,  # Creates explicit school types
    "school_mixing_type": "random" or "age_clustered" or "age_and_class_clustered",  # Mixing type for schools
    "average_class_size": float,  # Average classroom size
    "inter_grade_mixing": float,  # Fraction of edges rewired between grades in the same school
    "average_student_teacher_ratio": float,  # Average number of students per teacher
    "average_teacher_teacher_degree": float,  # Average number of contacts per teacher with other teachers
    "teacher_age_min": int,  # Minimum age for teachers
    "teacher_age_max": int,  # Maximum age for teachers
    "with_non_teaching_staff": bool,  # Includes non-teaching staff
    "average_student_all_staff_ratio": float,  # Average number of students per all staff members at school
    "average_additional_staff_degree": float,  # Average number of contacts per additional non-teaching staff
    "staff_age_min": int,  # Minimum age for non-teaching staff
    "staff_age_max": int,  # Maximum age for non-teaching staff
    "rand_seed": int,  # Random sequence start point
    "country_location": str,  # Country name
    "state_location": str,  # State name
    "location": str,  # Location name
    "sheet_name": str,  # Sheet name for data
    "household_method": str,  # Household generation method
    "smooth_ages": bool or str,  # Use smoothed age distribution
    "window_length": int,  # Window length for age distribution smoothing
    "do_make": bool,  # Whether to make the population
}

synthpops_empty_allowed=[
    #Region pars
    exdf.synthpops_region_csv_columns["parent_dirpath"],
    exdf.synthpops_region_csv_columns["parent_filename"],
    exdf.synthpops_region_csv_columns["parent_filepath"],
    exdf.synthpops_region_csv_columns["notes"],
    #Pars cols
    "n",
    "ltcf_pars",
    "school_pars",
    "with_industry_code",
    "with_facilities",
    "use_default",
    "use_two_group_reduction",
    "average_LTCF_degree",
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
    "window_length",
    "do_make",
]

synthpops_data_files=exdf.synthpops_data_files
synthpops_data_files_names=[
    "pop_creator_file",
    "input_data_global",
    "parameters",
]
# simulation_data_files=[x[0] for x in exdf.covasim_data_files]
