from datetime import datetime, timedelta

import abmshare.covasim_ex.simulation_conf_getter as exscg
import abmshare.defaults as exdf
import abmshare.utils as exut
import covasim.immunity as cvim
import covasim.interventions as cvi


class MobilityIntervention:
    def __init__(self,days:list=None,start_day:str|datetime=None,end_day:str|datetime=None,label:str=None):
        # self.location_code=location_code
        # self.region_wide = True if isinstance(location_code,list) else False
        self.start_day=start_day if days is None else days[0]
        self.end_day=end_day if days is None else days[1]
        self.label=label

def mobility_change_intervention(intervention:dict,config:dict)->MobilityIntervention|None:
    """Function for creating mobility_change intervention

    Args:
        intervention (dict): Dictionary of keys for intervention
        config (dict): Base configuration file - for providing start daytime of simulation to calculate days

    Returns:
        Mobility_Intervention: obility intervention dataobject or None depend on validation

    """
    try:
        int_days=calculate_daytime(start_day=intervention.get("start_day"),end_day=intervention.get("end_day"),
                                    num_days=intervention.get("num_days"),config=config,return_days=True)
        return MobilityIntervention(start_day=int_days["start_day"],
                                    end_day=int_days["end_day"],
                                    label=intervention.get("label"))

    except:
        print(f"An error occured while processing mobility intervention:{intervention}")
        return None

def beta_change_intervention(intervention:dict,config:dict)->cvi.change_beta|None:
    """Function for creating beta_change intervention

    Args:
        intervention (dict): Dictionary of keys for intervention
        config (dict): Base configuration file - for providing start daytime of simulation to calculate days

    Returns:
        cvi.change_beta|None: beta_change intervention or None depend on validation

    """
    # try:
        # Calculate days
    int_days=calculate_daytime(start_day=intervention.get("start_day"),end_day=intervention.get("end_day"),
                            num_days=intervention.get("num_days"),config=config,return_days=True)
    # Validate consistency of dates and beta change values
    int_days=validate_days_and_beta_change(intervention=intervention,int_days=int_days)
    return cvi.change_beta(days=int_days,changes=intervention["beta_change"],layers=intervention.get("layers"),\
                        label=intervention.get("label"))
    # except Exception as e:
    #     print(f"An error occured: {e}, while processing beta_change intervention:{intervention}")
    #     return None


def isolate_contacts_intervention(intervention:dict,config:dict)->cvi.clip_edges|None:
    """Function for creating isolate_contacts intervention

    Args:
        intervention (dict): Dictionary of keys for intervention
        config (dict): Base configuration file - for providing start daytime of simulation to calculate days

    Returns:
        cvi.clip_edges|None: beta_change intervention or None depend on validation

    """
    try:
        int_days=calculate_daytime(start_day=intervention.get("start_day"),end_day=intervention.get("end_day"),
                                num_days=intervention.get("num_days"),config=config,return_days=True)
        int_days=validate_days_and_beta_change(intervention=intervention,int_days=int_days)
        # List for layers is ok, because covasim do double cecking in promotetolist method
        return cvi.clip_edges(days=int_days,changes=intervention.get("beta_change") if isinstance(intervention.get("beta_change",list)) else float(intervention.get("beta_change",1)),
                          layers=intervention.get("layers"),
                          label=intervention.get("label"))
    except Exception as e:
        print(f"An error occured: {e}, while processing isolate_contacts intervention:{intervention}")
        return None

def per_day_testing_intervention(intervention:dict,config:dict)->cvi.test_num:
    """Function for creating per_day_tetsing intervention

    Args:
        intervention (dict): Dictionary of keys for intervention
        config (dict): Base configuration file / for providing start daytime of simulation to calculate days

    Returns:
        cvi.test_num|None: per_day_testing intervention or None depend on validation

    """
    try:
        int_days=calculate_daytime(start_day=intervention.get("start_day"),end_day=intervention.get("end_day"),
                                num_days=intervention.get("num_days"),config=config,return_days=True)
        int_days=validate_days_and_beta_change(intervention=intervention,int_days=int_days)
        return cvi.test_num(daily_tests=intervention.get("daily_tests"), symp_test=intervention.get("symp_test",exdf.default_per_day_testing_values.get("symp_test")),
                            quar_test=intervention.get("quar_test",exdf.default_per_day_testing_values.get("quar_test")),quar_policy=intervention.get("quar_policy",exdf.default_per_day_testing_values.get("quar_policy")),
                            ili_prev=intervention.get("ili_prev"),sensitivity=intervention.get("sensitivity",exdf.default_per_day_testing_values.get("sensitivity")),
                            loss_prob=intervention.get("loss_prob",exdf.default_per_day_testing_values.get("loss_prob")),test_delay=intervention.get("test_delay",exdf.default_per_day_testing_values.get("test_delay")),
                            start_day=int_days[0] if not None and isinstance(int_days,list) else int_days if isinstance(int_days,int) else 0,
                            end_day=int_days[1] if len(int_days)>1 else None, label=intervention.get("label"))
    except Exception as e:
        print(f"An error occured: {e}, while processing per_day_testing intervention:{intervention}")
        return None

def testing_probability_intervention(intervention:dict,config:dict)->cvi.test_prob:
    """Function for creating testing_probability intervention

    Args:
        intervention (dict): Dictionary of keys for intervention
        config (dict): Base configuration file / for providing start daytime of simulation to calculate days

    Returns:
        cvi.test_prob|None: testing_probability intervention or None depend on validation

    """
    try:
        int_days=calculate_daytime(start_day=intervention.get("start_day"),end_day=intervention.get("end_day"),
                                num_days=intervention.get("num_days"),config=config,return_days=True)
        int_days=validate_days_and_beta_change(intervention=intervention,int_days=int_days)
        return cvi.test_prob(symp_prob=intervention.get("symp_prob",exdf.default_prob_testing_values.get("symp_prob")),
                            asymp_prob=intervention.get("asymp_prob",exdf.default_prob_testing_values.get("asymp_prob")),
                            symp_quar_prob=intervention.get("symp_quar_prob",exdf.default_prob_testing_values.get("symp_prob")),
                            asymp_quar_prob=intervention.get("asymp_quar_prob",exdf.default_prob_testing_values.get("asymp_prob")),
                            quar_policy=intervention.get("quar_policy",exdf.default_prob_testing_values.get("quar_policy")),
                            ili_prev=intervention.get("ili_prev"),sensitivity=intervention.get("sensitivity",exdf.default_prob_testing_values.get("sensitivity")),
                            loss_prob=intervention.get("loss_prob",exdf.default_prob_testing_values.get("loss_prob")),
                            test_delay=intervention.get("test_delay",exdf.default_prob_testing_values.get("test_delay")),
                            start_day=int_days[0] if not None and isinstance(int_days,list) else int_days if isinstance(int_days,int) else 0,
                            end_day=int_days[1] if len(int_days)>1 else None, label=intervention.get("label"))
    except Exception as e:
        print(f"An error occured: {e}, while processing testing_probability intervention:{intervention}")
        return None

def contact_tracing_intervention(intervention:dict,config:dict)->cvi.contact_tracing:
    """Function for creating contact_tracing intervention

    Args:
        intervention (dict): Dictionary of keys for intervention
        config (dict): Base configuration file / for providing start daytime of simulation to calculate days

    Returns:
        cvi.contact_tracing|None: contact_tracing intervention or None depend on validation

    """
    try:
        int_days=calculate_daytime(start_day=intervention.get("start_day"),end_day=intervention.get("end_day"),
                                num_days=intervention.get("num_days"),config=config,return_days=True)
        int_days=validate_days_and_beta_change(intervention=intervention,int_days=int_days)
        return cvi.contact_tracing(trace_probs=intervention.get("trace_probs"),
                            trace_time=intervention.get("trace_time"),
                            start_day=int_days[0] if not None and isinstance(int_days,list) else int_days if isinstance(int_days,int) else 0,
                            end_day=int_days[1] if isinstance(int_days,list) and len(int_days)>1 else None,presumptive=intervention.get("presumptive",exdf.default_contact_tracing_values["presumptive"]),
                            capacity=intervention.get("capacity",exdf.default_contact_tracing_values["capacity"]),quar_period=intervention.get("quar_period",exdf.default_contact_tracing_values["quar_period"]),
                            label=intervention.get("label"))
    except Exception as e:
        print(f"An error occured: {e}, while processing contact_tracing intervention:{intervention}")
        return None

def vaccinate_probability_intervention(intervention:dict,config:dict)->cvi.vaccinate_prob:
    """Function for creating vaccinate_probability intervention

    Args:
        intervention (dict): Dictionary of keys for intervention
        config (dict): Base configuration file / for providing start daytime of simulation to calculate days

    Returns:
        cvi.vaccinate_prob|None: vaccinate_probability intervention or None depend on validation

    """
    try:
        int_days=calculate_daytime(start_day=intervention.get("start_day"),end_day=intervention.get("end_day"),
                                num_days=intervention.get("num_days"),config=config,return_days=True)
        int_days=validate_days_and_beta_change(intervention=intervention,int_days=int_days)
        return cvi.vaccinate_prob(vaccine=intervention.get("vaccine"),
                            days=[int_days[0],int_days[1]] if len(int_days)>1 else int_days[0],
                            prob=intervention.get("prob",exdf.default_vaccinate_probability_values["prob"]),
                            booster=intervention.get("booster",exdf.default_vaccinate_probability_values["booster"]),label=intervention.get("label"))
    except Exception as e:
        print(f"An error occured: {e}, while processing testing_probability intervention:{intervention}")
        return None

def vaccinate_distribution_intervention(intervention:dict,config:dict)->cvi.vaccinate_num:
    """Function for creating vaccinate_distribution intervention

    Args:
        intervention (dict): Dictionary of keys for intervention
        config (dict): Base configuration file / for providing start daytime of simulation to calculate days

    Returns:
        cvi.vaccinate_prob|None: vaccinate_distribution intervention or None depend on validation

    """
    try:
        int_days=calculate_daytime(start_day=intervention.get("start_day"),end_day=intervention.get("end_day"),
                                num_days=intervention.get("num_days"),config=config,return_days=True)
        int_days=validate_days_and_beta_change(intervention=intervention,int_days=int_days)
        return cvi.vaccinate_num(vaccine=intervention.get("vaccine"),
                                days=[int_days[0],int_days[1]] if len(int_days)>1 else int_days[0],
                                num_doses=intervention.get("num_doses"),booster=intervention.get("booster",exdf.default_vaccinate_probability_values["booster"]),
                                sequence=intervention.get("sequence"),label=intervention.get("label"))
    except Exception as e:
        print(f"An error occured: {e}, while processing testing_probability intervention:{intervention}")
        return None

 #TODO: Test simple vaccine intervention

def simple_vaccine_intervention(intervention:dict,config:dict)->cvi.simple_vaccine:
    """Function for creating simple_vaccine intervention

    Args:
        intervention (dict): Dictionary of keys for intervention
        config (dict): Base configuration file / for providing start daytime of simulation to calculate days

    Returns:
        cvi.simple_vaccine|None: simple_vaccine intervention or None depend on validation

    """
    try:
        int_days=calculate_daytime(start_day=intervention.get("start_day"),end_day=intervention.get("end_day"),
                                num_days=intervention.get("num_days"),config=config,return_days=True)
        int_days=validate_days_and_beta_change(intervention=intervention,int_days=int_days)
        return cvi.simple_vaccine(prob=intervention.get("prob",1.0),
                            days=[int_days[0],int_days[1]] if len(int_days)>1 else int_days[0],
                            rel_sus=intervention.get("orig_rel_sus",0.0),
                            rel_symp=intervention.get("orig_rel_symp",0.0),
                            label=intervention.get("label"),)
    except Exception as e:
        print(f"An error occured: {e}, while processing simple_vaccine intervention:{intervention}")
        return None

def validate_days_and_beta_change(intervention:dict,int_days:dict):
        # If not end_day, then check if betachange is only one value, if yes, then set beta change as only value
        if int_days is None:
            raise Exception(f"Cannot validate days for intervention:{intervention} skipping this intervention")
        if int_days.get("end_day") is None:
            if isinstance(intervention.get("beta_change"),list) and len(intervention["beta_change"])==1:
                intervention["beta_change"]=intervention["beta_change"][0]
            elif isinstance(intervention.get("beta_change"),list) and len(intervention["beta_change"])==2:
                raise Exception(f"You cannot define two beta values when is only start_day of intervention defined, for intervention: {intervention}")
        # Check for two betas when two startdates exists otherwise return to 1
        if int_days["start_day"] is not None and int_days["end_day"] is not None and ((intervention.get("beta_change")) and len(intervention["beta_change"])==1):
            intervention["beta_change"]=[intervention["beta_change"][0],1]
        # Convert days back to ints after validation
        int_days=[int_days["start_day"],int_days["end_day"]] if int_days.get("end_day") else int_days["start_day"]
        return int_days


def validate_and_get_keys(intervention:dict, intervention_type:str)->bool:
    """Method to validate given keys and return if validation pass

    Args:
        intervention (dict): intervention dictionary from configuration
        intervention_type (str): name of intervention type

    Returns:
        bool: True - validation passes, False - incorrect keys

    """
    required_keys=exdf.intervention_mapping[intervention_type]["keys"]
    if not exut.validate_items_in_lists(list(intervention.keys()),required_keys):
        print(f"Cannot integrate intervention:{intervention}. Check if you have valid keys:\
                {exdf.interventions[intervention_type]}")
        return False
    return True

def calculate_daytime(start_day:str|datetime|int=None,end_day:str|datetime|int=None,num_days:int|str|list=None,config:dict|str=None,return_days:bool=False)->list|bool:
    """Complex time calculation
    
    Parameters
    ----------
        datetime format is: "%Y-%m-%d"
    Args:
        start_day (str | dt.datetime | int, optional): Start day of intervention by num of day represented as datetime or int. Defaults to None.
        end_day (str | dt.datetime | int, optional): End day of intervention by num of day represented as datetime or int Defaults to None.
        num_days (int | str | list, optional): Start and end of intervention time, Or start time - as integer only Defaults to None.
        config (dict | str, optional): base configuration file. Defaults to None.
        return_days (bool, optional): When false returns datetime, whent true returns days as ints Defaults to False.

    Returns
    -------
        list|bool: [start_day,end_day] in datetime or int days, depends on return_days boolean. Or False if not possible to calculatef

    """
    # sim_start_date=exscg.get_global_pars(config,'start_day') if not None else exdf.covasim_default_datetime # Get simulation date
    sim_start_datetime=exut.convert_str_to_date(exscg.get_global_pars(config,"start_day") if not None else exdf.covasim_default_datetime,exdf.covasim_datetime_format) # Get simulation date
    sim_end_datetime=exut.convert_str_to_date(exscg.get_global_pars(config,"start_day") if not None else exdf.covasim_default_datetime,exdf.covasim_datetime_format) # Get simulation date
    sim_end_datetime=sim_start_datetime + timedelta(days=exscg.get_global_pars(config,"n_days")) # Get simulation date
    # sim_start_datetime=dt.datetime.strptime(sim_start_date,exdf.covasim_datetime_format) # Convert to datetime
    if isinstance(num_days,str):
        try: num_days=int(num_days)
        except: pass #print(f"Cannot convert num_days:{num_days} of type:{type(num_days)} to int")

    try: start_daytime=exut.convert_str_to_date(start_day,exdf.covasim_datetime_format)
    except: start_daytime=int(start_day) if isinstance(start_day,str|int) else None
    try: end_daytime=exut.convert_str_to_date(end_day,exdf.covasim_datetime_format)
    except: end_daytime=int(end_day) if isinstance(end_day,str|int) else None

    if isinstance(start_daytime,int) and isinstance(end_daytime,int) and num_days is None: # If start_day and end_day are ints
        start_daytime=sim_start_datetime + timedelta(days=start_daytime)
        end_daytime=sim_start_datetime + timedelta(days=end_daytime)
    elif (start_daytime is not None and end_daytime is not None) and exut.compare_two_types(start_daytime,end_daytime) and start_daytime>=sim_start_datetime: # For given start day to end day
        pass
    elif start_daytime is not None and end_daytime is None and num_days is None: # If only start day is supplied
        if not return_days and isinstance(start_daytime,datetime):
            return {"start_day":exut.convert_date_to_str(start_daytime,exdf.covasim_datetime_format),"end_day":None}
        return {"start_day":start_daytime,"end_day":None}
    elif (start_daytime is not None and num_days is not None) and start_daytime>=sim_start_datetime: # For given num_day as end day, with supplied start day
        end_daytime=start_daytime + timedelta(days=num_days)
    elif (num_days is not None and isinstance(num_days,int)) and end_day is not None: # For given num_day as start day, with supplier end day
        start_daytime=sim_start_datetime + timedelta(days=num_days)
    elif isinstance(num_days,list): # For given num_day as start day and end day
        start_daytime=sim_start_datetime + timedelta(days=num_days[0])
        end_daytime=sim_start_datetime + timedelta(days=num_days[1])
    elif isinstance(start_daytime,int) and isinstance(end_daytime,datetime): # If start day is supplied only as int/str and end day as datetime
        start_daytime=sim_start_datetime + timedelta(days=start_daytime)
    elif isinstance(start_daytime,datetime) and isinstance(end_daytime,int): # If start day is supplied only as datetime and end day as int/str
        end_daytime=sim_start_datetime + timedelta(days=end_daytime)
    elif end_daytime is not None and start_daytime is None and num_days is None: # If only end day is supplied so start_day is from beginning
        start_daytime=sim_start_datetime
    # If nothing is supplied block
    elif start_daytime is None and end_daytime is None: # start and end from 0 to n_days of sim
        start_daytime=sim_start_datetime
        end_daytime=sim_end_datetime
    elif start_daytime is None: # If only end day is supplied so start_day is from beginning
        start_daytime=sim_start_datetime
    elif end_daytime is None: # If only end day is supplied so start_day is from beginning
        end_daytime=sim_end_datetime
    else:
        print("There is no possible combination for creating starting time")
        return None

    if not exut.compare_two_types(start_daytime,end_daytime): # Compare to be same types
        try:
            start_daytime=sim_start_datetime + timedelta(days=start_daytime) if not isinstance(start_daytime, datetime) else start_daytime
            end_daytime=sim_start_datetime + timedelta(days=end_daytime)  if not isinstance(end_daytime, datetime) else end_daytime
        except:
            print(f"Cannot convert start_day:{start_daytime} or end_day:{end_daytime} to datetime")
            return None
    if exut.compare_two_types(start_daytime,end_daytime) and start_daytime>=end_daytime: # Check for consistancy
        print(f"Start day:{start_daytime} is greater than end day:{end_daytime}")
        return None

    if not return_days:
        return {"start_day":exut.convert_date_to_str(start_daytime,exdf.covasim_datetime_format),"end_day":exut.convert_date_to_str(end_daytime,exdf.covasim_datetime_format)}
    return {"start_day":(start_daytime-sim_start_datetime).days,"end_day":(end_daytime-sim_start_datetime).days}

def process_interventions(interventions:list,config:dict)->list:
    """Intervention process

    Args:
        interventions (list): intervention list
        config (dict): main configuration file

    Returns:
        list: _description_

    """
    if not interventions:
        return []
    intervention_list=[]
    for intervention in interventions:
        if intervention[exdf.confkeys["type"]]==exdf.intervention_names_mapping["beta_change"]: # SHOULD BE ALSO VALIDATION
            try:
                intervention_list.append(beta_change_intervention(intervention=intervention,config=config))
            except Exception as e:
                print(f"An error occured: {e}, while processing intervention:{intervention}")
        if intervention[exdf.confkeys["type"]]==exdf.intervention_names_mapping["mobility_change"]: # SHOULD BE ALSO VALIDATION
            try:
                intervention_list.append(mobility_change_intervention(intervention=intervention,config=config))
            except Exception as e:
                print(f"An error occured: {e}, while processing intervention:{intervention}")
        if intervention[exdf.confkeys["type"]]==exdf.intervention_names_mapping["isolate_contacts"]: # SHOULD BE ALSO VALIDATION
            try:
                intervention_list.append(isolate_contacts_intervention(intervention=intervention,config=config))
            except Exception as e:
                print(f"An error occured: {e}, while processing intervention:{intervention}")
        if intervention[exdf.confkeys["type"]]==exdf.intervention_names_mapping["per_day_testing"]: # SHOULD BE ALSO VALIDATION
            try:
                intervention_list.append(per_day_testing_intervention(intervention=intervention,config=config))
            except Exception as e:
                print(f"An error occured: {e}, while processing intervention:{intervention}")
        if intervention[exdf.confkeys["type"]]==exdf.intervention_names_mapping["testing_probability"]: # SHOULD BE ALSO VALIDATION
            try:
                intervention_list.append(testing_probability_intervention(intervention=intervention,config=config))
            except Exception as e:
                print(f"An error occured: {e}, while processing intervention:{intervention}")
        if intervention[exdf.confkeys["type"]]==exdf.intervention_names_mapping["contact_tracing"]: # SHOULD BE ALSO VALIDATION
            try:
                intervention_list.append(contact_tracing_intervention(intervention=intervention,config=config))
            except Exception as e:
                print(f"An error occured: {e}, while processing intervention:{intervention}")
        if intervention[exdf.confkeys["type"]]==exdf.intervention_names_mapping["vaccinate_probability"]: # SHOULD BE ALSO VALIDATION
            try:
                intervention_list.append(vaccinate_probability_intervention(intervention=intervention,config=config))
            except Exception as e:
                print(f"An error occured: {e}, while processing intervention:{intervention}")
        if intervention[exdf.confkeys["type"]]==exdf.intervention_names_mapping["vaccinate_distribution"]: # SHOULD BE ALSO VALIDATION
            try:
                intervention_list.append(vaccinate_distribution_intervention(intervention=intervention,config=config))
            except Exception as e:
                print(f"An error occured: {e}, while processing intervention:{intervention}")
        if intervention[exdf.confkeys["type"]]==exdf.intervention_names_mapping["simple_vaccination"]: # SHOULD BE ALSO VALIDATION
            try:
                intervention_list.append(simple_vaccine_intervention(intervention=intervention,config=config))
            except Exception as e:
                print(f"An error occured: {e}, while processing intervention:{intervention}")
        if len(intervention_list)>0 and intervention_list[-1] is None: # Remove None intervention
                    intervention_list.pop()
    return intervention_list

def create_variants(config:str|dict,code:str):
    config=exut.load_config(config)
    if config.get("variants",None) is None or config["variants"].get("filepath",None) is None:
        return []
    try:
        data=exut.load_datafile(config["variants"]["filepath"])
        location_codes=[x.lower() for x in[code,exscg.get_region_parent_name(config,code),"global"]]
    except:
        print(f"Cannot load variants datafile:{config['variants']['filepath']}")
        return []
    indexes=data.loc[data["location_code"].str.lower().isin(location_codes)].index
    # Prepare
    prep_output=[]
    for i in indexes:
        if not data.iloc[i]["use"]:
            continue
        d={}
        for key in data.columns:
            if key in exdf.interventions["variant"]:
                d[key]=data.loc[i,key]
        prep_output.append(d)
    # Finalize
    output=[]
    for variant in prep_output:
        int_days=calculate_daytime(start_day=variant.get("start_day",None),end_day=variant.get("end_day",None),
                            num_days=variant.get("num_days"),config=config,return_days=True)
        int_days=validate_days_and_beta_change(intervention=variant,int_days=int_days)
        output.append(cvim.variant(variant=variant.get("variant",None),
                                   days=[int_days[0],int_days[1]] if len(int_days)>1 else int_days[0],
                                   label=variant.get("label",None),
                                   n_imports=variant.get("number_of_imports",1),
                                   rescale=variant.get("rescale",False),
                                   ))
    return output

# testing only
# import extensions.covasim_ex.immunity_process as eximm
# import covasim.parameters as cvpar
# if __name__=="__main__":
#     config="/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/simulation_with_variants.json"
#     meh=eximm.ImmunityProcessing(config)
#     interventions=exscg.get_interventions_by_code(config,code="CZ01")
#     variants=create_variants(config,code="CZ01")
# #     intervent=process_interventions(interventions,config)
#     print()
    # meh=calculate_daytime(config=config,start_day="2020-03-01",end_day="2020-03-10",return_days=True)
    # meh1=calculate_daytime(config=config,start_day="2020-03-01",num_days=10,return_days=True)
    # meh2=calculate_daytime(config=config,num_days=10,end_day="2020-03-10")
    # meh3=calculate_daytime(config=config,num_days=[10,20])
    # meh4=calculate_daytime(config=config,start_day=20,end_day=30)
    # meh5=calculate_daytime(config=config)
    # meh6=calculate_daytime(config=config,end_day=20)
    # beta_change=beta_change_intervention(interventions[1],config=config)
    # beta_change1=beta_change_intervention(interventions[3],config=config)
    # mobility_change=mobility_change_intervention(interventions[0],config=config)
    # mobility_change2=mobility_change_intervention(interventions[1],config=config)
    # isolate_contacts=isolate_contacts_intervention(interventions[7],config=config)
    # isolate_contacts2=isolate_contacts_intervention(interventions[8],config=config)
    # per_day_testing=per_day_testing_intervention(interventions[9],config=config)
    # per_day_testing2=per_day_testing_intervention(interventions[10],config=config)
    # per_day_testing3=per_day_testing_intervention(interventions[11],config=config)
    # testing_probability_testing=testing_probability_intervention(interventions[12],config=config)
    # testing_probability_testing2=testing_probability_intervention(interventions[13],config=config)
    # testing_probability_testing3=testing_probability_intervention(interventions[14],config=config)
    # contact_tracing_testing=contact_tracing_intervention(interventions[15],config=config)
    # contact_tracing_testing2=contact_tracing_intervention(interventions[16],config=config)
    # contact_tracing_testing3=contact_tracing_intervention(interventions[17],config=config)
    # vaccinate_probability_testing=vaccinate_probability_intervention(interventions[18],config=config)
    # vaccinate_probability_testing2=vaccinate_probability_intervention(interventions[19],config=config)
    # vaccinate_probability_testing3=vaccinate_probability_intervention(interventions[20],config=config)
    # vaccinate_distribution_testing=vaccinate_distribution_intervention(interventions[18],config=config)
    # vaccinate_distribution_testing2=vaccinate_distribution_intervention(interventions[19],config=config) # No days working now
    # interv=process_interventions(interventions,config)
    #TODO: weekends
    # print()

