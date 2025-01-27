# Parameters for Synthetic population module

These parameters can be used in [Synthetic population settings](./Synthetic_pop_settings.md#settings-for-population-creator) in *key:pars* section. 
More information can be found at [IDM SynthPops](https://docs.idmod.org/projects/synthpops/).

Example parameters with default values:

- use_two_group_reduction=True
- average_LTCF_degree=20
- ltcf_staff_age_min=20
- ltcf_staff_age_max=60
- with_school_types=False
- school_mixing_type='random'
- average_class_size=20
- inter_grade_mixing=0.1
- average_student_teacher_ratio=20
- average_teacher_teacher_degree=3
- teacher_age_min=25
- teacher_age_max=75
- with_non_teaching_staff=False
- average_student_all_staff_ratio=15
- average_additional_staff_degree=20
- staff_age_min=20
- staff_age_max=75
- rand_seed=None
- country_location=None
- state_location=None
- location=None
- sheet_name=None
- household_method='infer_ages'
- smooth_ages=False
- window_length=7

# Parameters for Covasim variants

- name: "wild" #*default*
    - rel_beta        = 1.0, # Default values
    - rel_symp_prob   = 1.0, # Default values
    - rel_severe_prob = 1.0, # Default values
    - rel_crit_prob   = 1.0, # Default values
    - rel_death_prob  = 1.0, # Default values


- name: "alpha"
    - rel_beta        = 1.67, # Midpoint of the range reported in [https://science.sciencemag.org/content/372/6538/eabg3055](https://science.sciencemag.org/content/372/6538/eabg3055).
    - rel_symp_prob   = 1.0,  # Inconclusive evidence on the likelihood of symptom development. See [https://www.thelancet.com/journals/lanpub/article/PIIS2468-2667(21)00055-4/fulltext](https://www.thelancet.com/journals/lanpub/article/PIIS2468-2667(21)00055-4/fulltext).
    - rel_severe_prob = 1.64, # From [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3792894](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3792894), and consistent with [https://www.eurosurveillance.org/content/10.2807/1560-7917.ES.2021.26.16.2100348](https://www.eurosurveillance.org/content/10.2807/1560-7917.ES.2021.26.16.2100348) and [https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/961042/S1095_NERVTAG_update_note_on_B.1.1.7_severity_20210211.pdf](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/961042/S1095_NERVTAG_update_note_on_B.1.1.7_severity_20210211.pdf)
    - rel_crit_prob   = 1.0,  # Various studies have found increased mortality for B117 (summary here: [https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(21)00201-2/fulltext#tbl1](https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(21)00201-2/fulltext#tbl1)), but not necessarily when conditioned on having developed severe disease
    - rel_death_prob  = 1.0,  # See comment above

- name: "beta" 
    - rel_beta        = 1.0, # No increase in transmissibility; B1351's fitness advantage comes from the reduction in neutralisation
    - rel_symp_prob   = 1.0,
    - rel_severe_prob = 3.6, # From [https://www.eurosurveillance.org/content/10.2807/1560-7917.ES.2021.26.16.2100348](https://www.eurosurveillance.org/content/10.2807/1560-7917.ES.2021.26.16.2100348)
    - rel_crit_prob   = 1.0,
    - rel_death_prob  = 1.0,

- name: "gamma" 
    - rel_beta        = 2.05, # Estimated to be 1.7–2.4-fold more transmissible than wild-type: [https://science.sciencemag.org/content/early/2021/04/13/science.abh2644](https://science.sciencemag.org/content/early/2021/04/13/science.abh2644)
    - rel_symp_prob   = 1.0,
    - rel_severe_prob = 2.6, # From [https://www.eurosurveillance.org/content/10.2807/1560-7917.ES.2021.26.16.2100348](https://www.eurosurveillance.org/content/10.2807/1560-7917.ES.2021.26.16.2100348)
    - rel_crit_prob   = 1.0,
    - rel_death_prob  = 1.0,


- name: "delta"
    - rel_beta        = 2.2, # Estimated to be 1.25-1.6-fold more transmissible than B117: [https://www.researchsquare.com/article/rs-637724/v1](https://www.researchsquare.com/article/rs-637724/v1)
    - rel_symp_prob   = 1.0,
    - rel_severe_prob = 3.2, # 2x more transmissible than alpha from [https://mobile.twitter.com/dgurdasani1/status/1403293582279294983](https://mobile.twitter.com/dgurdasani1/status/1403293582279294983)
    - rel_crit_prob   = 1.0,
    - rel_death_prob  = 1.0,

# Parameters for simulation
All parameters are written as the key for use and possible values. All assigned values are representing default Covasim parameters. Some of those parameters are not implemented and tested yet - look for their description in each section. TO DO: What does this mean? Some parameters do not need to use, because they are already used by another module.

## Admissible parameters for global settings
- use_waning   = True **(bool)** - **(Optional)** Whether to use dynamically calculated immunity. **Must be enabled if there are vaccine intervention**
- unique_mobility_indexes = True **(bool)** As from the *V0.2.4* this must be enabled. Future fix coming.
- start_day = '2020-03-01' **str** - **(Optional)** Date from when the simulation is started. *Can be combined as start_day and n_days. Do not need to specify end_day.*
- n_days = 180 **int** - number of days for simulation

## Population parameters
- pop_size     = (int) e.g. 20000 or 20e3 - Number of agents, **Do not use when there is population object loaded**
- pop_infected = (int) 20 - Number of initial infections - **Can be used Globally or separately**
- pop_type     = 'random' - What type of population data to use -- 'random' (fastest), 'synthpops' (best), 'hybrid' (compromise) **Don not use when there is population object loaded**
- location     = None     - What location to load data from -- default Seattle **Do not use when there is population object loaded**

## Simulation parameters
- start_day  = '2020-03-01' - **(Optional)** Date from when is simulation started. *Can be combined as start_day and n_days. Do not need to specify end_day.*
- end_day    = None **(Datetime (YYYY-MM-DD))**- **(Optional)** End day of the simulation - can be used with `start_day`. *Does not need to be specified when there is start_day and n_days*
- n_days     = 60 **(int)** - Number of days to run, if `end_day` is not specified. *Simulation can only have n_days and starts with default date and ends after las day from n_days* 
- rand_seed  = 1 **(int)** - **(Optional)** Random seed, if None, do not reset *Simulation is using some random values, use rand_seed for different random seed*
- verbose    = cvo.verbose  - **(Optional)** Whether or not to display information during the run -- options are 0 (silent), 0.1 (some; default), 1 (default), 2 (everything). *It signifanctly slower simulation process*

## Rescaling parameters
Rescaling parameters do not need to be used. Some intervention have problem with rescaling (for example, contact tracing).

- pop_scale         = 1 **(int)** -**(Optional)** Factor by which to scale the population -- e.g. `pop_scale`=10 with `pop_size`=100e3 means a population of 1 million. **Cannot be used with interventions for contact tracing**
- scaled_pop        = None - The total scaled population, i.e. the number of agents times the scale factor **No need for use**
- rescale           = True **(bool)** - Enable dynamic rescaling of the population -- starts with `pop_scale`=1 and scales up dynamically as the epidemic grows. **Use the default, so no need to explicitly specify**
- rescale_threshold = 0.05 **(float)** - Fraction susceptible population that will trigger rescaling (if rescaling enabled)
- rescale_factor    = 1.2  **(float**- Factor by which the population is rescaled on each step
- frac_susceptible  = 1.0  **(float)**- What proportion of the population is susceptible to infection

## Network parameters, generally initialized after the population has been constructed
Because of synthetic pre-generated population there is no need to use Network parameters. For more info look for covasim original documentation.

- contacts        = None  - The number of contacts per layer; set by reset_layer_pars() below
- dynam_layer     = None  - Which layers are dynamic; set by reset_layer_pars() below
- beta_layer      = None  - Transmissibility per layer; set by reset_layer_pars() below

## Basic disease transmission parameters
- beta_dist    = dict(dist='neg_binomial', par1=1.0, par2=0.45, step=0.01)**(dict)**  - **(Optional)** Distribution to draw individual level transmissibility; dispersion from https://www.researchsquare.com/article/rs-29548/v1
- viral_dist   = dict(frac_time=0.3, load_ratio=2, high_cap=4) **(dict)** - **(Optional)** The time varying viral load (transmissibility); estimated from Lescure 2020, Lancet, https://doi.org/10.1016/S1473-3099(20)30200-0
- beta         = 0.016 **(float)**  - **(Optional)** Beta per symptomatic contact; absolute value, calibrated
- asymp_factor = 1.0  **(float)** - **(Optional)**  Multiply beta by this factor for asymptomatic cases; no statistically significant difference in transmissibility: https://www.sciencedirect.com/science/article/pii/S1201971220302502

## Parameters used to calculate immunity
Parameters defined as dict are not tested in current version. Its recommended to use only *use_waning, trans_redux, nab_boost* parameter from this section.  

- use_waning   = True **(bool)** - **(Optional)** Whether to use dynamically calculated immunity. **Must be enabled if there are vaccine intervention**
- nab_init     = dict(dist='normal', par1=0, par2=2) **  - **(Optional)** Parameters for the distribution of the initial level of log2(nab) following natural infection, taken from fig1b of https://doi.org/10.1101/2021.03.09.21252641
- nab_decay    = dict(form='nab_growth_decay', growth_time=21, decay_rate1=np.log(2) / 50, decay_time1=150, decay_rate2=np.log(2) / 250, decay_time2=365)**(dict)**  **(Optional)** 
- nab_kin      = None - **(Optional)**  Constructed during sim initialization using the nab_decay parameters
- nab_boost    = 1.5 - **(Optional)**  Multiplicative factor applied to a person's nab levels if they get reinfected. No data on this, assumption.
- nab_eff      = dict(alpha_inf=1.08, alpha_inf_diff=1.812, beta_inf=0.967, alpha_symp_inf=-0.739, beta_symp_inf=0.038, alpha_sev_symp=-0.014, beta_sev_symp=0.079)**(dict)**  - **(Optional)**  Parameters to map nabs to efficacy
- rel_imm_symp = dict(asymp=0.85, mild=1, severe=1.5)**(dict)**  -**(Optional)**  Relative immunity from natural infection varies by symptoms. Assumption.
- immunity     = None  - **(Optional)** Matrix of immunity and cross-immunity factors, set by init_immunity() in immunity.py
- trans_redux  = 0.59  - **(Optional)**  Reduction in transmission for breakthrough infections, https://www.medrxiv.org/content/10.1101/2021.07.13.21260393v

## Variant-specific disease transmission parameters.
When there are multiple variants from [T5.2 Simulation - Variants](./examples/exampleE5B.md) then there is no need to use those parameters.

- rel_beta        = 1.0 ## Relative transmissibility varies by variant

## Duration parameters: time for disease progression
> **Duration parameters are not implemented yet**

- dur['exp2inf  = dict(dist='lognormal_int', par1=4.5, par2=1.5) # Duration from exposed to infectious; see Lauer et al., https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7081172/, appendix table S2, subtracting - inf2sym duration
- dur['inf2sym  = dict(dist='lognormal_int', par1=1.1, par2=0.9) # Duration from infectious to symptomatic; see Linton et al., https://doi.org/10.3390/jcm9020538, from Table 2, 5.6 day incubation period - 4.5 day exp2inf from Lauer et al.
- dur['sym2sev  = dict(dist='lognormal_int', par1=6.6, par2=4.9) # Duration from symptomatic to severe symptoms; see Linton et al., https://doi.org/10.3390/jcm9020538, from Table 2, 6.6 day onset to hospital admission (deceased); see also Wang et al., https://jamanetwork.com/journals/jama/fullarticle/2761044, 7 days (Table 1)
- dur['sev2crit = dict(dist='lognormal_int', par1=1.5, par2=2.0) # Duration from severe symptoms to requiring ICU; average of 1.9 and 1.0; see Chen et al., https://www.sciencedirect.com/science/article/pii/S0163445320301195, 8.5 days total - 6.6 days sym2sev = 1.9 days; see also Wang et al., https://jamanetwork.com/journals/jama/fullarticle/2761044, Table 3, 1 day, IQR 0-3 days; std=2.0 is an estimate

## Duration parameters: time for disease recovery
> **Duration parameters are not implemented yet**

- dur['asym2rec = dict(dist='lognormal_int', par1=8.0,  par2=2.0) # Duration for asymptomatic people to recover; see Wölfel et al., https://www.nature.com/articles/s41586-020-2196-x
- dur['mild2rec = dict(dist='lognormal_int', par1=8.0,  par2=2.0) # Duration for people with mild symptoms to recover; see Wölfel et al., https://www.nature.com/articles/s41586-020-2196-x
- dur['sev2rec  = dict(dist='lognormal_int', par1=18.1, par2=6.3) # Duration for people with severe symptoms to recover, 24.7 days total; see Verity et al., https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(20)30243-7/fulltext; 18.1 days = 24.7 onset-to-recovery - 6.6 sym2sev; 6.3 = 0.35 coefficient of variation * 18.1; see also https://doi.org/10.1017/S0950268820001259 (22 days) and https://doi.org/10.3390/ijerph17207560 (3-10 days)
- dur['crit2rec = dict(dist='lognormal_int', par1=18.1, par2=6.3) # Duration for people with critical symptoms to recover; as above (Verity et al.)
- dur['crit2die = dict(dist='lognormal_int', par1=10.7, par2=4.8) # Duration from critical symptoms to death, 18.8 days total; see Verity et al., https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(20)30243-7/fulltext; 10.7 = 18.8 onset-to-death - 6.6 sym2sev - 1.5 sev2crit; 4.8 = 0.45 coefficient of variation * 10.7

## Severity parameters: probabilities of symptom progression
- rel_symp_prob   = 1.0  **(float)** - **(Optional)** Scale factor for proportion of symptomatic cases
- rel_severe_prob = 1.0  **(float)** - **(Optional)** Scale factor for proportion of symptomatic cases that become severe
- rel_crit_prob   = 1.0  **(float)** - **(Optional)** Scale factor for proportion of severe cases that become critical
- rel_death_prob  = 1.0  **(float)** - **(Optional)** Scale factor for proportion of critical cases that result in death
- prog_by_age     = prog_by_age *or* False **(str/bool)** - Whether to set or not disease progression based on the person's age.
- prognoses       = None **(float)** - **(Optional)** The actual arrays of prognoses by age; this is populated later

## Efficacy of protection measures
- iso_factor   = None **(float)** - **(Optional)** Multiply beta by this factor for diagnosed cases to represent isolation
- quar_factor  = None **(float)** - **(Optional)** Quarantine multiplier on transmissibility and susceptibility
- quar_period  = 14  **(int)** - **(Optional)** Number of days to quarantine for; assumption based on standard policies

# Intervention parameters
## Parameters for mobility intervention
- location_code **(str)** = location code of region
- use **(bool)** = True # Default value for use is **True**. If you want to disable this intervention, set it to **False**
- intervention_type **(str)** = "mobility_change" # Default value for type is **mobility_change**.  iNo other value allowed.
- label **(str)** = "Some label" # **Optional** Label for this mobility change eg. "Region1 lockdown"
- start_day **(str in YYYY-MM-DD)/ int as number of day** = "2021-03-16"/ 16 Specifies day of the intervention start
- end_day **(str in YYYY-MM-DD)int as number of day** = "2021-03-16"/ 16 Specifies day of the intervention end
- num_days **(int/list of ints)** = can be specified for starting/ending day. Usage as list or integer: [10,25] or 10

## Parameters for changing beta intervention
- location_code **(str)** = location code of region
- use **(bool)** = True # Default value for use is **True**. If you want to disable this intervention, set it to **False**
- intervention_type **(str)** = "beta_change" # Default value for type is **beta_change**. No other value allowed.
- label **(str)** = "Some label" # **Optional**Label for this mobility change eg. "School lockdown"
- start_day **(str in YYYY-MM-DD)** = "2021-03-16" # Specifies day of the intervention start
- end_day **(str in YYYY-MM-DD)** = "2021-03-16" # Specifies day of the intervention end
- num_days **(int/list of ints)** = can be specified for starting/ending day. Usage as list or integer: [10,25] or 10 `"days":[1,30]` - which will set starting day as 1st day of simulation and it will end the 30th day of simulation. Or can be used as start day only `"days":10` - intervention will start the 10th day of simulation.
- beta_change **(float/float list)** = change overall beta (transmission) parameter. Can be used as single value `"beta_change":0.6` and after intervention ends it will go back to 1.0. Or can be used as list `"beta_change":[0.6,0.8]` and after intervention ends the value will be se to 0.8
- layers **list of str** = change can be applied to one or more layers. You can use it only for school `"layers":['s']` or for more layers e.g. workplaces `"layers":['s','w']`

## Parameters for contact isolation
- location_code **(str)** = location code of region
- use **(bool)** = True # Default value for use is **True**. If you want to disable this intervention, set it to **False**
- intervention_type **(str)** = "isolate_contacts" # Default value for type is **isolate_contacts**. No other value allowed.
- label **(str)** = "Some label"  **Optional** # Label for this mobility change eg. "School contact isolation"
- num_days **(int/list of ints)** = can be specified for starting/ending day. Usage as list or integer: [10,25] or 10`"days":"[1,30]"` - which will set starting day as 1st day of simulation and it will end the 30th day of simulation. Or can be used as start day only `"days":10` - intervention will start the 10th day of simulation.
- changes **(float/float list)** = change overall contacts by given number (0.3 == - 30% of contacts). Can be used as single value `"changes":0.6` and after intervention ends it will go back to 1.0. Or can be used as list `"changes":"[0.6,0.8]"` and after intervention ends the value will be se to 0.8
- layers **list of str** = change can be applied to one or more layers. You can use it only for school `"layers":"['s']"` or for more layers e.g. workplaces `"layers":"['s','w']" `
- start_day **(str in YYYY-MM-DD)** = "2021-03-16" # Specifies day of the intervention start
- end_day **(str in YYYY-MM-DD)** = "2021-03-16" # Specifies day of the intervention end

## Parameters for daily testing
> There is a plenty of key:values which are optional. Basically its necessary to define daily_test and type of intervention. Everything else is optional and be loaded as default parameters, if none provided. (Default parameters are written on every key = default_value). **Note: do not use dict value specific keys, this is not tested yet e.g. *key:subtarget***

- location_code **(str)** = location code of region
- use **(bool)** = True # Default value for use is **True**. If you want to disable this intervention, set it to **False**
- intervention_type **(str)** = "per_day_testing" # Default value for type is **per_day_testing**. No other value allowed.
- label **(str)** = "Some label"  **Optional** # Label for this mobility change eg. "School contact isolation"
- daily_tests **(int/int list)**  = number of tests per day, can be int, array, or dataframe/series; if integer, use - that number every day
- symp_test   **(float)** = 100.0 **Optional**odds ratio of a symptomatic person testing (default: 100x more likely)
- quar_test   **(float)**= 1.0 **Optional**probability of a person in quarantine testing (default: no more likely)
- quar_policy **(str)**  = None **Optional**policy for testing in quarantine: options are 'start' (default), 'end', 'both' (start and end), 'daily'; can also be a number or a function, see get_quar_inds()
- subtarget   **(dict)** = None **Optional**subtarget intervention to people with particular indices (format: {'ind': array of indices, or function to return indices from the sim, 'vals': value(s) to apply} **NOT IMPLEMENTED YET**
- ili_prev    **(arr)**  = None **Optional**prevalence of influenza-like-illness symptoms in the population; can be float, array, or dataframe/series
- sensitivity **(float)**= 1.0 **Optional**test sensitivity (default 100%, i.e. no false negatives)
- loss_prob   **(float)**= 0 **Optional**probability of the person being lost-to-follow-up (default 0%, i.e. no one lost to follow-up)
- test_delay  **(int)**  = 0 **Optional**days for test result to be known (default 0, i.e. results available instantly)
- start_day   **(int)**  = 0 **Optional**day the intervention starts (default: 0, i.e. first day of the simulation)
- end_day     **(int)**  = None **Optional**day the intervention ends
- num_days **(int/list of ints)** = can be specified for starting/ending day. Usage as list or integer: [10,25] or 10

## Parameters for testing probability
There is a plenty of `key:values` which are optional. Basically its necessary to define `daily_test` and type of intervention. Everything else is optional and be loaded as default parameters, if none provided. (Default parameters are written on every key = default_value). **Note: do not use dict value specific keys, this is not tested yet e.g. *key:subtarget* **

- location_code **(str)** = location code of region
- use **(bool)** = True # Default value for use is **True**. If you want to disable this intervention, set it to **False**
- intervention_type **(str)**= "testing_probability" # Default value for type is **testing_probability**. No other value allowed.
- label **(str)** = "Some label"  **Optional** # Label for this mobility change eg. "School contact isolation"
- symp_prob        **(float)**    = 0.1 probability of testing a symptomatic (unquarantined) person
- asymp_prob       **(float)**    = 0.0 **Optional** probability of testing an asymptomatic (unquarantined) person (default: 0)
- symp_quar_prob   **(float)**    = None **Optional** probability of testing a symptomatic quarantined person (default: same as `symp_prob`)
- asymp_quar_prob  **(float)**    = None **Optional** probability of testing an asymptomatic quarantined person (default: same as `asymp_prob`)
- quar_policy      **(str)**      = None **Optional** policy for testing in quarantine: options are 'start' (default), 'end', 'both' (start and end), 'daily'; can also be a number or a function, see get_quar_inds()
- subtarget        **(dict)**     = None **Optional** subtarget intervention to people with particular indices  (see test_num() for details) **NOT IMPLEMENTED YET**
- ili_prev         **(float/float list)** = None **Optional** prevalence of influenza-like-illness symptoms in the population; can be float, array, or dataframe/series
- sensitivity      **(float)**    = 1.0 **Optional** test sensitivity (default 100%, i.e. no false negatives)
- loss_prob        **(float)**    = 0.0 **Optional** probability of the person being lost-to-follow-up (default 0%, i.e. no one lost to follow-up)
- test_delay       **(int)**      = 0 **Optional** days for test result to be known (default 0, i.e. results available instantly)
- start_day        **(int)**      = 0 **Optional** day the intervention starts (default: 0, i.e. first day of the simulation)
- end_day          **(int)**      = None **Optional** day the intervention ends (default: no end)
- num_days **(int/list of ints)** = can be specified for starting/ending day. Usage as list or integer: [10,25] or 10

## Parameters for contact tracing
There is a plenty of `key:values` which are optional. Basically it is necessary to define `daily_test` and type of intervention. Everything else is optional and be loaded as default parameters, if none provided. (Default parameters are written on every key = default_value). **Note: do not use dict value specific keys, this is not tested yet e.g. *keys: trace_probs and trace_time otherwise use them only as single float value* **

- location_code **(str)** = location code of region
- use **(bool)** = True # Default value for use is **True**. If you want to disable this intervention, set it to **False**
- intervention_type **(str)*** = "contact_tracing" # Default value for type is **contact_tracing**. No other value allowed.
- label **(str)** = "Some label"  **Optional** # Label for this mobility change eg. "School contact isolation"
- trace_probs **(float/dict)**=0.4 **Optional** probability of tracing, per layer (default=100%, i.e. everyone is traced) **NOT IMPLEMENTED YET**
- trace_time  **(float/dict)**=0 **Optional** days required to trace, per layer (default=0, i.e. no delay) **NOT IMPLEMENTED YET**
- start_day   **(int)**=0       **Optional** intervention start day (default=0, i.e. the start of the simulation)
- end_day     **(int)**=None       **Optional** intervention end day (default=no end)
- presumptive **(bool)**=false      **Optional** whether or not to begin isolation and contact tracing on the presumption of a positive diagnosis (default=no)
- capacity    **(int)**=None       **Optional** optionally specify a maximum number of newly diagnosed people to trace each day
- quar_period **(int)**=None       **Optional** number of days to quarantine when notified as a known contact.
- num_days **(int/list of ints)** = can be specified for starting/ending day. Usage as list or integer: [10,25] or 10

## Parameters for simple vaccination
There are a few keys to define this intervention. Use waning immunity must be enabled.

- location_code **(str)** = location code of region
- use **(bool)** = True # Default value for use is **True**. If you want to disable this intervention, set it to **False**
- intervention_type **(str)** = "simple_vaccination" # Default value for type is **vaccine**. No other value allowed.
- label **(str)** = "Some label"  **Optional** # Label for this mobility change eg. "School contact isolation"
- start_day **(int)** = 0       **Optional** intervention start day (default=0, i.e. the start of the simulation)
- end_day **(int)** = None       **Optional** intervention end day (default=no end)
- num_days **(int/list of ints)** = can be specified for starting/ending day. Usage as list or integer: [10,25] or 10
- prob **(float)** = 0.0       **Optional** probability of being vaccinated each day (default=0, i.e. no one is vaccinated)
- rel_sus **(float)** = 0.0       **Optional** relative susceptibility of vaccinated people (0 = perfect, 1 = no effect)
- rel_symp **(float)** = 0.0       **Optional** relative symptomaticity of vaccinated people (0 = perfect, 1 = no effect)
- cumulative **(bool)** = False       **Optional** whether cumulative doses have cumulative effects (default false);


