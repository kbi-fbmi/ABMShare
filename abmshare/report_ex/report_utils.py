import os
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import abmshare.defaults as exdf
import abmshare.utils as exut
import covasim as cv


def load_sim(filepath):
    """Method for returning a multisim object.
    filepath (str)                           : path to .msim file (file containing multisim)
    """
    try:
        return cv.MultiSim.load(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filepath} does not exists.")

# For saving figures into .png images in /images
def save_fig_to_png(fig,filename,filepath,extension=".png"):
    """Method for saving .png images of figures generated in covasim.
    fig (matplotlib fig)                               : figure to save
    filename (str)                                     : name for save figure
    filepath (str)                                     : dirpath for saving figure
    extension (str)                                    : file extension. Default is .png
    """
    filename=f"{filename}.{extension}"
    fig.savefig(os.path.join(filepath,exdf.save_settings["saved_images"],filename))

def return_fig_of_two_variables(x,y):
    """Method for returning simple figure of two parameters.
    x(numeric)                                         :      
    y(numeric)                                         :
    """
    fig=plt.figure()
    plt.plot(x,y)
    return fig

def save_report(report,sim_results,location):
    """report(dict)                         : keys, output_format, filename
    sim_result (dict)                    : values
    location (string)                    : dirpath
    """
    filename=exut.filename_validator(exut.merge_twoPaths(location,report["filename"]))
    output_format=report["output_format"] or "csv"
    dictionary={}
    for key in report["keys"]:
        if key =="t":
            dictionary[key]=sim_results[key]
        else:
            dictionary[key]=sim_results[key].values
    df=pd.DataFrame(dictionary)
    filename=os.path.basename(filename)
    exut.save_file(location,filename,output_format,df)


def save_whole(simulations,dirpath,filename=None,extension=".csv"):
    """Method for saving the whole multisimulation object parameters and data.
    simulations (multisim)      : multisim object
    dirpath(string)             : dirpath for saving 
    filename(string)            : filename for saving OPTIONAL
    extension(string)           : default extension
    """
    if not filename:
        filename="FullSimulation"
    filepath=exut.merge_twoPaths(dirpath,filename)
    try:
        # df=copy.deepcopy(simulations.sims[0].to_df())
        df=simulations.sims[0].to_df()
        df=df[exdf.report_keys_without_date]
        for i,sim in enumerate(simulations.sims):
            if i != 0:
                df2=sim.to_df()
                df[exdf.report_keys_without_date]=df[exdf.report_keys_without_date].add(df2[exdf.report_keys_without_date])

        # Add date and time
        # df['date']=simulations.sims[0].date(simulations.sims[0].t)
        # t = np.arange(datetime(1985,7,1), datetime(2015,7,1), timedelta(days=1)).astype(datetime)
        df["date"]= np.arange(datetime.strptime((simulations.sims[0].date(0)),"%Y-%m-%d"),
                  datetime.strptime((simulations.sims[0].date(simulations.sims[0].t+1)),"%Y-%m-%d"),
                  timedelta(days=1)).astype(datetime)
        df["t"]=np.arange(0,int(simulations.sims[0].t+1))
        exut.save_file(dirpath,filename,extension,df)
    except:
        print(f"Cannot create whole simulation summary at:{os.path.join(dirpath,filename)}.{extension}")


def create_single_variant_output(simulation, dirpath):
    result_keys = simulation.results["variant"]
    variant_names = ["wild"] + [simulation["variants"][variant].label for variant in range(simulation["n_variants"] - 1)]
    days = np.array(range(simulation.t + 1))
    dates = simulation.date(range(simulation.t + 1))

    df_list = []
    for variant in range(simulation["n_variants"]):
        df_dict = {"day": days, "date": dates}
        for key in result_keys:
            df_dict[key] = simulation.results["variant"][key][variant]
        df_list.append(pd.DataFrame(df_dict))

    filename = f"{simulation.label}_variant_results.xlsx"
    writer = pd.ExcelWriter(exut.merge_twoPaths(dirpath, filename), engine="xlsxwriter")

    for i, dataframe in enumerate(df_list):
        dataframe.to_excel(writer, sheet_name=variant_names[i])

    writer.close()

    return df_list, variant_names

def sum_dataframes(basedf,newdf):
    for i,data in enumerate(basedf):
        basedf[i]=basedf[i].add(newdf[i][exdf.variant_result_keys])
    # return basedf

def save_whole_variant_output(dataframe_list,variant_names,dirpath,filename=None):
    filename=filename or "FullSimulation_variant_results.xlsx"
    writer = pd.ExcelWriter(exut.merge_twoPaths(dirpath,filename), engine = "xlsxwriter")
    for i,dataframe in enumerate(dataframe_list):
        dataframe.to_excel(writer,sheet_name=variant_names[i])
    writer.close()

