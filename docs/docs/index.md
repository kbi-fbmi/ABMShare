# Welcome to abmSHARE documentation
abmSHARE is an agent-based (also called individual-based or microsimulation) epidemiological spatial model adapted to SHARE and Eurostat data.

**The abmSHARE model is restricted for internal use in the Horizon SHARE-COVID19 project.**


## What is abmSHARE? 

The abmSHARE model is built on Covasim (COVID-19 Agent-based Simulator), an open-source agent-based model developed by the [Institute for Disease Modeling](https://idmod.org/) available at [https://github.com/InstituteforDiseaseModeling/covasim](https://github.com/InstituteforDiseaseModeling/covasim), and build with related SynthPops, an open-source synthetic population constructor developed also by [Institute for Disease Modeling](https://idmod.org/) available at [https://github.com/InstituteforDiseaseModeling/synthpops](https://github.com/InstituteforDiseaseModeling/synthpops). 

The model is written in python and can be adapted by users to suit their research questions and local context by specifying detailed data on population (age structure, mobility, contacts) and the epidemic (diagnosed cases, hospitalization, deaths). As in the original Covasim model, abmSHARE cab be used to explore theoretical research questions or to make projections, its main purpose is to evaluate the effect of different interventions on the epidemic. These interventions include physical interventions (mobility restrictions and masks), diagnostic interventions (testing, contact tracing, and quarantine), and pharmaceutical interventions (vaccination). 

abmSHARE extends the original Covasim model in two important dimensions: it allows epidemiological simulations across geographic regions (countries, NUTS) and is able to input external data as parameters for characterizing these regions in terms of their population, policies, or socio-economic conditions, for example. The abmSHARE includes all information of the Covasim model in region-specific geospatial environment on age structure and population size in each region; realistic transmission networks in different social layers, including households, schools, or workplaces; age-specific epidemiological outcomes; and viral dynamics and transmissibility. The abmSHARE model allows for region-specific policy interventions such as non-pharmaceutical interventions (physical distancing, lockdowns), vaccinations, testing, contact tracing and quarantine, all with detailed time structure and other factors. 

## How to become a user? 

The abmSHARE model has been built for the Horizon SHARE-Covid19 project. To become a user, please contact the administrators of the project for access and support at radim.bohacek@gmail.com.
