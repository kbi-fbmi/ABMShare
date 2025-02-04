from cryptography.fernet import Fernet
import abmshare.utils as exut
import abmshare.defaults as exdf
import json
import subprocess
import os
from datetime import datetime
from dateutil import parser
import pandas as pd
import shutil



def generate_key(path:str=None):
    """Generate a key and save it into a file"""
    path=path or exut.merge_default_path(".key/key")
    key = Fernet.generate_key()
    with open(path, "wb") as key_file:
        key_file.write(key)

def load_key(path:str=None):
    path = path or exut.merge_default_path(".key/key")
    return open(path, "rb").read()

def generate_data(username:str=None,server:str=None,kerberos_user:str=None,input_path:str=None,output_path:str=None,server_script:str=None):
    data=exdf.grid_base_conf_structure
    data['username']=username or input(f"\nAdd server ssh username: ")
    data['server']=server or input(f"\nAdd ssh server name: ")
    data['kerberos_user']=kerberos_user or input(f"\nAdd kerberos user name: ") # Main name for sudo user
    data['input_path_server']=input_path or input(f"\nAdd ssh input path directory: ")
    data['output_path_server']=output_path or input(f"\nAdd ssh output path directory: ")
    data['remote_script_path']=server_script or input(f"\nAdd remote qsub script path directory: ")
    return data

def save_conf(path:str=None,data:dict=None,key_path:str=None):
    """Save data to conf file"""    
    data= data or generate_data()
    path= path or exut.merge_filepathGC(exdf.grid_base_conf_name)
    try:
        key=load_key(key_path)
    except:
        print(f"\nKey not found, generating new key")
        generate_key()
        key=load_key()
    fernet=Fernet(key)
    credential_data=json.dumps(data).encode('utf-8')
    data=fernet.encrypt(credential_data)
    with open(path, "wb") as key_file:
        key_file.write(data)

def load_conf_to_dict(path:str=None,key:str=None):
    path = path or exut.merge_filepathGC(exdf.grid_base_conf_name)
    if not isinstance(key,bytes):
        key = load_key(key)
    with open(path, "rb")as file:
        data= file.read()
    fernet=Fernet(key)
    data=fernet.decrypt(data).decode('utf-8')
    return json.loads(data)

def check_files(key_path:str=None,conf_path:str=None):
    key_path = key_path or exut.merge_default_path(".key/key")
    conf_path = conf_path or exut.merge_filepathGC(exdf.grid_base_conf_name)
    if not exut.file_validator(key_path):
        print(f"\nKey not found, generating new key")
        generate_key()
    if not exut.file_validator(conf_path):
        print(f"\nConf file not found, generate new conf file manually with grid_utils")
        return False
    return True

def execute_shell_script(command:str):
    """Execute shell command a string command or script file"""
    if os.path.isfile(command) and os.access(command,os.X_OK):
        command=[command] # For 
    try:
        if isinstance(command,list):
            process = subprocess.call([command],shell=True)
        else:    
            process = subprocess.call(command,shell=True)
        return True
    except Exception as e:
        print(f"\nError executing shell command: {e}")
        return False
    
def check_kinit():
    """Check validity of actual Kerberos ticket - only for users with own tickets

    Returns:
        bool: True if ticket is valid, False if not
    """
    current_datetime = datetime.utcnow().timestamp()
    # Get output from klist
    try:
        klist_output = subprocess.check_output('klist', shell=True, text=True)
    except subprocess.CalledProcessError:
        print("Warning: klist command failed. Is kinit available?")
        klist_output = ""
    # Split output into lines and filter out non-data lines
    data_list = [[field for field in line.split('  ') if field] for line in klist_output.split('\n') if len(line.split('  ')) == 3]
    # Create DataFrame from the list
    df = pd.DataFrame(data_list, columns=['Valid starting', 'Expires', 'Service principal'])
    # Check if token is expired
    expires_timestamp = parser.parse(df.iloc[0]['Expires']).timestamp()
    if expires_timestamp < current_datetime:
        print(f"You cannot send a request to Metacentrum, because token is expired. Max valid until: {df.iloc[0]['Expires']} Contact the administrator to register a new token.")
        return False
    else:
        print("Its ok")
        return True

def execute_shell_script_and_check_output(command:str):
    """Execute shell command a string command or script file""" 
    process = subprocess.run(command,shell=True,check=False)
    return_code=process.returncode    
    if bool(return_code)==True:
        return True
    else:
        return False

def copy_files_to_parent(path:str):
    parent_dir = os.path.dirname(path)
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            shutil.copy(file_path, parent_dir)

def get_folder_name(path:str):
    return os.path.basename(os.path.normpath(path))

def load_config(path:str):
    with open(path,'r') as f:
        return json.load(f)

def write_config(path:str,data:dict):
    with open(path,'w') as f:
        pretty_json=json.dumps(data,indent=2)
        f.write(pretty_json)

def add_to_queue(user_name:str,local_location:str,remote_location:str,json_path:str=exdf.queue_default_path):
    queue_conf=load_config(json_path)
    if 'queue_list' not in queue_conf:
        queue_conf=exdf.queue_download_config
    app_conf=exdf.queue_download_config_single
    app_conf["user_name"]=user_name
    app_conf["local_location"]=local_location
    app_conf["remote_location"]=remote_location
    queue_conf['queue_list'].append(app_conf)
    write_config(json_path,queue_conf)

# if __name__=="__main__":
# #     # Generating keys and saving new configuration files
# #       save_conf()
#     save_conf("/home/user/download_scripts/conn_conf",key_path="/home/user/download_scripts/key")