"""Defines functions for making the population.
"""

from collections import defaultdict

import numpy as np
import sciris as sc

from . import loaders as spl
from . import people as spp
from . import utils as spu

# Specify all externally visible functions this file defines
__all__ = ["make_people", "make_randpop", "make_random_contacts",
           "make_microstructured_contacts", "make_hybrid_contacts",
           "parse_synthpop"]


def make_people(n=None, popdict=None, rand_seed=1, pop_type="synthpops", location=None, save_pop=False, popfile=None, die=True, verbose=None, **kwargs):
    """Make the actual people for the simulation. Usually called via sim.initialize(),
    but can be called directly by the user.

    Args:
        n        (int)  : the number of people to create
        popdict  (dict) : if supplied, use this population dictionary instead of generating a new one
        save_pop (bool) : whether to save the population to disk
        popfile  (bool) : if so, the filename to save to
        die      (bool) : whether or not to fail if synthetic populations are requested but not available
        verbose  (bool) : level of detail to print
        kwargs   (dict) : passed to make_randpop() or make_synthpop()

    Returns:
        people (People): people

    New in version 1.10.0.

    """
    if popdict is not None:
        popdict = sc.dcp(popdict) # Otherwise, modifies in place
        n = len(popdict)

    pars = dict(
            pop_size   = n,
            pop_type   = pop_type,
            rand_seed  = rand_seed,
            location   = location,
            verbose    = 0,
            contacts   = dict(h=2.0, s=20,  w=16,  c=20),
        )

    # Set inputs and defaults
    pop_size = int(pars["pop_size"]) # Shorten
    pop_type = pars["pop_type"] # Shorten
    if verbose is None:
        verbose = pars["verbose"]

    # Actually create the population
    if popdict is None: # Main use case: no popdict is supplied
        # Create the population
        if pop_type in ["random", "clustered", "hybrid"]:
            popdict = make_randpop(pars, microstructure=pop_type, **kwargs)
        else: # pragma: no cover
            errormsg = f'Population type "{pop_type}" not found; choices are random, clustered, hybrid, or synthpops'
            raise ValueError(errormsg)
    else:
        popdict = parse_synthpop(popdict)

    # Actually create the people
    people = spp.People(pars, uid=popdict["uid"], age=popdict["age"], sex=popdict["sex"], contacts=popdict["contacts"]) # List for storing the people

    average_age = sum(popdict["age"]/pop_size)
    sc.printv(f"Created {pop_size} people, average age {average_age:0.2f} years", 2, verbose)

    if save_pop:
        if popfile is None: # pragma: no cover
            errormsg = "Please specify a file to save to using the popfile kwarg"
            raise FileNotFoundError(errormsg)
        filepath = sc.makefilepath(filename=popfile)
        sc.saveobj(filepath, people)
        if verbose:
            print(f'Saved population of type "{pop_type}" with {pop_size:n} people to {filepath}')

    return people


def make_randpop(sim, use_age_data=True, use_household_data=True, sex_ratio=0.5, microstructure=False):
    """Make a random population, with contacts.

    This function returns a "popdict" dictionary, which has the following (required) keys:

        - uid: an array of (usually consecutive) integers of length N, uniquely identifying each agent
        - age: an array of floats of length N, the age in years of each agent
        - sex: an array of integers of length N (not currently used, so does not have to be binary)
        - contacts: list of length N listing the contacts; see make_random_contacts() for details
        - layer_keys: a list of strings representing the different contact layers in the population; see make_random_contacts() for details

    Args:
        sim (Sim): the simulation object
        use_age_data (bool): whether to use location-specific age data
        use_household_data (bool): whether to use location-specific household size data
        sex_ratio (float): proportion of the population that is male (not currently used)
        microstructure (bool): whether or not to use the microstructuring algorithm to group contacts

    Returns:
        popdict (dict): a dictionary representing the population, with the following keys for a population of N agents with M contacts between them:
    
    New in version 1.10.0.

    """
    pop_size = int(sim["pop_size"]) # Number of people

    # Load age data and household demographics based on 2018 Seattle demographics by default, or country if available
    age_data = spl.default_age_data
    location = sim["location"]
    if location is not None:
        if sim["verbose"]:
            print(f'Loading location-specific data for "{location}"')
        if use_age_data:
            try:
                age_data = spl.get_age_distribution(location)
            except ValueError as E:
                print(f'Could not load age data for requested location "{location}" ({str(E)}), using default')
        if use_household_data:
            try:
                household_size = spl.get_household_size(location)
                if "h" in sim["contacts"]:
                    sim["contacts"]["h"] = household_size - 1 # Subtract 1 because e.g. each person in a 3-person household has 2 contacts
                else:
                    keystr = ", ".join(list(sim["contacts"].keys()))
                    print(f'Warning; not loading household size for "{location}" since no "h" key; keys are "{keystr}". Try "hybrid" population type?')
            except ValueError as E:
                if sim["verbose"]>=2: # These don't exist for many locations, so skip the warning by default
                    print(f'Could not load household size data for requested location "{location}" ({str(E)}), using default')

    # Handle sexes and ages
    uids           = np.arange(pop_size, dtype=spu.default_int)
    sexes          = np.random.binomial(1, sex_ratio, pop_size)
    age_data_min   = age_data[:,0]
    age_data_max   = age_data[:,1] + 1 # Since actually e.g. 69.999
    age_data_range = age_data_max - age_data_min
    age_data_prob  = age_data[:,2]
    age_data_prob /= age_data_prob.sum() # Ensure it sums to 1
    age_bins       = spu.n_multinomial(age_data_prob, pop_size) # Choose age bins
    ages           = age_data_min[age_bins] + age_data_range[age_bins]*np.random.random(pop_size) # Uniformly distribute within this age bin

    # Store output
    popdict = {}
    popdict["uid"] = uids
    popdict["age"] = ages
    popdict["sex"] = sexes

    # Actually create the contacts
    if   microstructure == "random":    contacts, layer_keys    = make_random_contacts(pop_size, sim["contacts"])
    elif microstructure == "clustered": contacts, layer_keys, _ = make_microstructured_contacts(pop_size, sim["contacts"])
    elif microstructure == "hybrid":    contacts, layer_keys, _ = make_hybrid_contacts(pop_size, ages, sim["contacts"])
    else: # pragma: no cover
        errormsg = f'Microstructure type "{microstructure}" not found; choices are random, clustered, or hybrid'
        raise NotImplementedError(errormsg)

    popdict["contacts"]   = contacts
    popdict["layer_keys"] = layer_keys

    return popdict


def make_random_contacts(pop_size, contacts, overshoot=1.2, dispersion=None):
    """Make random static contacts.

    Args:
        pop_size (int): number of agents to create contacts between (N)
        contacts (dict): a dictionary with one entry per layer describing the average number of contacts per person for that layer
        overshoot (float): to avoid needing to take multiple Poisson draws
        dispersion (float): if not None, use a negative binomial distribution with this dispersion parameter instead of Poisson to make the contacts

    Returns:
        contacts_list (list): a list of length N, where each entry is a dictionary by layer, and each dictionary entry is the UIDs of the agent's contacts
        layer_keys (list): a list of layer keys, which is the same as the keys of the input "contacts" dictionary
    
    New in version 1.10.0.

    """
    # Preprocessing
    pop_size = int(pop_size) # Number of people
    contacts = sc.dcp(contacts)
    layer_keys = list(contacts.keys())
    contacts_list = []

    # Precalculate contacts
    n_across_layers = np.sum(list(contacts.values()))
    n_all_contacts  = int(pop_size*n_across_layers*overshoot) # The overshoot is used so we won't run out of contacts if the Poisson draws happen to be higher than the expected value
    all_contacts    = spu.choose_r(max_n=pop_size, n=n_all_contacts) # Choose people at random
    p_counts = {}
    for lkey in layer_keys:
        if dispersion is None:
            p_count = spu.n_poisson(contacts[lkey], pop_size) # Draw the number of Poisson contacts for this person
        else:
            p_count = spu.n_neg_binomial(rate=contacts[lkey], dispersion=dispersion, n=pop_size) # Or, from a negative binomial
        p_counts[lkey] = np.array((p_count/2.0).round(), dtype=spu.default_int)

    # Make contacts
    count = 0
    for p in range(pop_size):
        contact_dict = {}
        for lkey in layer_keys:
            n_contacts = p_counts[lkey][p]
            contact_dict[lkey] = all_contacts[count:count+n_contacts] # Assign people
            count += n_contacts
        contacts_list.append(contact_dict)

    return contacts_list, layer_keys


def make_microstructured_contacts(pop_size, contacts):
    """Create microstructured contacts -- i.e. for households"""
    # Preprocessing -- same as above
    pop_size = int(pop_size) # Number of people
    contacts = sc.dcp(contacts)
    contacts.pop("c", None) # Remove community
    layer_keys = list(contacts.keys())
    contacts_list = [{c:[] for c in layer_keys} for p in range(pop_size)] # Pre-populate

    for layer_name, cluster_size in contacts.items():

        # Initialize
        cluster_dict = dict() # Add dictionary for this layer
        n_remaining = pop_size # Make clusters - each person belongs to one cluster
        contacts_dict = defaultdict(set) # Use defaultdict of sets for convenience while initializing. Could probably change this as part of performance optimization

        # Loop over the clusters
        cluster_id = -1
        while n_remaining > 0:
            cluster_id += 1 # Assign cluster id
            this_cluster =  spu.poisson(cluster_size)  # Sample the cluster size
            if this_cluster > n_remaining:
                this_cluster = n_remaining

            # Indices of people in this cluster
            cluster_indices = (pop_size-n_remaining)+np.arange(this_cluster)
            cluster_dict[cluster_id] = cluster_indices
            for i in cluster_indices: # Add symmetric pairwise contacts in each cluster
                for j in cluster_indices:
                    if j > i:
                        contacts_dict[i].add(j)

            n_remaining -= this_cluster

        for key in contacts_dict.keys():
            contacts_list[key][layer_name] = np.array(list(contacts_dict[key]), dtype=spu.default_int)

        clusters = {layer_name: cluster_dict}

    return contacts_list, layer_keys, clusters


def make_hybrid_contacts(pop_size, ages, contacts, school_ages=None, work_ages=None):
    """Create "hybrid" contacts -- microstructured contacts for households and
    random contacts for schools and workplaces, both of which have extremely
    basic age structure. A combination of both make_random_contacts() and
    make_microstructured_contacts().

    New in version 1.10.0.
    """
    # Handle inputs and defaults
    layer_keys = ["h", "s", "w", "c"]
    contacts = sc.mergedicts({"h":4, "s":20, "w":20, "c":20}, contacts) # Ensure essential keys are populated
    if school_ages is None:
        school_ages = [6, 22]
    if work_ages is None:
        work_ages   = [22, 65]

    # Create the empty contacts list -- a list of {'h':[], 's':[], 'w':[]}
    contacts_list = [{key:[] for key in layer_keys} for i in range(pop_size)]

    # Start with the household contacts for each person
    h_contacts, _, clusters = make_microstructured_contacts(pop_size, {"h":contacts["h"]})

    # Make community contacts
    c_contacts, _ = make_random_contacts(pop_size, {"c":contacts["c"]})

    # Get the indices of people in each age bin
    ages = np.array(ages)
    s_inds = sc.findinds((ages >= school_ages[0]) * (ages < school_ages[1]))
    w_inds = sc.findinds((ages >= work_ages[0])   * (ages < work_ages[1]))

    # Create the school and work contacts for each person
    s_contacts, _ = make_random_contacts(len(s_inds), {"s":contacts["s"]})
    w_contacts, _ = make_random_contacts(len(w_inds), {"w":contacts["w"]})

    # Construct the actual lists of contacts
    for i     in range(pop_size):   contacts_list[i]["h"]   =        h_contacts[i]["h"]  # Copy over household contacts -- present for everyone
    for i,ind in enumerate(s_inds): contacts_list[ind]["s"] = s_inds[s_contacts[i]["s"]] # Copy over school contacts
    for i,ind in enumerate(w_inds): contacts_list[ind]["w"] = w_inds[w_contacts[i]["w"]] # Copy over work contacts
    for i     in range(pop_size):   contacts_list[i]["c"]   =        c_contacts[i]["c"]  # Copy over community contacts -- present for everyone

    return contacts_list, layer_keys, clusters



def parse_synthpop(population, layer_mapping=None, community_contacts=0):
    """Make a population using SynthPops, including contacts. Usually called automatically,
    but can also be called manually. Either a simulation object or a population must
    be supplied; if a population is supplied, transform it into the correct format;
    otherwise, create the population and then transform it.

    Args:
        population (list): a pre-generated SynthPops population
        layer_mapping (dict): a custom mapping from SynthPops layers to Covasim layers
        community_contacts (int): create this many community contacts on average

    New in version 1.10.0.

    """
    # Handle layer mapping
    default_layer_mapping = {"H":"h", "S":"s", "W":"w", "C":"c", "LTCF":"l"} # Remap keys from old names to new names
    layer_mapping = sc.mergedicts(default_layer_mapping, layer_mapping)

    # Create the basic lists
    pop_size = len(population)
    uids, ages, sexes, contacts = [], [], [], []
    for uid,person in population.items():
        uids.append(uid)
        ages.append(person["age"])
        sexes.append(person["sex"])

    # Replace contact UIDs with ints
    uid_mapping = {uid:u for u,uid in enumerate(uids)}
    for uid in uids:
        iid = uid_mapping[uid] # Integer UID
        person = population.pop(uid)
        uid_contacts = sc.dcp(person["contacts"])
        int_contacts = {}
        for spkey in uid_contacts.keys():
            try:
                lkey = layer_mapping[spkey] # Map the SynthPops key into a Covasim layer key
            except KeyError: # pragma: no cover
                errormsg = f'Could not find key "{spkey}" in layer mapping "{layer_mapping}"'
                raise sc.KeyNotFoundError(errormsg)
            int_contacts[lkey] = []
            for cid in uid_contacts[spkey]: # Contact ID
                icid = uid_mapping[cid] # Integer contact ID
                if icid>iid: # Don't add duplicate contacts
                    int_contacts[lkey].append(icid)
            int_contacts[lkey] = np.array(int_contacts[lkey], dtype=spu.default_int)
        contacts.append(int_contacts)

    # Add community contacts
    c_contacts, _ = make_random_contacts(pop_size, {"c":community_contacts})
    for i in range(int(pop_size)):
        contacts[i]["c"] = c_contacts[i]["c"] # Copy over community contacts -- present for everyone

    # Finalize
    popdict = {}
    popdict["uid"]        = np.array(list(uid_mapping.values()), dtype=spu.default_int)
    popdict["age"]        = np.array(ages)
    popdict["sex"]        = np.array(sexes)
    popdict["contacts"]   = sc.dcp(contacts)
    popdict["layer_keys"] = list(layer_mapping.values())

    return popdict
