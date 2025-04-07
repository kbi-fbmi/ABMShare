### ABMShare system
> Created by [DNAi s.r.o](https://www.dnai.ai/) maintained by [FBME CTU ](https://www.fbmi.cvut.cz/en)

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

### Download ABMShare system or copy ShareSim folder
> Clone a ABMShare project on [Link](https://github.com/kbi-fbmi/ABMShare) <br>

#### 1.A Install within Pip package manager
> Create virtualEnvironment for python packages in main **ABMShare** folder. Install virtual env via pip: ```python3 -m venv .venv``` (Works same way for Windows and Linux) 
> Activate virtual environment. 
* For windows run in shell: ```.\<path_to_ABMShare_project>\.venv\Scripts\activate```. 
* For Linux run in shell: ```source <path_to_ABMShare_project>/.venv/bin/activate``` 

>In activated virtual environment, in path of sharesim run: ```pip install -e .```

#### 1.B Install within uv package manager
> First install uv - follow this [Link](https://docs.astral.sh/uv/getting-started/installation/)
> Create virtual environment ```uv venv```
> Install all dependencies using ```uv sync```, if you want to use development version, then also run ```uv pip install -e <path_to_the_project / or use ".">```

### 3. Edit few paths in ShareSim folder
> Edit configuration files paths in "abmShare_sandbox folder". You can also run python code to edit paths - if you want to replace current/different patterns. It looks across all csv/xlsx json/yaml files and replace paths.
```python
    from abmshare.change_paths import RecursiveChangePaths
    pattern_to_replace="<Path_to_sandbox>" #Pattern of your choice
    replacement_pattern="/path/you/want/to/replace"
    dir_path="/path/to/your/sandbox/input_files"
    RecursiveChangePaths(directory=dir_path,pattern=pattern_to_replace,replacement=replacement_pattern)
```
#### 3.A For locall run 
> run start.sh with possible arguments for:``` -c <path_to_main_configuration_file> -s <path_to_abmshare.abm_share_start.py>```
> run ```python abm_share_start.py``` with corresponding args
> run your own python script with import like:
```python
import abmshare.extension_controller as exct
configuration_path="path/to/main/configuration/file"
exct.ExtensionController(configuration=configuration_path) #args.config
```
### Run with the Google colab
> Check this [Link](https://drive.google.com/drive/folders/1LzP4MUeqz9upJU3DdFkVAYIooW0rwiM5?usp=drive_link)
> And look for ABMShare_run.ipynb notebook, Also you can run this with ipykernel.

