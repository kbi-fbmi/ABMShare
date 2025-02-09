import numpy as np
import pandas as pd
import abmshare.defaults as exdf
import random as rnd
# warnings.simplefilter(action='ignore', category=FutureWarning)

'''
Methods for synchronizing people in other sims.
Basically person who works/study in different region has probability to be in contact with infectious person. 
If it happens, then he is synchronized as well with his "home region", as with his foreign region.
'''


def synchronize_people(s1, s2, c1_ids,c2_ids,init_infection=False):
    '''
    Method for synchronize people in different regions.
    s1 = home region simulation
    s2 = foreign region simulation
    c1_ids,c2_ids = indexes calculated via "mobility_indexes" method. It works the way that, for example person id[2] in s1 is the same as person id[end-2] in s2
    init_infection(bool)            : if its init infection, then synchronize all pars
    '''   
    for par in exdf.person_all_states:
        if par == 'uid':
            continue   
        p1 = getattr(s1.people, par)[c1_ids]
        p2 = getattr(s2.people, par)[c2_ids]
        m_id = np.where(np.logical_xor(np.isnan(p1),np.isnan(p2)) | (~np.isnan(p1) & ~np.isnan(p2) & (p1 != p2)))[0]
        for id in m_id:
            if np.isnan(p1[id]):            
                getattr(s1.people, par)[c1_ids[id]] = getattr(s2.people, par)[c2_ids[id]]
            elif np.isnan(p2[id]):
                getattr(s2.people, par)[c2_ids[id]] = getattr(s1.people, par)[c1_ids[id]]
            elif p1[id] != p2[id]:
                getattr(s2.people, par)[c2_ids[id]] = getattr(s1.people, par)[c1_ids[id]]
            
    for par in exdf.person_arrays:
        for variant in range(s1.pars['n_variants']):
            # p1 = getattr(s1.people, par)[variant][[c1_ids]]
            # p2 = getattr(s2.people, par)[variant][[c2_ids]]                                                       
            p1 = getattr(s1.people, par)[variant][c1_ids]
            p2 = getattr(s2.people, par)[variant][c2_ids]
            m_id = np.where(np.logical_xor(np.isnan(p1), np.isnan(p2)) | (~np.isnan(p1) & ~np.isnan(p2) & np.not_equal(p1, p2)))[0]
            
            for id in m_id:
                if np.isnan(p1[id]):
                    getattr(s1.people, par)[variant][c1_ids[id]] = getattr(s2.people, par)[variant][c2_ids[id]]
                elif np.isnan(p2[id]):
                    getattr(s2.people, par)[variant][c2_ids[id]] = getattr(s1.people, par)[variant][c1_ids[id]]
                elif np.not_equal(p1[id], p2[id]):
                    getattr(s2.people, par)[variant][c2_ids[id]] = getattr(s1.people, par)[variant][c1_ids[id]]


# def create_default_mobility_indexes(region_list:dict):
#     """ Method for standard picking indexes for mobility
#     Outcoming are starting from 0, outcoming after max popsize

#     Args:
#         region_list (dict): _description_
#     """
#     for loc_code1,region1 in region_list.items():
#         for loc_code2,region2 in region_list.items():
#             output={}
#             if loc_code1==loc_code2:
#                 continue
#             keys=list(region1.mobility_data.keys())
#             orig_population_size=region2.original_population_size
#             min_id1 = sum([v for k,v in region1.mobility_data.items() if keys.index(k) < keys.index(region2.location_code) and not pd.isna(v)]) #From
#             max_id1 = sum([v for k,v in region1.mobility_data.items() if keys.index(k) <= keys.index(region1.location_code)+1 and not pd.isna(v)]) # To

#             min_id2=orig_population_size+min_id1
#             max_id2=orig_population_size+max_id1

#             output[loc_code2]=(list(range(int(min_id1), int(max_id1))), list(range(int(min_id2), int(max_id2))))

def extract_indexes(random_indexes, count):
    """Helper function for creating random mobility indexes

    Args:
        random_indexes (_type_): random indexes to pick from
        count (_type_): number of random indexes to pick

    Returns:
        list: list of indexes by specific range
    """
    out = set(rnd.sample(list(random_indexes), count))
    random_indexes -= out
    return list(out)

def create_random_mobility_indexes(region_list:dict):    
    """ Method for random picking indexes for mobility

    Args:
        region_list (dict): _description_
    """
    for key, val in region_list.items():
        total_sum = int(sum(v for v in val.mobility_incoming_data.values() if not pd.isna(v)))
        total_sum+=int(sum(v for v in val.mobility_data.values() if not pd.isna(v)))
        # Use a set for random_indexes for faster membership checks and differences
        random_indexes = set(rnd.sample(range(int(val.population_size)), total_sum))
        incoming_dict={}
        outcoming_dict={}
        for key2, val2 in region_list.items():
            incoming_indexes, outcoming_indexes = [], []
            if key == key2:
                continue
                
            count_in = int(val.mobility_incoming_data.get(key2))
            count_out = int(val.mobility_data.get(key2))
            
            # Extract incoming and outcoming indexes
            incoming_indexes.extend(extract_indexes(random_indexes, count_in))
            outcoming_indexes.extend(extract_indexes(random_indexes, count_out))

            incoming_dict[key2]=incoming_indexes
            outcoming_dict[key2]=outcoming_indexes

        val.unique_mobility_indexes = {
            "incoming_indexes":incoming_dict,
            "outcoming_indexes":outcoming_dict
        }


def interactions(region_list:dict,init:bool=False):
    if init:
        create_random_mobility_indexes(region_list=region_list)
    for key0,reg0 in region_list.items():
        for key1,reg1 in region_list.items():
            if key0==key1:
                continue
            elif reg0.mobility_data is None or reg1.mobility_data is None: # If there is no mobility at all
                continue
            synchronize_people(reg0.cv_simulation,reg1.cv_simulation,reg0.unique_mobility_indexes.get("outcoming_indexes").get(key1),
                               reg1.unique_mobility_indexes.get("incoming_indexes").get(key0),init_infection=init)



def mobility_indexes(mobility,pop_sz,id1,id2):
    '''
        This method returns a list representing persons who are travelling across regions (sims).
        For every region
    '''
    min_id1 = np.concatenate(([0],np.cumsum(mobility[id1,:])))[id2]
    max_id1 = np.concatenate(([0],np.cumsum(mobility[id1,:])))[id2+1]
    
    min_id2 = pop_sz[id2] + np.concatenate(([0],np.cumsum(mobility[:,id2])))[id1]
    max_id2 = pop_sz[id2] + np.concatenate(([0],np.cumsum(mobility[:,id2])))[id1+1]    
    return ( list(range(int(min_id1), int(max_id1))), list(range(int(min_id2), int(max_id2))) )
  

def interactions_default(region_list:dict,init_bool=False): #TODO:...
    '''
        Method for applying interactions between same persons in different region.
        Calls indexing and synchronizing.
        Initial interaction is for synchronizing people right before simulation starts.
        So it copy one person to another sim.
        pop_sz (list)                   : list of ints representing num of people, must be without added mobility        
    '''
    pop_sz=np.array([x.original_population_size for x in region_list.values()])
    mobility=np.array([[x.mobility_data.get(y.location_code) for y in region_list.values()] for x in region_list.values()])
    for id1,s1 in enumerate(region_list.items()):
        for id2,s2 in enumerate(region_list.items()):
            if(id1 == id2):
                continue                     
            (mob_id1, mob_id2) = mobility_indexes(mobility,pop_sz, id1,id2)
            synchronize_people(s1,s2,mob_id1,mob_id2,init_bool)



# def load_pop_and_mob(mobilitypath=None,populationpath=None):
#     '''
#         Method for initializing mobility and population data. If there is no data given, it loads defaults
#         Method is called in constructor, no need to call it directly.
#         !!Important!! always use absolute path if data are given.
#     '''
#     if  mobilitypath is not None:
#         mobility=exut.load_datafile(mobilitypath)
#     if mobility is not None:
#         mobility=np.asarray(mobility[mobility.columns[2:]])
#         mobility[np.isnan(mobility)] = 0           

#     if populationpath is not None:
#         population=exut.load_datafile(populationpath)
#     if population is not None:
#         population=np.array(population.population_size,dtype=int)  
#     return population,mobility
# if __name__=="__main__":
#     # old approach

#     population,mobility=load_pop_and_mob(mobilitypath="/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/data/NUTS2_mobility_data.csv",
#                                             populationpath="/storage/ssd2/sharesim/share-covasim/Tests/test_outputs3/ABM_share_meta/input_data/data/population_age_distributions.csv")
#     test0=old_mobility_indexes(mobility,population,0,2)
#     test1=old_mobility_indexes(mobility,population,0,3)
#     test2=old_mobility_indexes(mobility,population,0,4)
#     test3=old_mobility_indexes(mobility,population,0,5)
#     test4=old_mobility_indexes(mobility,population,1,0)
#     test5=old_mobility_indexes(mobility,population,2,0)
#     test6=old_mobility_indexes(mobility,population,3,4)
#     print()
    