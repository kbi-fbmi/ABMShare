import numpy as np
import covasim as cv
import abmshare.defaults as exdf
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

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
  

def interactions(sims,mobility,pop_sz,init_interaction=False):
    '''
        Method for applying interactions between same persons in different region.
        Calls indexing and synchronizing.
        Initial interaction is for synchronizing people right before simulation starts.
        So it copy one person to another sim.
        pop_sz (list)                   : list of ints representing num of people, must be without added mobility
    '''
    for id1,s1 in enumerate(sims):
        for id2,s2 in enumerate(sims):
            if(id1 == id2):
                continue                     
            (mob_id1, mob_id2) = mobility_indexes(mobility,pop_sz, id1,id2)
            synchronize_people(s1,s2,mob_id1,mob_id2,init_interaction)