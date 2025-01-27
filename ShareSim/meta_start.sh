#!/bin/bash

# Activate virtual environment
source "/storage/ssd2/sharesim-app/.venv311/bin/activate"

# Get current timestamp
dt=$(date '+%d_%m_%Y_%H_%M')

# Set default configuration file path
DEFAULT_CONFIG="/home/$USER/sandbox/input_data/share_extension_configuration.json"

# Initialize variables
VALIDATION="false"  # default value for validation
CONFIG_FILE="$DEFAULT_CONFIG"  # default configuration file

# Parse command-line options
while getopts "c:v:" opt; do
  case $opt in
    c)
      CONFIG_FILE="$OPTARG"
      ;;
    v)
      if [[ "${OPTARG}" != "true" && "${OPTARG}" != "false" ]]; then
          echo "Invalid value for -v. Use 'true' or 'false'."
          exit 1
      fi
      VALIDATION="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# FILEPATH="/storage/ssd2/sharesim-app/extensions/abm_share_start.py"
FILEPATH="/storage/ssd2/sharesim-app/extensions/abm_share_start.py"


# Execute the Python script based on validation flag
if [ "$VALIDATION" == "true" ]; then
  /storage/ssd2/sharesim-app/.venv311/bin/python $FILEPATH -c $CONFIG_FILE -v $VALIDATION
else
  /storage/ssd2/sharesim-app/.venv311/bin/python $FILEPATH -c $CONFIG_FILE -g True -u $USER
fi

# Executing the script
# /storage/ssd2/sharesim-app/.venv311/bin/python $FILEPATH -c $CONFIG_FILE -g True -u $USER
#Validation of input files was successful
# Print the result
echo "Done!"