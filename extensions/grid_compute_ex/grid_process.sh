#!/bin/bash


while getopts "f:i:u:s:o:q:a:" opt; do
  case $opt in
    f)
      FUNCTION="$OPTARG" #Script to call
      ;;
    i)
      LOCALFOLDER="$OPTARG" #Datadir for input folder
      ;;
    u)
      USERNAME="$OPTARG" #Username for remote
      ;;
    s)
      SERVERNAME="$OPTARG" #Servername for remote
      ;;
    o)
      REMOTEFOLDER="$OPTARG" #Datadir for input on remote
      ;;
    q)
      QSUBSTRING="$OPTARG" #Datadir for input on remote
      ;;
    a)
      APPENDSTRING="$OPTARG" #Datadir for input on remote
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

# Check credentials function
check_credentials(){
current_datetime=$(date -u +"%s") # Convert current datetime to Unix timestamp
klist_output=$(klist) # Get output of klist directly into a variable
# Read the output line by line
while read -r line; do
    if [[ $line =~ ^[0-9]{2}\/[0-9]{2}\/[0-9]{2} ]]; then
        expires_column=$(echo "$line" | awk '{print $2 " " $3}')
        expires_timestamp=$(date -u -d "$expires_column" +"%s") # Convert expires datetime to Unix timestamp

        if [[ "$expires_timestamp" -lt "$current_datetime" ]]; then
            echo "You cannot send a request to Metacentrum, because token is expired. Max valid until: $expires_column\
             Contact the administrator to register a new token."
             exit 0
        else
            exit 1 # if its valid = 1 for true
        fi
    fi
done <<< "$klist_output"  # Use variable instead of file
}

# Remote server sender for directories
scp_copy_to_remote(){
    scp -q -r $LOCALFOLDER $USERNAME@$SERVERNAME:$REMOTEFOLDER
}

send_qsub_to_remote() {
    local qsubString=$QSUBSTRING # Check for right format
    ssh -q $USERNAME@$SERVERNAME << EOF
        $qsubString
EOF
}

append_to_queue(){
    directory="/home/user/download_scripts"
    python "${directory}/download_script.py" ${APPENDSTRING}
}

case "$FUNCTION" in
    "check_credentials")
        check_credentials
        ;;
    "scp_copy_to_remote")
        scp_copy_to_remote
        ;;
    "send_qsub_to_remote")
        send_qsub_to_remote
        ;;
    "append_to_queue")
        append_to_queue
        ;;
    *)
        echo "Invalid script name"
        exit 1
        ;;
esac