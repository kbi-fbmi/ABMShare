import abmshare.validator.validator_defaults as vd
import abmshare.utils as exut
import abmshare.validator.json_validator as jv
import abmshare.validator.csv_validator as cv


def process(main_config:str|dict,simulation_config:str|dict=None,synthpops_config:str|dict=None,report_config:str|dict=None):
    # First validate configs, then csvs
    jv.validate_json(main_config,vd.share_extension_json_validation)
    if simulation_config:
        #Validate Json
        jv.validate_json(simulation_config,vd.simulation_json_validation)
        files=exut.get_all_csv_files(simulation_config,vd.simulation_data_files,return_dict=True)
        #Validate CSVS
        # Validate simulation_region_pars
        if 'region_parameters' in files:
            cv.validate_csv(files['region_parameters'],base_keys_dict_with_values=vd.simulation_region_csv_cols_with_types,
                            empty_allowed=vd.simulation_empty_allowed,check_files=vd.simulation_input_files)
        # Validate simulation global_pars
        if 'global_parameters' in files:
            cv.validate_csv(files['global_parameters'],base_keys_dict_with_values=vd.simulation_region_csv_cols_with_types,
                            empty_allowed=vd.simulation_empty_allowed,check_files=vd.simulation_input_files)
        # Validate simulation_interventions
        if 'interventions' in files: 
            cv.validate_interventions_csv(files['interventions'],vd.simulation_interventions_csv_cols_with_types)
        # Validate simulation variants #TODO:

        # Validate simulation Vaccines #TODO:
        print("Simulation config has been validated")
    if synthpops_config:
        jv.validate_json(synthpops_config,vd.synthpops_json_validation)
        files=exut.get_all_csv_files(synthpops_config,vd.synthpops_data_files,return_dict=True,filenames=vd.synthpops_data_files_names)
        # Validate parameters synthpops data file
        if 'pop_creator_file' in files:
            cv.validate_csv(files["pop_creator_file"],vd.synthpops_region_cols,empty_allowed=vd.synthpops_empty_allowed)            
        if "input_data_global" in files:
            cv.validate_csv(files['input_data_global'],vd.synthpops_input_files_cols,check_files=vd.synthpops_input_data_files) 
        # Validate pop creator pars
        if "parameters" in files:
            cv.validate_csv(files['parameters'],vd.synthpops_pars_cols,check_files=vd.synthpops_region_config_files,
                empty_allowed=vd.synthpops_empty_allowed)            
        print("Synthetic population config has been validated")
    # if report_config: # Need to fix it 
    #     jv.validate_json(report_config,vd.report_json_validation,report_conf=True)
    #     print("Report config has been validated")
    #TODO: Someday combinations of synthpop + covasim
        print("Validation of input files was successful")
        

# if __name__=="__main__":
#     jsons={
#         '/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/new_simulation.json':vd.simulation_json_validation,
#         '/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/report_configuration.json':vd.report_json_validation,
#         '/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/synthpops_configuration.json':vd.synthpops_json_validation,
#         '/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/share_extension_configuration.json':vd.share_extension_json_validation
#     }
#     simpath="/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/new_simulation.json"
#     synthpath="/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/synthpops_configuration.json"
#     reportpath="/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/report_configuration.json"
#     # meh=validate_json(test_path,vd.simulation_json_validation)
#     # meh2=run_test(jsons)
#     process('/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/share_extension_configuration.json',
#             simpath,
#             synthpath,
#             reportpath
#             )
#     print()
#     pass