#!/usr/bin/env bash

HOST_IP=$(hostname -I | grep -o -E "((([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])))")
HITLIST="/root/git/scripts/text-files/short_hitlist.txt"
HITLIST_LENGTH=$(wc -l < $HITLIST) # get the number of lines in file
N_ITERATIONS=1
TAR_DIR="/root/tarballs"
#echo "$HITLIST_LENGTH"
#N=1
#let M=$N+9

create_tarball()
{
    cd $TAR_DIR
    echo "Creating tarball..."
    local l_DATE=$(date '+%d-%m-%y-%H-%M-%S')
    local l_TAR_FILENAME="tar-$HOSTNAME-${l_DATE}.tar.gz"
    tar -czvf ${l_TAR_FILENAME} -C /root/logs/$HOSTNAME/ .
    echo "Tarball saved to $TAR_DIR/$l_TAR_FILENAME. Cleaning up the /root/logs/$HOSTNAME/-directory..."
    rm /root/logs/$HOSTNAME/*
    echo "Transferring tarball to remote host"
    scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i /root/.ssh/scp-key $TAR_DIR/$l_TAR_FILENAME 209.97.138.74:/root/archived-logs/$l_TAR_FILENAME
    if [ $? -eq 0 ];
    then
        echo "Transfer completed successfully. Deleting tarball..."
        rm $TAR_DIR/$l_TAR_FILENAME 
        echo "Tarball deleted"
        echo "Cleaning up raw data..."
        rm /root/raw/*
    else
        echo "Transfer to remote host failed"
    fi
}

pt_run()
{
    local l_DESTINATION_ADDR="$1"
    local l_DESTINATION_PORT="$2"
    local l_FLOW_LABEL="$3"
    local l_HASH=$(echo -n ${l_DESTINATION_ADDR} | md5sum | awk '{print $1}')
    local l_SHORT="${l_HASH:0:6}"
    local l_DATE=$(date '+%d-%H-%M-%S')
    local l_FILEPATH="/root/raw/"
    local l_FILENAME="$HOSTNAME-${l_SHORT}-${l_DATE}.txt"

    echo "Starting paris-traceroute"
    sudo paris-traceroute -T -p ${l_DESTINATION_PORT} "${l_FLOW_LABEL}" "${l_DESTINATION_ADDR}" > $l_FILEPATH$l_FILENAME
    echo "paris-traceroute finished. Output saved in $l_FILENAME."
    echo "Converting to JSON..."
    python3 /root/git/scripts/python-scripts/text-to-json-2.py $l_FILEPATH$l_FILENAME $HOSTNAME ${l_DESTINATION_PORT} ${HOST_IP} ${l_FLOW_LABEL}
}

# Explanation: 
# In stage 2, the flow label will be constant (0).
# The goal is to figure out if we can get a path to change by changing the port number

# port definitions
TRACEROUTE_DEFAULT_PORT=33434
HTTP_PORT=80
HTTPS_PORT=443
SSH_PORT=22

# flow-label definitions
FLOW_LABEL_MIN=0
FLOW_LABEL_LOW_1=1
FLOW_LABEL_LOW_2=2
FLOW_LABEL_LOW_3=10
FLOW_LABEL_MID_1=277
FLOW_LABEL_MID_2=131071
FLOW_LABEL_HIGH_1=1048574
FLOW_LABEL_MAX=1048575

#flow_labels=($FLOW_LABEL_MIN)
FLOW_LABELS=($FLOW_LABEL_LOW_1)
#flow_labels=($FLOW_LABEL_MIN $FLOW_LABEL_MID_1 $FLOW_LABEL_MID_2 $FLOW_LABEL_MAX)

DESTINATION_PORTS=($TRACEROUTE_DEFAULT_PORT) # get destination tcp-port from input args
#DESTINATION_PORTS=($TRACEROUTE_DEFAULT_PORT $SSH_PORT $HTTP_PORT $HTTPS_PORT) # get destination tcp-port from input args

# ITERATIONS=$1 # the number of iterations that you wish to run the script. from input args

host_ip=$(hostname -I | grep -o -E "((([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])))")

for i in $(seq 1 $N_ITERATIONS); do
    for DESTINATION_PORT in "${DESTINATION_PORTS[@]}"; do
        for FLOW_LABEL in "${FLOW_LABELS[@]}"; do
            N=1
            let M=$N+9
            while [ $N -lt $HITLIST_LENGTH ]; do
                readarray -t my_array < <(sed -n "${N},${M}p" $HITLIST)
                    for ADDRESS in ${my_array[@]}; do
                        #pt_run "$ELEMENT" &
                        pt_run "$ADDRESS" "$DESTINATION_PORT" "$FLOW_LABEL" &
                    done
                let N=$N+10
                let M=$N+9
                wait
            done
        done
    done
    wait
    create_tarball
done

echo "All done!"
