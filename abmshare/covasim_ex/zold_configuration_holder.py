# Core function for initializiing everything from configuration file
from covasim.run import parallel
from covasim.utils import false
from abmshare.covasim_ex.mobility_old import interactions
import abmshare.defaults as exdf
import abmshare.utils as exut
import os

# Class for handling and returning items
class ConfigurationHolder:
    def __init__(self,configuration,test=False,parallel_run=False):
        # Load json file or can be already loaded dict of pars
        if not isinstance(configuration,dict):
            self.configuration=exut.load_config(configuration)
        else:
            self.configuration=configuration
        self.test=test
        #Holder
        self.mobility_path=None      
        self.population_path=None
        self.sim_pars=[]
        self.run_settings_pars=dict()
        self.interventions=[]
        self.variants=[]
        self.interventions_different_bool=False
        self.variants_different_bool=False
        self.mobility_interventions_bool=False
        self.pars_different_bool=False
        self.num_of_sims=None
        self.save_pars=dict()
        self.parse_pars()

    # In development
    def parse_pars(self):
        '''
            Core function of parsing all covasim configuration
        '''
        conf=self.configuration #For shorter usage
        #Assign some values
        self.pars_different_bool=conf[exdf.confkeys['different_pars']]['value']
        if self.pars_different_bool:
            self.num_of_sims=len(conf[exdf.confkeys['different_pars']]['regions'])
            exut.fill_list(self.interventions,self.num_of_sims)
            exut.fill_list(self.variants,self.num_of_sims)   
            self.parse_different_pars()
        else:
            self.num_of_sims=conf[exdf.confkeys['global_pars']]['num_of_sims']
            exut.fill_list(self.interventions,self.num_of_sims) 
            exut.fill_list(self.variants,self.num_of_sims)               
            self.parse_global_pars()

        #If there are mobility pars (can also be empty string)
        if conf[exdf.confkeys['mobility_pars']]['value']:            
            self.mobility_path=conf[exdf.confkeys['mobility_pars']]['filepath']

        #If there are (can also be empty string)
        if conf[exdf.confkeys['population_pars']]['value']:
            self.population_path=conf[exdf.confkeys['population_pars']]['filepath']

        #Handle if there are not separated interventions
        if not self.interventions_different_bool:
            for intervention in conf[exdf.confkeys['interventions']][exdf.confkeys['intervention_list']]:
                for inter in self.interventions:
                    inter.append(intervention)
            if len(conf[exdf.confkeys['interventions']][0]) < 1: # if there is no interventions at all
                for inter in self.interventions:
                    inter.append(None)
            
        # Handle saving pars
        if conf.get(exdf.confkeys['save_pars'],False) and conf[exdf.confkeys['save_pars']].get('value',False):
            self.save_pars=dict()
            for key,value in conf[exdf.confkeys['save_pars']].items():
                self.save_pars[key]=value
        
        # Handle variant pars
        if exdf.confkeys['variants'] in conf and exdf.confkeys['include_with_different'] in conf[exdf.confkeys['variants']]:
            if exdf.confkeys['include_with_different'] in conf[exdf.confkeys['variants']] and conf[exdf.confkeys['variants']][exdf.confkeys['include_with_different']]:
                pass #TODO include different k soucasnym
            elif exdf.confkeys['global_only'] in conf[exdf.confkeys['variants']] and conf[exdf.confkeys['variants']][exdf.confkeys['global_only']]:
                pass #TODO rewrite and set only to global variants
                # self.parse_variants(conf[exdf.confkeys['variants']])

        # Handle parallel run pars
        if 'parallel_run' in conf and conf['parallel_run'] == True:
            self.run_settings_pars['parallel_run']=True
        elif 'parallel_run' in conf and conf['parallel_run'] != True:
            self.run_settings_pars['parallel_run']=False
        else:
            self.run_settings_pars['parallel_run']=False
        # Handle global_pars and global_interventions for including with different
        self.check_global_pars()
        self.check_global_interventions()
        self.check_global_variants()
        self.variants=exut.check_variant(self.variants) # Check and maintain variants
        print()
    
    def check_global_interventions(self):
        '''
            Method for handling inlcude_with_different interventions
        '''
        conf = self.configuration[exdf.confkeys['interventions']]
        if conf[exdf.confkeys['global_only']]: #Override to global pars
            self.parse_global_pars(pars_only_choice=False)
        elif conf[exdf.confkeys['include_with_different']]:
            for intervention in conf[exdf.confkeys['intervention_list']]:
                for intervention_made in self.interventions:
                    intervention_made.append(intervention)
        pass
    
    def check_global_variants(self):
        '''
            Method for handling include_with_different variants
        '''
        try:        
            conf=self.configuration[exdf.confkeys['variants']]
            if conf[exdf.confkeys['global_only']]:  #Override to global pars
                self.parse_global_pars(pars_only_choice=False)
            elif conf[exdf.confkeys['include_with_different']]:
                try:
                    for i in range(self.num_of_sims):
                        exut.append_variant(base_variant_list=self.variants,variants=self.parse_variants(conf[exdf.confkeys['variant_list']]),id=i)
                except:
                    print(f"Cannot parse variants:\n {conf[exdf.confkeys['variant_list']]}")   
        except:
            print(f"An error occured while including global variants in different variants.")


    def check_global_pars(self):
        '''
            Method for checking global pars after making basic pars.
            And for overrite with warning
        '''
        conf=self.configuration[exdf.confkeys['global_pars']]
        if conf[exdf.confkeys['global_only']]: # If there are only global pars
            if len(self.sim_pars)>0:
                print("Overriding created pars. If this is unintentionally, then change global_only to False")            
            self.parse_global_pars(interventions_choice=False,variant_choice=False)

        elif conf[exdf.confkeys['include_with_different']] and conf[exdf.confkeys['include_keys']]: # If include global pars and only speccific keys
            for sim in self.sim_pars:
                for key,value in conf.items():
                    if exut.validate_pars(key,conf[exdf.confkeys['include_keys']]) and exut.validate_pars(key,exdf.covasim_pars_all):
                        sim[key]=value
        elif conf[exdf.confkeys['include_with_different']] and not conf[exdf.confkeys['include_keys']]:
            for sim in self.sim_pars:
                for key,value in conf.items():
                    if exut.validate_pars(key,exdf.covasim_pars_all):
                        sim[key]=value
        return    


    def parse_global_pars(self,interventions_choice=True,variant_choice=True,pars_only_choice=True):
        '''
            If there are global pars only, then create them in the num of given in config file.
            Also check for test to optimize max. people by default test value.
            interventions_choice (bool)             : if remake only global interventions
            variant_choice(bool)                    : if remake only global variants
            pars_only_choice (bool)                 : if remake only sim pars
        '''
        conf=self.configuration
        if 'num_of_sims' in conf[exdf.confkeys['global_pars']] or self.num_of_sims is not None:
            if pars_only_choice:
                for i in range(conf[exdf.confkeys['global_pars']]['num_of_sims']):
                    pars=conf[exdf.confkeys['global_pars']].copy()
                    # If there is pop_infected
                    if 'pop_infected' in pars:
                        pars['pop_infected']=conf[exdf.confkeys['global_pars']]['pop_infected'][i]
                    if 'num_of_sims' in pars: # Delete num of sims from config - dont need for sim
                        self.num_of_sims=pars['num_of_sims']
                        del pars['num_of_sims']
                    if not 'pop_size' in pars or self.test:
                        pars['pop_size']=exdf.test_n_people
                    self.sim_pars.append(pars)
            # Handle also global interventions
            if interventions_choice:        
                if conf[exdf.confkeys['interventions']]['global_only']:
                    for i in self.interventions:
                        i.append(conf[exdf.confkeys['interventions']]['intervention_list'])
            if variant_choice:
                if exdf.confkeys['global_only'] in conf[exdf.confkeys['variants']] and conf[exdf.confkeys['variants']][exdf.confkeys['global_only']]:
                    try:
                        for i in range(self.num_of_sims):
                            exut.append_variant(base_variant_list=self.variants,variants=self.parse_variants(conf[exdf.confkeys['variants']][exdf.confkeys['variant_list']]),id=i)
                    except:
                        print(f"Cannot parse variants:\n {conf[exdf.confkeys['variants']][exdf.confkeys['variant_list']]}")                   
        else:                    
            self.sim_pars.append(conf[exdf.confkeys['global_pars']])

    def parse_different_pars(self):
        conf=self.configuration # For shorter usage
        if exdf.confkeys['interventions_different'] in conf[exdf.confkeys['different_pars']]:
            self.interventions_different_bool=conf[exdf.confkeys['different_pars']][exdf.confkeys['interventions_different']]
        if exdf.confkeys['variants_different'] in conf[exdf.confkeys['different_pars']]:
            self.variants_different_bool=conf[exdf.confkeys['different_pars']][exdf.confkeys['variants_different']]
        for i,region in enumerate(conf[exdf.confkeys['different_pars']]['regions']):
                self.sim_pars.append(region[exdf.confkeys['simulation_pars']])
                # also check for interventions, if they are separate
                if exdf.confkeys['interventions'] in region and self.interventions_different_bool:
                    for inter in region[exdf.confkeys['interventions']]:
                        self.interventions[i].append(inter)
                else:
                    self.interventions[i]=[]
                # check for variants same way
                if (exdf.confkeys['variants'] in region and len(region[exdf.confkeys['variants']])>0) and self.variants_different_bool:
                    exut.append_variant(base_variant_list=self.variants,variants=self.parse_variants(conf=region[exdf.confkeys['variants']]),id=i)

    def parse_variants(self,conf):
        '''
            Conf(str/dict)  : can be precisely dict of variant vars
            id(int)         : id of
        '''     
        variant_list=[]
        for variant in conf:
            variant_dict={}          
            if isinstance(variant[exdf.confkeys['variant']],str):
                variant_dict[exdf.confkeys['variant']]=variant[exdf.confkeys['variant']]
            elif isinstance(variant[exdf.confkeys['variant']],dict):
                variant_dict[exdf.confkeys['variant']]={}
                for key in variant[exdf.confkeys['variant']]:
                    if key in exdf.custom_variant_keys:
                        variant_dict[exdf.confkeys['variant']][key] = variant[exdf.confkeys['variant']][key]
                    else:
                        print(f"Key {key} is not a valid key for a variant. Please use only this keys: {exdf.custom_variant_keys}")
                        return False
            else:
                print("This variant type is not supported.")
                return                
            for key in variant:  
                if key == exdf.confkeys['variant']:
                    continue
                if key in exdf.simulation_variant_keys:
                    variant_dict[key]=variant[key]
                else:
                    print(f"This key {key} is no a valid key for variant creation. Please use only keys: {exdf.simulation_variant_keys}")
                    return False
            variant_list.append(variant_dict)
        return variant_list

    def return_pars(self,pars_type=None):
        if pars_type=="covasim" or pars_type==None:
            return self.sim_pars
        elif pars_type=="interventions":
            return self.interventions
        elif pars_type=="run_settings_pars":
            return self.run_settings_pars
        elif pars_type=="variants":
            return self.variants
        return self.sim_pars

    def return_number_of_sims(self):
        if len(self.sim_pars)<1:
            print("There is no sim provided")
        else:
            return self.num_of_sims


            
        

