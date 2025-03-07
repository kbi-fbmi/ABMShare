import copy
import json

import jsbeautifier
import numpy as np
from pytictoc import TicToc

import abmshare.defaults as exdf
import abmshare.utils as exut
import synthpops as sp


class Region:
    def __init__(self,
                 location_code:str,
                 region_name:str,
                 untrimmed_name:str,
                 pars:dict,
                 notes:str|list=None,
                 region_parent_name:str=None,
                 parent_config:str|dict=None,
                 sheet_name:str=None,
                 region_config:str|dict=None,
                 data_provenance_notices:str|list=None,
                 reference_links:str|list=None,
                 citations:str|list=None,
                 save_settings:dict=None,
                 pop_size:int=None,
                 test:bool=False):
        # Region config parameters
        self.location_code=location_code
        self.region_name=region_name
        self.untrimmed_name=untrimmed_name
        self.pars=pars
        self.region_parent_name=region_parent_name
        self.parent_config=parent_config
        if isinstance(notes,str):
            notes=[notes]
        elif isinstance(notes,float):
            notes=[""]
        self.notes=notes or [""]
        if isinstance(citations,str):
            citations=[citations]
        self.citations=citations or [""]
        if isinstance(data_provenance_notices,str):
            data_provenance_notices=[data_provenance_notices]
        self.data_provenance_notices=data_provenance_notices or [""]
        if isinstance(reference_links,str):
            reference_links=[reference_links]
        self.reference_links=reference_links or [""]
        self.test=test
        # Save setting
        self.save_settings=save_settings
        # Region creator parameters
        self.sheet_name=sheet_name
        self.region_config=region_config
        self.data_files={}
        self.pop_size=pop_size
        # Processed parameters
        self.region_config={}
        self.region_config_output_path=None
        self.pop_creator_pars={}
        self.naming_object={}

    def create_population_object(self):
        print(f"\nCreating population object for region {self.region_name} ({self.location_code})",end="")
        t=TicToc()
        t.tic()
        pop=sp.Pop(**self.pop_creator_pars)
        t.toc(f"\nRegion: {self.region_name} ({self.location_code}) population object created.")
        filename=exut.generate_population_filename(region_name=self.region_name,prefix=self.naming_object["pop_name_prefix"],
                                                   suffix=self.naming_object["pop_name_suffix"],test=self.test)
        self.save_population_object(pop=pop,filename=filename)
        #saving

    def save_population_object(self,pop:sp.Pop,filename:str):
        if self.save_settings:
            filedir=exut.merge_twoPaths(self.save_settings["location"],exdf.save_settings["population_path"])
        elif self.naming_object["pop_creator_dirpath"]:
            filedir = self.naming_object["pop_creator_dirpath"]
        exut.directory_validator(filedir)
        filepath=exut.merge_twoPaths(filedir,filename)
        if self.naming_object["pop_output_type"] == "json":
            pop.to_json(f"{filepath}.json")
        elif self.naming_object["pop_output_type"] =="obj":
            pop.save(f"{filepath}.pop")
        else:
            print("Location for save was not specified, saving population as default .pop object.")
            pop.save(f"{filepath}.pop")

    def add_naming_object(self,naming_object):
        """Naming object is a dictionary with keys and values for naming the population."""
        for key, value in exdf.synthpops_naming_keys_mapped.items():
            if key in naming_object.keys():
                self.naming_object[value]=naming_object[key]
            else:
                self.naming_object[value]=""
        # for key,value in naming_object.items():
        #     if key in exdf.synthpops_naming_keys_mapped.keys():
        #         self.naming_object[exdf.synthpops_naming_keys_mapped[key]]=value

    def add_pop_size(self,pop_size:int):
        self.pop_size=pop_size

    def add_pop_creator_par(self,key:str,value):
        self.pop_creator_pars[key]=getattr(self,value)

    def add_datafiles(self,datafiles:list):
        self.data_files=datafiles

    def process_region_creation(self,test:bool=False):
        self.prepare_region_config()
        self.load_synthpops_csv_data()
        self.process_region_config()
        self.save_region_config()

    def save_region_config(self):
        try:
            if self.save_settings:
                filedir=exut.merge_twoPaths(self.save_settings["location"],exdf.save_settings["population_configurations"])
            else:
                filedir=self.naming_object["pop_creator_dirpath"]
            exut.directory_validator(filedir)
            filepath=exut.merge_twoPaths(filedir,f"{self.region_name}.json")
            options = jsbeautifier.default_options()
            options.indent_size = 2
            pretty_json=jsbeautifier.beautify(json.dumps(self.region_config), options)
            with open(filepath,"w") as f:
                f.write(pretty_json)
            self.region_config_output_path=filepath
        except:
            print(f"\nNo save settings for region {self.region_name} ({self.location_code}). Cannot save population configurations.",end="")


    def prepare_region_config(self):
        self.region_config=exut.load_config(self.parent_config)

    def process_region_config(self):
        for var in self.__dict__:
            if var in exdf.synthpops_region_pars_mapped.keys():
                value=self.__dict__[var]
                if var==exdf.synthpops_region_pars_mapped["region_parent_name"] or var=="region_parent_name":
                    value+=".json"
                elif isinstance(value,float) and np.isnan(value) or not value:
                    value=[""]
                self.region_config[exdf.synthpops_region_pars_mapped[var]]=value
        if exut.file_validator(self.parent_config):
            self.region_config["parent"]=self.parent_config

    def load_synthpops_csv_data(self):
        """Method for loading csv data and parsing them.
        """
        # for key,value in self.csv_data_dict.items():
        for key,filepath in self.data_files.items():
            if key not in exdf.synthpops_csv_files:
                continue
            # If its age_distribution
            if key =="population_age_distributions":
                self.region_config[key]=self.load_pop_age_distribution_csv()

            elif key=="employment_rates_by_age":
                self.region_config[key]=self.load_employment_rates_by_age()

            elif key=="enrollment_rates_by_age":
                self.region_config[key]=self.load_enrollment_rates_by_age()

            elif key in exdf.synthpops_one_file_data.keys():
                func=getattr(self,exdf.synthpops_one_file_data[key])
                self.region_config[key]=func()

    def load_pop_age_distribution_csv(self):
        """Method for parsing csv age_distribution file.
        """
        num_of_bins = exdf.population_age_distributions_bins
        data = exut.load_datafile(self.data_files["population_age_distributions"])
        data = data.iloc[exut.get_index_by_column_and_value(df=data, column=exdf.synthpops_region_csv_columns["location_code"], value=self.location_code)][3:]
        output = []
        for bin in num_of_bins:
            max = -1
            distrib = copy.deepcopy(exdf.population_age_distribution_default)
            distrib["num_bins"] = bin
            if bin != len(data):
                max = bin
            for i, column in enumerate(data.index):
                if len(column.split("_")) == 3:
                    _prefix, pre, pos = column.split("_")
                else:
                    pre, pos = column.split("_")
                if max - 1 == i or i == len(data) - 1:
                    distrib["distribution"].append([int(pre), 100, np.sum(data.iloc[i:])]) # add mean for data
                    break
                distrib["distribution"].append([int(pre), int(pos), data.iloc[i]])
            output.append(distrib)
        return output

    ## method for loading csv data and parsing them. Default its int:float pairs
    def load_employment_rates_by_age(self):
        csv_data_name="employment_rates_by_age"
        data=exut.load_datafile(self.data_files[csv_data_name])
        data.columns = map(str.lower, data.columns)

        region_name= self.region_parent_name.lower()
        location_code=self.location_code.lower()

        if location_code in data.head():
            index_name = location_code
        elif region_name is not None and region_name in data.head():
            index_name = region_name
        else:
            print(f"Cannot find region in {csv_data_name}. Region name: {region_name}, location code: {location_code}, using Defaults")
            return self.region_config[csv_data_name]
        output=[]
        # Convert all columns to lowercase
        for i,row in data.iterrows():
            output.append([int(row["age"]),float(row[index_name])])
        return output


    def load_enrollment_rates_by_age(self):
        csv_data_name="enrollment_rates_by_age"
        data=exut.load_datafile(self.data_files[csv_data_name])
        data.columns = map(str.lower, data.columns)
        region_name= self.region_parent_name.lower()
        location_code=self.location_code.lower()
        if location_code in data.head():
            index_name = location_code
        elif region_name is not None and region_name in data.head():
            index_name = region_name
        else:
            print(f"Cannot find region in {csv_data_name}. Region name: {region_name}, location code: {location_code}, using Defaults")
            return self.region_config[csv_data_name]
        output=[]
        # Convert all columns to lowercase
        for i,row in data.iterrows():
            output.append([int(row["age"]),float(row[index_name])])
        return output

    def load_household_head_age_brackets(self):
        csv_data_name="household_head_age_brackets"
        data=exut.load_datafile(self.data_files[csv_data_name])
        data.columns = map(str.lower, data.columns)
        output=[]
        # Convert all columns to lowercase
        for i,row in data.iterrows():
            output.append([int(row["min_age"]),int(row["max_age"])])
        return output

    def load_household_head_age_distribution_by_family_size(self):
        csv_data_name="household_head_age_distribution_by_family_size"
        data=exut.load_datafile(self.data_files[csv_data_name])
        data.columns = map(str.lower, data.columns)
        output=[]
        # Convert all columns to lowercase
        ind=0
        for i,row in data.iterrows():
            output.append([float(x) for x in row[:]])
            output[ind][0]=int(output[ind][0])
            ind+=1
        return output

    def load_household_size_distribution(self):
        csv_data_name="household_size_distribution"
        data=exut.load_datafile(self.data_files[csv_data_name])
        data.columns = map(str.lower, data.columns)
        output=[]
        for i,row in data.iterrows():
            output.append([int(row["num"]),float(row["distribution"])])
        return output

    def load_school_size_brackets(self):
        csv_data_name="school_size_brackets"
        data=exut.load_datafile(self.data_files[csv_data_name])
        data.columns = map(str.lower, data.columns)
        output=[]
        for i,row in data.iterrows():
            output.append([int(row["min"]),int(row["max"])])
        return output

    def load_school_distribution(self):
        csv_data_name="school_size_distribution"
        data=exut.load_datafile(self.data_files[csv_data_name])
        data.columns = map(str.lower, data.columns)
        output=[]
        for i,row in data.iterrows():
            output.append(float(row["distribution"]))
        return output

    def load_school_size_distribution(self):
        csv_data_name = "school_size_distribution_by_type"
        data = exut.load_datafile(self.data_files[csv_data_name])
        data.columns = map(str.lower, data.columns)
        output = []
        for _, row in data.iterrows():
            pattern = {
                "school_type": row["school_type"],
                "size_distribution": [float(x) for x in row["size_distribution"].split(",")],
            }
            output.append(pattern)
        return output

    def load_school_types(self):
        csv_data_name="school_types_by_age"
        data=exut.load_datafile(self.data_files[csv_data_name])
        data.columns = map(str.lower, data.columns)
        output=[]
        pattern={"school_type":"","age_range":[]}
        for i,row in data.iterrows():
            pattern["school_type"]=row["school_type"]
            pattern["age_range"]=[row["min_age"],row["max_age"]]
            output.append(pattern.copy())
        return output

    def load_workplace_size_counts(self):
        csv_data_name="workplace_size_counts_by_num_personnel"
        data=exut.load_datafile(self.data_files[csv_data_name])
        data.columns = map(str.lower, data.columns)
        output=[]
        for i,row in data.iterrows():
            output.append([int(row["min_people"]),int(row["max_people"]),float(row["count"])])
        return output

    def __str__(self):
        return f"Region: {self.region_name} ({self.location_code})\nParent: {self.region_parent_name}\nNotes: {self.notes}\n"



