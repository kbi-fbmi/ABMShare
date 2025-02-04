import os
import covasim as cv
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import numpy as np
import json

# for saving sims into /multisims_saves
# TODO: create for single sims as well
def save_sims(sims,filename):
    if isinstance(sims,cv.MultiSim):
        sims.save(get_filepath(f"multisims_saves/{filename}.msim"))
    sims.save(get_filepath(f"multisims_saves/{filename}.msim"))
    return

# For loading multisims from /multisims_saves
def load_sims(filename): 
    try:
        return cv.MultiSim.load(get_filepath(f'multisims_saves/{filename}.msim'))
    except FileNotFoundError:
        raise FileNotFoundError(f"File was not found in multisims_saves/{filename}")

# For saving figures into .png images in /images
def save_fig_to_png(fig,filename):
    fig.savefig(get_filepath(f"images/{filename}.png"))

def get_filepath(path):
    this_dir=os.path.dirname(os.path.abspath(__file__)) #Example dir 
    return os.path.join(this_dir,path)

# Get and save graph of deads in time of days/t
# TODO: Recreate it for using keys instead fixing on time
def get_deaths_graph_from_sim(sim:cv.Sim,time=None,filename=None):
    filename = filename or f"Simulation_{sim.label}_{datetime.datetime.now().strftime('%m-%d_%H-%M-%S')}" 
    if time is None or 't':
        return save_fig_to_png(return_fig_of_two_variables(sim.results['t'],sim.results['n_dead']),f"{filename}")
    elif time == 'days':
        return save_fig_to_png(return_fig_of_two_variables(sim.results['date'],sim.results['n_dead']),f"{filename}")
    else:
        errormsg = f'Time key({time}, is not valid, it must be one of: <t,days> or nothing to load default.'
        raise KeyError(errormsg)

def return_fig_of_two_variables(x,y):
    fig=plt.figure()
    plt.plot(x,y)
    # plt.xticks(ticks=x, labels=x)
    # plt.yticks(ticks=y,labels=y)
    return fig

# Return or save df of supplied variables
# If save is true, than 
# Col_names is supplied as list of keys from sim results
# TODO Refactor, now only converts to ints
def create_int_results_df(sim,col_names:list,save:bool=False,filename:str=None):    
    dictionary={}
    for i in col_names:
        if i not in sim.results:
            raise KeyError("This key is not in sim results")
        dictionary[i]=np.int64(sim.results[i][:])
    df=pd.DataFrame(dictionary)
    if save and filename is not None:
        return save_csv_file(df,filename)
    elif save and filename==None:
        raise ValueError(f"Filename was not supplied.")
    return df

def create_default_types_results_df(sim,col_names:list,save:bool=False,filename:str=None):    
    dictionary={}
    for i in col_names:
        if i not in sim.results:
            raise KeyError("This key is not in sim results")
        dictionary[i]=sim.results[i][:]
    df=pd.DataFrame(dictionary)
    if save and filename is not None:
        return save_csv_file(df,filename)
    elif save and filename==None:
        raise ValueError(f"Filename was not supplied.")
    return df

def save_csv_file(df:pd.DataFrame,filename):
    df.to_csv(get_filepath(f"saved_csv/{filename}.csv"),index=False)
    return
    
# TODO refactor to be more general, now is specified
#Its merging all csv files from all regions into one
def merge_data_csv(base_filename:str,col_names:list=None):
    df=pd.DataFrame()    
    for i in range(0,8,1):
        if df.empty:
            try:
                df=pd.read_csv(get_filepath(f"saved_csv/r_{i}_{base_filename}.csv"))                
            except FileNotFoundError:
                raise FileNotFoundError(f"Cannot find file with name:r_{i}_{base_filename}.csv in saved_csv/")
        else:
            try:
                df[col_names]+=pd.read_csv(get_filepath(f"saved_csv/r_{i}_{base_filename}.csv"))[col_names]
            except FileNotFoundError:
                raise FileNotFoundError(f"Cannot find file with name:r_{i}_{base_filename}.csv in saved_csv/")            
    return df

# Method for loading various formats of mobility/population data
def load_datafile(path:str):
    '''
    Method for loading data, default for .xlsx. Can be implemented for others
    '''
    filename, file_extension = os.path.splitext(path)
    if file_extension ==".xlsx":
        return pd.read_excel(path)

def load_json_config(filepath,absolute_path=False):
    if not absolute_path: 
        filepath=get_filepath('confs/'+filepath)            
    with open(filepath,'r',encoding="utf-8") as jsonfile:
        config=json.load(jsonfile)
    return config
