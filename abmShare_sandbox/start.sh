#!/bin/bash

unset VALIDATION

while getopts "v:p:c:s:" flag
do
    case "${flag}" in
        v) 
            if [[ "${OPTARG}" == "true" ]]; then
                VALIDATION=true
            elif [[ "${OPTARG}" == "false" ]]; then
                VALIDATION=false
            else
                echo "Invalid value for -v. Use 'true' or 'false'."
                exit 1
            fi
            ;;
        p)
            parent_dir=${OPTARG}        
            ;;
        c)
            mainconfig=${OPTARG}            
            ;;
        s)
            script_path=${OPTARG}
            ;;
        *) 
            echo "Usage: scriptname [-v true|false] [-p parent_dir] [-c mainconfig] [-s execution_script_path]"
            exit 1
            ;;
    esac
done

# Get the directory of the parrent_dir, defaultly
if [ -z "$parent_dir" ]; then
    parent_dir=$(dirname "$(dirname "$(readlink -f "$0")")")
fi

# Path to virtual environment
source "$parent_dir/.venv/bin/activate" # Specify the full path, or let it based on the original structure
# Chunk of code for getting timestamp
dt=$(date '+%d_%m_%Y_%H_%M')
# Filepath for python starting script
if [ -z "$script_path" ]; then
    script_path="$parent_dir/abmshare/abm_share_start.py"
fi
# Filepath for main configuration file
if [ -z "$mainconfig" ]; then
    mainconfig="$parent_dir/abmShare_sandbox/input_data/main_configuration.json"
fi
# Needed process
name="$parent_dir/abmShare_sandbox/nohup${dt}.out"

# Check the state of VALIDATION and act accordingly
if [ "${VALIDATION}" == "true" ]; then
    nohup python3 $script_path -c $mainconfig -v $validation &> $name &
elif [ "${VALIDATION}" == "false" ]; then # If v_flag is not set, call the Python script with False 
    nohup python3 $script_path -c $mainconfig -v $validation &> $name &
else
    nohup python3 $script_path -c $mainconfig &> $name &
fi
tail -f "nohup${dt}.out"