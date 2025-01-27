#!/bin/bash

unset VALIDATION

while getopts "v:" flag
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
        *) 
            echo "Usage: scriptname [-v true|false]"
            exit 1
            ;;
    esac
done

# Get the directory of the current script and go two directories back
parent_dir=$(dirname "$(dirname "$(readlink -f "$0")")")

# Path to virtual environment
source "$parent_dir/.venv/bin/activate" # Specify the full path, or let it based on the original structure
# Chunk of code for getting timestamp
dt=$(date '+%d_%m_%Y_%H_%M')
# Filepath for python starting script
filepath="$parent_dir/extensions/abm_share_start.py"
# Filepath for main configuration file
mainconfig="$parent_dir/ShareSim/input_data/main_configuration.json"
# Needed process
name="$parent_dir/ShareSim/nohup${dt}.out"

# Check the state of VALIDATION and act accordingly
if [ "${VALIDATION}" == "true" ]; then
    nohup python3 $filepath -c $mainconfig -v $validation &> $name &
elif [ "${VALIDATION}" == "false" ]; then # If v_flag is not set, call the Python script with False 
    nohup python3 $filepath -c $mainconfig -v $validation &> $name &
else
    nohup python3 $filepath -c $mainconfig &> $name &
fi
tail -f "nohup${dt}.out"