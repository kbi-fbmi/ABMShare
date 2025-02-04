import abmshare.defaults as exdf
import abmshare.utils as exut
import pandas as pd
import os
import numpy as np
import covasim as cv
import covasim.parameters as cvpar

class ImmunityProcessing():
    """_summary_
    """
    def __init__(self,config:str|dict):
        self.config=exut.load_config(config)
        self.data_files=self.load_datafiles(self.config['immunity']['filepath'])
        self.process_files()

    def load_datafiles(self,datapath:str):
        data=exut.load_datafile(datapath)
        try:
            return data.to_dict(orient="index")[0]
        except Exception as e:
            print(f"Error: {e}")
            return None

    def prepare_vaccine_dose_pars(self,path:str):
        try:
            data=exut.load_datafile(path)
            data.set_index("vaccine",inplace=True)
            return data.to_dict(orient="index")

        except Exception as e:
            print(f"Error while loading file {path} in vaccine dose pars processing: {e}")
            return None
    
    def prepare_vaccine_variant_pars(self,path:str):
        try:
            data=exut.load_datafile(path)
            data.set_index("vaccine",inplace=True)
            return data.to_dict(orient="index")

        except Exception as e:
            print(f"Error while loading file {path} in vaccine variant pars processing: {e}")
            return None

    def prepare_variant_pars(self,path:str):
        try:
            data=exut.load_datafile(path)
            data.set_index("variant",inplace=True)
            return data.to_dict(orient="index")

        except Exception as e:
            print(f"Error while loading file {path} in variant pars processing: {e}")
            return None
        
    def get_variant_cross_im(self,path:str):
        try:
            data=exut.load_datafile(path)
            data.set_index("variant",inplace=True)
            return data.to_dict(orient="index")

        except Exception as e:
            print(f"Error while loading file {path} in variant cross immunity processing: {e}")
            return None

    def process_files(self):
        if self.data_files.get("vaccine_dose_pars",False):
            cvpar.immunity_custom_pars['immunity']['vaccine_dose_pars']=self.prepare_vaccine_dose_pars(self.data_files['vaccine_dose_pars'])
        if self.data_files.get("vaccine_variant_pars",False): # Also do get_vaccine_variant_pars
            cvpar.immunity_custom_pars['immunity']['vaccine_variant_pars']=self.prepare_vaccine_variant_pars(self.data_files['vaccine_variant_pars'])
            orig_choices,_=cvpar.get_vaccine_choices()
            for key in cvpar.immunity_custom_pars['immunity']['vaccine_variant_pars']:
                if key not in orig_choices:
                    cvpar.immunity_custom_pars['immunity']['get_vaccine_choices']={key:[key]}                    
        if self.data_files.get("variant_pars",False): # Also do get_variant_pars
            cvpar.immunity_custom_pars['variants']['variant_pars']=self.prepare_variant_pars(self.data_files['variant_pars'])
            orig_choices=cvpar.get_variant_choices()
            for key in cvpar.immunity_custom_pars['variants']['variant_pars']:
                if key not in orig_choices:
                    cvpar.immunity_custom_pars['variants']['get_variant_choices']={key:[key]}
            cvpar.immunity_custom_pars['variants']['get_variant_choices']={key:[key]}
        if self.data_files.get("variant_cross_immunity",False):
            cvpar.immunity_custom_pars['immunity']['cross_immunity']=self.get_variant_cross_im(self.data_files['variant_cross_immunity'])
            

# if __name__=="__main__":
#     config=exut.load_config("/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/simulation_with_variants.json")
#     vp=ImmunityProcessing(config)

#     pass
#     # Implement it to loader
#     # Edit the grid loader for processing variants
#         # Edit get simulation files
#     # Validator somehow?
#     # Implement it to the simulation
#     # Test it