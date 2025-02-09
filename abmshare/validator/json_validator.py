import abmshare.utils as exut


def validate_type(value, expected_type, optional=False,filename:str=None,keys:list=None):
    if not isinstance(value, expected_type['type']):
        if optional:
            print("There is a problem with an optional value")
        else:
            print(f"Expected {expected_type} but got {type(value)} in file:{filename} on keys:{keys}")


def validate_end_with(value, expected_endings,filename:str=None,keys:list=None):
    if not isinstance(value, str):
        if expected_endings['optional']:
            print(f"There is a problem with an optional value in {value}")
        else:
            print(f"Expected a string but got {type(value)}")
    if (value=="" or value is None) and expected_endings['optional']:   
        pass
    elif not any(value.endswith(ending) for ending in expected_endings['allowed']):
        print(f"Expected the string to end with one of {expected_endings['allowed']}, but got {value}")

def validate_if_file_exists(value,filename:str):
        if not exut.file_validator(value): print(f"File {value} does not exist in configuration file;{filename}")

def validate_json(data:str| dict,rule:dict,config_name:str=None,keys:list=[],report_conf=False):
    if isinstance(data, str):
        config_name=exut.get_filename(data)  
        try: # Hotfix for reportconf
            data = exut.load_config(data)
        except Exception as e:
            if report_conf:
                pass
            else:
                print(f"Could not load file {data} with error {e}")
            return
        keys=[]        
    for key, val in data.items():
        keys.append(key)
        if isinstance(val,dict) and "type" not in val.keys(): # If it needs to recursively do deeper
            keys=validate_json(val,rule[key],config_name,keys=keys,report_conf=report_conf)
        elif isinstance(val,dict) and "type" in val.keys(): # If its the last level
            if val["optional"]==True and not data[key]:# If its optional and not there, skip 
                pass
            elif val["optional"]==True and data[key]: # If its optional and there, validate
                validate_type(data[key],rule[key],optional=True,filename=config_name,keys=keys)
                keys=[]
            if val['type']!=rule[key]:
                print(f"Expected {rule[key]} but got {val['type']} in configuration: {config_name}")
        elif isinstance(val,list): # If its a list, validate each element
            for i in val:
                keys=validate_json(i,rule[key],config_name,keys=keys,report_conf=report_conf)
        elif key=="filepath" and val!="": # Validate type and ending
            validate_type(data[key],rule[key],filename=config_name,keys=keys)
            validate_end_with(data[key],rule[key],filename=config_name,keys=keys)            
            validate_if_file_exists(data[key],filename=config_name)
            keys=[]
        else: # if its not a dict, just validate
            validate_type(data[key],rule[key],filename=config_name,keys=keys)
            keys=[]
    return keys
