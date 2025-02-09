import abmshare.validator.validator_defaults as vd
import abmshare.utils as exut
import abmshare.defaults as exdf
from abmshare.validator.validator_defaults import TypeValidationError
import pandas as pd


def validate_simulation_csv(filepath:str,rule:dict,keys:list):
    if exdf.covasim_region_parameters_confkeys in keys:
        if not exut.file_validator(filepath):
            raise FileNotFoundError(f"File {filepath} does not exist in configuration file;{filepath}")
        df = exut.load_csv(filepath)
    elif any(
        confkey in keys
        for confkey in [
            exdf.covasim_interventions_confkeys,
            exdf.covasim_immunity_confkeys,
            exdf.covasim_mobility_confkeys,
            exdf.covasim_population_size_confkeys,
            exdf.covasim_global_parameters_confkeys
        ]
    ):
        pass
    else:
        raise Exception("Unknown file. Cannot proceed.")

def validate_csv(df:pd.DataFrame|str,base_keys_dict_with_values:dict,empty_allowed:list=None,check_files:list=None):
    if isinstance(df,str):
        filepath=df
        df=exut.load_datafile(df)
    param_keys=set(base_keys_dict_with_values.keys())
    csv_columns=set(df.columns)
    unmatched_columns=csv_columns- param_keys

    if unmatched_columns: # if there is some column, which cannot be used
        print(f"Columns {unmatched_columns} are not defined for use.")

    # Skip theese columns, defined by other functions
    #NOTE: for future processing
    skip_columns=[]
    
    for col in df.columns:
        if col in base_keys_dict_with_values.keys():
            expected_type = base_keys_dict_with_values[col] if not isinstance(base_keys_dict_with_values[col],list) else tuple(base_keys_dict_with_values[col])
            for value in df[col]:
                try:
                    if col in skip_columns: # Skip theese columns
                        pass
                    elif check_files and isinstance(value,expected_type) and col in check_files: # Check for the files, if they are string                        
                        if not exut.file_validator(value):
                            raise FileExistsError(f"File {value} does not exist in configuration file:{filepath}")
                    elif isinstance(expected_type,list) and type(value) in expected_type and pd.notna(value): # If there is more than one type allowed
                        pass
                    elif not isinstance(expected_type,list) and isinstance(value,expected_type) and pd.notna(value): # if there is only one type
                        pass
                    elif col in empty_allowed and pd.isna(value): # if the value is empty and allowed
                        pass
                    else: # If there is a problem                         
                        raise TypeValidationError(f"Value {value} in column {col} on the is not of type {expected_type}. This can throw errors later on. Check it in file {filepath}")
                except Exception as e:
                    print(f"{e}")

def validate_interventions_csv(filepath:str,intervention_dict:list):
    df=exut.load_datafile(filepath)
    csv_columns=set(df.columns)
    datetime_columns=['start_day','end_day','num_days']
    for i,row in df.iterrows():
        time_validated=False
        # check if intervention is enabled. do not control inetventions which are off
        if not row['use']: continue
        # check if intervention type has more allowed variable types                
        if row['intervention_type'] in intervention_dict.keys(): intervention_type=intervention_dict[row['intervention_type']] 
        else:raise TypeValidationError(f"Intervention type {row['intervention_type']} is not allowed on row number:{i}")
        # hard way to fix the daily_tests value in the csv
        if 'daily_tests' in intervention_type.keys() and 'daily_tests' in csv_columns:
            try:
                row['daily_tests']=int(row['daily_tests'])
            except:
                print(f"Cannot convert daily_tests value {row['daily_tests']} to int on row number {i}")
        for col in csv_columns:            
            # If the col is allowed for this intervention
            if col in intervention_type:
                # Prepare variables, if len of list >1, then make it to touple for isinstance validation
                if isinstance(intervention_type[col]['allowed_type'], list) and len(intervention_type[col]['allowed_type'])>1: intervention_type[col]['allowed_type']=tuple(intervention_type[col]['allowed_type'])
                # Check if the row[col] value should be list and is like a string / and edit it 
                if isinstance(row[col],str) and isinstance(intervention_type[col]['allowed_type'],tuple) and list in intervention_type[col]['allowed_type']:
                    row[col]=exut.convert_string_lists(row[col])                    
                # if it is datetime check separately
                if col in datetime_columns and time_validated==False:
                    time_validated=validate_time(intervention_type,row,datetime_columns,i,time_validated)
                    intervention_type={x:y for x,y in intervention_type.items() if x not in datetime_columns} if time_validated else intervention_type
                # If row has value
                elif row[col]:
                    # if row have correct type value
                    if isinstance(row[col],intervention_type[col]['allowed_type']):
                        pass
                    # if its optional
                    elif intervention_type[col]['optional']:
                        pass                        
                    else:
                        raise TypeValidationError(f"Column {col} is not of type {intervention_type[col]['allowed_type']} in intervention type {row['intervention_type']} on row number:{i}")
                # If row has not value
                else:
                    # if row should have value
                    if not intervention_type[col]['optional']:
                        raise TypeValidationError(f"Column {col} is neccessary, and is not filled in intervention type {row['intervention_type']} on row number:{i}")
            # Check if is it time columns, which has been already validated to be OK
            elif col in csv_columns and time_validated:
                pass
            # Check if the columns is not allowed and also dont have value
            elif col not in intervention_type and pd.isna(row[col]):
                pass
            else: # Is the column has value and it should not have one                             
                raise TypeValidationError(f"Column {col} is not allowed in intervention type {row['intervention_type']} on row number:{i}")                

def validate_time(intervention_type:dict,row:pd.Series,datetime_columns:list,i:int,time_validated:bool):
    if not (((row['start_day'] and row['end_day']) or row['start_day'] or row['num_days']) and (all([intervention_type[col]['optional'] for col in datetime_columns])) or not all([intervention_type[col]['optional'] for col in datetime_columns])):
        raise TypeValidationError(f"There is a problem on row number {i} for intervention: {row['intervention_type']} has problem with start day, end day or num_days. Check it. Look for more info in documentation")
    return True

def run_test(path:str|dict):
    if isinstance(path,str):
        validate_csv(path,vd.share_extension_json_validation)
    elif isinstance(path,dict):
        for k,v in path.items():
            validate_csv(k,v)
        

# if __name__=="__main__":
#     jsons={
#         '/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/new_simulation.json':vd.simulation_json_validation,
#         # '/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/report_configuration.json':vd.report_json_validation,
#         # '/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/synthpops_configuration.json':vd.synthpops_json_validation,
#         # '/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/share_extension_configuration.json':vd.share_extension_json_validation
#     }
#     # test_path="/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/new_simulation.json"
#     # test_csv_path="/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/data/simulation/simulation_region_pars.csv"
#     # test_csv_path="/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/data/simulation/simulation_interventions.csv"
#     test_csv_path="/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/data/simulation/simulation_interventions.csv"
#     intervention_validation=validate_interventions_csv(test_csv_path,vd.simulation_interventions_csv_cols_with_types) # Synthpops region parameters
    
    
#     #TODO: VALIDATE SYNTHPOPS CSVS, 
#     #NOTE: and ADDED two new arguments to the function
#     # meh=validate_json(test_path,vd.simulation_json_validation, vd.simulation_empty_allowed)

#     # test_csv_path="/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/data/synthpops_input_files.csv"
#     # synthpops_validation=validate_csv(test_csv_path,vd.synthpops_input_files_cols,check_files=vd.synthpops_input_files_files) # Synthpops input files #NOTE:DONE 

#     # test_csv_path="/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/data/synthpops_region.csv"
#     # synthpops_region_validation=validate_csv(test_csv_path,vd.synthpops_region_cols,check_files=vd.synthpops_region_config_files,empty_allowed=vd.synthpops_empty_allowed) # Synthpops region parameters

#     # test_csv_path="/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/data/pars_file.csv"
#     # synthpops_pars_file=validate_csv(test_csv_path,vd.synthpops_pars_cols,empty_allowed=vd.synthpops_empty_allowed) # Synthpops pars parameters
#     # simulation_validation=validate_csv(test_csv_path,vd.simulation_region_csv_cols_with_types)
#     print()
#     pass