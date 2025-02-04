import abmshare.utils as exut
import abmshare.defaults as exdf
from pathlib import Path
import os
import numpy as np
import pandas as pd
import json
import copy
import jsbeautifier

class RegionConfigCreator:
    def __init__(self,configuration,age_distribution_configuration,full_configuration:dict=None,output_configuration=None, default_configuration=None, wait=False, save_settings:dict=None,csv_data_dict:dict=None):
        '''
            configuration = based on this configuration there will be made changes to output configuration
            output_configuration = there can be preloaded output configuration with some pars
            default_configuration = with pars, which can be missing from input configuration - default from Czechia
            age_distribution_configuration  (dict)                  : config parameters for age distribution
            wait (bool)                                             : if wait is true, then its manually needed to call process function
            save_settings (dict)                                    : (OPTIONAL) if provided, then its changed output filepath
            csv_data_dict (dict)                                    : dict of data of other files to integrate in
        '''
        # Some pars
        if not isinstance(configuration,dict):
            configuration=exut.load_config(configuration)
        if not isinstance(age_distribution_configuration,dict):
            age_distribution_configuration=exut.load_config(age_distribution_configuration)
        self.configuration=configuration
        self.age_distribution_configuration=age_distribution_configuration     
        self.full_configuration=full_configuration
        self.output_configuration=None
        self.default_configuration=None
        self.age_distribution_filepath=None
        self.wait=wait
        self.save_settings=save_settings or {}
        self.csv_data_dict=csv_data_dict or {}
        # Check and assign/load output and default configurations
        if output_configuration is None:
            self.output_configuration=exut.load_config(exut.merge_file_path("synthpops_ex/data/empty_region.json"))
        else:
            self.output_configuration=output_configuration
        
        if default_configuration is None:
            self.default_configuration=exut.load_config(exut.merge_file_path("synthpops_ex/data/default_czechia.json"))
        elif exdf.confkeys['parent_location'] in self.configuration and self.configuration[exdf.confkeys['parent_location']]:
            try:
                self.default_configuration=exut.load_config(self.configuration[exdf.confkeys['parent_location']])
            except:
                print(f"Cannot load parent config from {self.configuration[exdf.confkeys['parent_location']]}")
        else:
            self.default_configuration=default_configuration
        if not wait:
            self.process()

    def get_num_bins(self):
        return self.age_distribution_configuration['population_age_distributions_brackets']['num_bins']

    def save_output_config(self,region_config,filename): 
        '''
            Can be also called directly. For saving output configuration. It is called from process()
        '''
        if self.save_settings: # Autoincrement save settings are prioritized
            filedir=os.path.join(self.save_settings['location'],exdf.save_settings["population_configurations"]) 
        else:        
            filedir=self.configuration['output_configuration_filepath']
        exut.directory_validator(filedir) # Validator for directory
        filepath=os.path.join(filedir,filename)
        options = jsbeautifier.default_options()
        options.indent_size = 2
        pretty_json=jsbeautifier.beautify(json.dumps(region_config), options)
        with open(filepath,'w') as f:
            f.write(pretty_json)
        

    def process(self):
        '''
            Core function for parsing configuration.
            At first there are changes to plain empty configuration, and then merge with default (if there are not required values)
        '''
        if len(self.configuration['regions'])<1:
            raise ValueError("There is no regions in configuration. Check configuration or its filepath")

        if  self.age_distribution_configuration['value'] and self.age_distribution_configuration['filepath'] is not None:
            self.age_distribution_filepath=self.age_distribution_configuration['filepath']

        # Prepare csv data for region configs
        # self.load_synthpops_csv_data()

        for i,region in enumerate(self.configuration['regions']):
            region_config=copy.deepcopy(self.output_configuration)        
            self.load_synthpops_csv_data(region_config,i,region) # dont need to return it
            # Place for another par implementation
            for key,value in region.items(): #Pars from config file of each region
                if key in exdf.synthpops_pars['region_pars'] and not key in exdf.synthpops_csv_files:
                    region_config[key]=value
                elif key == "name": # Name as location_name
                    region_config['location_name']=value
                elif key in exdf.synthpops_pars['regions']: #Oter region pars, no need for adding to conf
                    pass
                elif key == "notes": # Notes must be in list
                    if value:
                        region_config['notes']=[value]
                    else:
                        region_config['notes']=[]
                elif key == exdf.confkeys['parent']:
                    try:
                        self.default_configuration=exut.load_config(region[exdf.confkeys['parent']]) #TODO: change for parent_location config
                    except:
                        self.default_configuration=exut.load_config(exut.merge_filepathSP('data/Czechia.json'))
                        print(f"Cannot load parent config from:{region[exdf.confkeys['parent']]}, using default configuration for Czechia.")
                else:
                    print(f"{key} is not a valid key, you can use keys from{exdf.synthpops_pars['region_pars']}")
                    
            for key,value in self.default_configuration.items():
                if not region_config[key]:
                    region_config[key]=value
            # Handle notes par
            if not isinstance(region_config['notes'],list):
                region_config['notes']=[]
            self.save_output_config(region_config,region['filename'])
        return
    
    def load_pop_age_distribution_csv(self,i,region,num_of_bins):
        '''
        Method for parsing csv age_distribution file.
            i (int)                             : number of iteration of region
            region (dict)                       : dict holding region data from configuration file                      
            num_of_bins (list)                  : list of integers representing bins
        '''        
        data=self.csv_data_dict['population_age_distributions']['data'].iloc[i][3:] # set for default dataset
        output=[]
        for bin in num_of_bins:
            max=-1
            distrib=copy.deepcopy(exdf.population_age_distribution_default)
            distrib['num_bins']=bin
            if bin != len(data):
                max=bin
            for i,column in enumerate(data.index):
                if len(column.split('_'))==3:
                    _prefix,pre,pos = column.split('_')
                else:
                    pre,pos = column.split('_')
                if max-1 == i or i == len(data)-1:
                    distrib['distribution'].append([int(pre),100,np.sum(data[i:])]) # add mean for data
                    break            
                distrib['distribution'].append([int(pre),int(pos),data[i]])
            output.append(distrib)
        return output
    
    ## method for loading csv data and parsing them. Default its int:float pairs
    def load_employment_rates_by_age(self,region:dict,conf:dict,index_name:str=None):
        csv_data_name="employment_rates_by_age"
        data=conf['data']
        data.columns = map(str.lower, data.columns)        
        region_name=region.get(exdf.confkeys['region_data_name'],None).lower()
        location_code=region.get(exdf.confkeys['location_code'],None).lower()
        if index_name:
            index_name = index_name.lower()
        elif index_name is None and location_code is not None and location_code in data.head():
            index_name = location_code
        elif index_name is None and region_name is not None and region_name in data.head():
            index_name = region_name
        else:
            print(f"Cannot find region in {csv_data_name}. Region name: {region_name}, location code: {location_code}")
            return
        output=[]
        # Convert all columns to lowercase
        for i,row in data.iterrows():
            if row[index_name] == row[index_name]:
                output.append([int(row['age']),float(row[index_name])])
        return output
    

    def load_enrollment_rates_by_age(self,region:dict,conf:dict,index_name:str=None):
        csv_data_name="enrollment_rates_by_age"
        data=conf['data']
        data.columns = map(str.lower, data.columns)        
        region_name=region.get(exdf.confkeys['region_data_name'],None).lower()
        location_code=region.get(exdf.confkeys['location_code'],None).lower()
        if index_name:
            index_name = index_name.lower()
        elif index_name is None and location_code is not None and location_code in data.head():
            index_name = location_code
        elif index_name is None and region_name is not None and region_name in data.head():
            index_name = region_name
        else:
            print(f"Cannot find region in {csv_data_name}. Region name: {region_name}, location code: {location_code}")
            return
        output=[]
        # Convert all columns to lowercase
        for i,row in data.iterrows():
            if row[index_name] == row[index_name]:
                output.append([int(row['age']),float(row[index_name])])
        return output
    
    def load_household_head_age_brackets(self,region:dict,conf:dict,index_name:str=None):
        data=conf['data']
        data.columns = map(str.lower, data.columns)        
        output=[]
        # Convert all columns to lowercase
        for i,row in data.iterrows():
            output.append([int(row['min_age']),int(row['max_age'])])
        return output
    
    def load_household_head_age_distribution_by_family_size(self,region:dict,conf:dict,index_name:str=None):
        data=conf['data']
        data.columns = map(str.lower, data.columns)        
        output=[]
        # Convert all columns to lowercase
        ind=0
        for i,row in data.iterrows():
            output.append([float(x) for x in row[:]])
            output[ind][0]=int(output[ind][0])
            ind+=1
        return output
    
    def load_household_size_distribution(self,region:dict,conf:dict,index_name:str=None):
        data=conf['data']
        data.columns = map(str.lower, data.columns)
        output=[]
        for i,row in data.iterrows():
            output.append([int(row['num']),float(row['distribution'])])
        return output
    
    def load_school_size_brackets(self,region:dict,conf:dict,index_name:str=None):
        data=conf['data']
        data.columns = map(str.lower, data.columns)
        output=[]
        for i,row in data.iterrows():
            output.append([int(row['min']),int(row['max'])])
        return output

    def load_school_distribution(self,region:dict,conf:dict,index_name:str=None):
        data=conf['data']
        data.columns = map(str.lower, data.columns)
        output=[]
        for i,row in data.iterrows():
            output.append(float(row['distribution']))
        return output

    def load_school_size_distribution(self,region:dict,conf:dict,index_name:str=None):
        data=conf['data']
        data.columns = map(str.lower, data.columns)
        output=[]
        pattern={"school_type":"","size_distribution":[]}
        for i,row in data.iterrows():
            pattern["school_type"]=row['school_type']
            pattern["size_distribution"]=[float(x) for x in (row[1].split(","))]
            output.append(pattern.copy())
        return output
    
    def load_school_types(self,region:dict,conf:dict,index_name:str=None):
        data=conf['data']
        data.columns = map(str.lower, data.columns)
        output=[]
        pattern={"school_type":"","age_range":[]}
        for i,row in data.iterrows():
            pattern["school_type"]=row['school_type']
            pattern["age_range"]=[row['min_age'],row['max_age']]
            output.append(pattern.copy())
        return output

    def load_workplace_size_counts(self,region:dict,conf:dict,index_name:str=None):
        data=conf['data']
        data.columns = map(str.lower, data.columns)
        output=[]
        for i,row in data.iterrows():
            output.append([int(row['min_people']),int(row['max_people']),float(row['count'])])
        return output

    def load_synthpops_csv_data(self,region_config,i,region):
        '''
            Method for parsing provided dataframes from csf to new sim configuration files. Also checking for all regions.
            region_config (dict)                : processed dictionary, which need to edit
            i (int)                             : number of iteration of region
            region (dict)                       : dict holding region data from configuration file
        '''
        # for key,value in self.csv_data_dict.items():
        for key in exdf.synthpops_csv_files:
            try:
                region_specific={"value":True,"data":exut.load_datafile(region[key]['filepath'])}
            except:
                region_specific=None
            # If its age_distribution
            if key =="population_age_distributions" and self.get_num_bins() is not None:
                if region.get('population_age_distributions',False) and exut.check_consistency(config=self.full_configuration,target_key="num_bins"):                        
                    region_config[key]=self.load_pop_age_distribution_csv(i,region,region[exdf.confkeys['population_age_distributions']][exdf.confkeys['population_age_distributions_brackets']]['num_bins'])
                    continue            
                region_config[key]=self.load_pop_age_distribution_csv(i,region,self.get_num_bins())

            elif key=="employment_rates_by_age" and (self.csv_data_dict.get("employment_rates_by_age",False) or region.get("employment_rates_by_age",False)):
                if region.get("employment_rates_by_age",False) and region_specific is not None:
                    region_config[key]=self.load_employment_rates_by_age(region=region,
                        conf=region_specific) 
                    continue
                region_config[key]=self.load_employment_rates_by_age(region=region,
                    conf=self.csv_data_dict[key],index_name=self.csv_data_dict[key].get('region_code',None)) 
                
            elif key=="enrollment_rates_by_age" and (self.csv_data_dict.get("enrollment_rates_by_age",False) or region.get("enrollment_rates_by_age",False)):
                if region.get("enrollment_rates_by_age",False) and region_specific is not None:
                    region_config[key]=self.load_enrollment_rates_by_age(region=region,
                        conf=region_specific)
                    continue
                region_config[key]=self.load_enrollment_rates_by_age(region=region,
                    conf=self.csv_data_dict[key], index_name=self.csv_data_dict[key].get('region_code',None))
                
            elif key in exdf.synthpops_one_file_data.keys() and (self.csv_data_dict.get(key,False) or region.get(key,False)):
                if region.get(key,False) and region_specific is not None:
                    func=getattr(self,exdf.synthpops_one_file_data[key])
                    region_config[key]=func(region=region,conf=region_specific)
                else:
                    func=getattr(self,exdf.synthpops_one_file_data[key])
                    region_config[key]=func(region=region,conf=self.csv_data_dict[key])
                
            # elif key=="household_head_age_brackets" and (self.csv_data_dict.get("household_head_age_brackets",False) or region.get("household_head_age_brackets",False)):
            #     if region.get("household_head_age_brackets",False):
            #         region_config[key]=self.load_household_head_age_brackets(region=region,
            #             conf=self.csv_data_dict[key])
            #         continue
            #     region_config[key]=self.load_household_head_age_brackets(region=region,
            #         conf=self.csv_data_dict[key])
            # elif key=="household_head_age_distribution_by_family_size" and (self.csv_data_dict.get("household_head_age_distribution_by_family_size",False) or region.get("household_head_age_distribution_by_family_size",False)):
            #     if region.get("household_head_age_distribution_by_family_size",False):
            #         region_config[key]=self.load_household_head_age_distribution_by_family_size(region=region,
            #             conf=self.csv_data_dict[key])
            #         continue
            #     region_config[key]=self.load_household_head_age_distribution_by_family_size(region=region,
            #         conf=self.csv_data_dict[key])
            # elif key=="household_size_distribution" and (self.csv_data_dict.get("household_size_distribution",False) or region.get("household_size_distribution",False)):
            #     if region.get("household_size_distribution",False):
            #         region_config[key]=self.load_household_size_distribution(region=region,
            #             conf=self.csv_data_dict[key])
            #         continue
            #     region_config[key]=self.load_household_size_distribution(region=region,
            #         conf=self.csv_data_dict[key])
            # elif key=="school_size_brackets" and (self.csv_data_dict.get("school_size_brackets",False) or region.get("school_size_brackets",False)):
            #     if region.get("school_size_brackets",False):
            #         region_config[key]=self.load_school_size_brackets(region=region,
            #             conf=self.csv_data_dict[key])
            #         continue
            #     region_config[key]=self.load_school_size_brackets(region=region,
            #         conf=self.csv_data_dict[key])
            # elif key=="school_size_distribution" and (self.csv_data_dict.get("school_size_distribution",False) or region.get("school_size_distribution",False)):
            #     if region.get("school_size_distribution",False):
            #         region_config[key]=self.load_school_distribution(region=region,
            #             conf=self.csv_data_dict[key])
            #         continue
            #     region_config[key]=self.load_school_distribution(region=region,
            #         conf=self.csv_data_dict[key])
            # elif key=="school_size_distribution_by_type" and (self.csv_data_dict.get("school_size_distribution_by_type",False) or region.get("school_size_distribution_by_type",False)):
            #     if region.get("school_size_distribution_by_type",False):
            #         region_config[key]=self.load_school_size_distribution(region=region,
            #             conf=self.csv_data_dict[key])
            #         continue
            #     region_config[key]=self.load_school_size_distribution(region=region,
            #         conf=self.csv_data_dict[key])
            # elif key=="school_types_by_age" and (self.csv_data_dict.get("school_types_by_age",False) or region.get("school_types_by_age",False)):
            #     if region.get("school_types_by_age",False):
            #         region_config[key]=self.load_school_types(region=region,
            #             conf=self.csv_data_dict[key])
            #         continue
            #     region_config[key]=self.load_school_types(region=region,
            #         conf=self.csv_data_dict[key])
            # elif key=="workplace_size_counts_by_num_personnel" and (self.csv_data_dict.get("workplace_size_counts_by_num_personnel",False) or region.get("workplace_size_counts_by_num_personnel",False)):            
            #     if region.get("workplace_size_counts_by_num_personnel",False):
            #         region_config[key]=self.load_workplace_size_counts(region=region,
            #             conf=self.csv_data_dict[key])
            #         continue
            #     region_config[key]=self.load_workplace_size_counts(region=region,
            #         conf=self.csv_data_dict[key])