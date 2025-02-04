#!/bin/bash

while getopts "f:u:c:d:" opt; do
  case $opt in
    f)
      FOLDERNAME="$OPTARG" #Datadir for input folder
      ;;
    u)
      USERNAME="$OPTARG" #Username 
      ;;
    c)
      CONFIGNAME="$OPTARG" #Name of configuration file
      ;;
    d)
      DEBUGGING="$OPTARG" #Debugging mode
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

export PATH=/storage/projects/cvut_fbmi_kbi/share-covasim/.venv310/bin:${PATH}
source /storage/projects/cvut_fbmi_kbi/share-covasim/.venv310/bin/activate
echo "\n"
which python
echo "\n"
# Script path
script=/storage/projects/cvut_fbmi_kbi/share-covasim/extensions/abm_share_start.py
# Paths to copy
INPUTDIR=/storage/projects/cvut_fbmi_kbi/ABM_share/inputs/$USERNAME/$FOLDERNAME
OUTPUTDIR=/storage/projects/cvut_fbmi_kbi/ABM_share/outputs/$USERNAME/$FOLDERNAME


trap 'clean_scratch' TERM EXIT


cp -r $INPUTDIR $SCRATCHDIR/ABM_share_meta
cd $SCRATCHDIR

# Main config path
default_config_path=$SCRATCHDIR/ABM_share_meta/input_data/share_extension_configuration.json
if [ -z "$CONFIGNAME" ]
then
    mainconfig=$SCRATCHDIR/ABM_share_meta/input_data/$CONFIGNAME # Check in future
else
    mainconfig=$default_config_path
fi
# Settings for debugging
# if [ -z "$DEBUGGING" ]
# then
#     mainconfig=$SCRATCHDIR/ABM_share_meta/Simulation/input_data/original_confs/share_extension_configuration.json
# fi

ls -R | grep ":$" | sed -e 's/:$//' -e 's/[^-][^\/]*\//--/g' -e 's/^/   /' -e 's/-/|/'

# Edit paths in the config files
cd $SCRATCHDIR/ABM_share_meta
python /storage/projects/cvut_fbmi_kbi/share-covasim/extensions/grid_compute_ex/grid_change_paths.py

python $script -c $mainconfig -g False -u $USERNAME -v false

# # Copy results back to the project directory
mkdir -pv $OUTPUTDIR && cp -rf $SCRATCHDIR/ABM_share_meta/* $OUTPUTDIR

echo $PWD
echo $SCRATCHDIR