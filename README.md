### ShareSim system
## Install requirements
Python >= Python 3.10.2 <= 3.12
Microsoft Windows >= Windows10
Linux distributions eg. Ubuntu >= 20.04
Git >= 2.25.1

## HW min. requirements
> 1. CPU: 4 cores (1 simulated region per core)
> 2. RAM: 16GB (1GB per 10E5 of simulated agents)
> 3. HDD: 100GB and more (for system and logs)
> Connection to internet for downloading packages and updates

### Reccomended requirements
> 1. CPU: 64 cores
> 2. RAM: 256GB
> 3. HDD: 0.5TB and more
> Linux based operation system like Ubuntu od Debian
> Connection to internet for downloading packages and updates


## Install system
> Documentation available at <a href="https://github.com/kbi-fbmi/ABMShare_doc"> ABMShare documentation </a>

### Download Sharesim system or copy ShareSim folder
> Copy **ABMShare** folder from git repository or from USB drive to your computer.
> Copy **ShareSim** folder from **ABMShare directory** to another path *(Its main folder for running the simulation)*
### 1. Create virtual environment and activate it
> Create virtualEnvironment for python packages in main **ABMShare** folder. Install virtual env via pip: ```python3 -m venv .venv``` (Works same way for Windows and Linux) 
> Activate virtual environment. 
* For windows run in shell: ```.\<path_to_ABMShare_project>\.venv\Scripts\activate```. 
* For Linux run in shell: ```source <path_to_ABMShare_project>/.venv/bin/activate``` 
### 2. Install all requirements for Sharesim system
In activated virtual environment, in path of sharesim run: ```pip install -e .```
### 3. Edit few paths in ShareSim folder
> Edit paths in ```/<path_to_sharesim_project>/start.sh```  
> Especially Paths, which needs to be changes. (it is noted with description)
### Zeppelin analysis
> For running Zeppelin analysis, you need look into ```ABMShare/ShareSim/notebooks/Tutotial.md```