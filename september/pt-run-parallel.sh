#!/usr/bin/env bash

# port definitions
TRACEROUTE_DEFAULT_PORT=33434
HTTP_PORT=80
HTTPS_PORT=443
SSH_PORT=22
DNS_PORT=53

# flow-label definitions
FLOW_LABEL_MIN=0
FLOW_LABEL_LOW_1=1
FLOW_LABEL_LOW_2=2
FLOW_LABEL_LOW_3=10
FLOW_LABEL_MID_1=277
FLOW_LABEL_MID_2=131071
FLOW_LABEL_HIGH_1=1048574
FLOW_LABEL_MAX=1048575

# default values
FLOW_LABELS=($FLOW_LABEL_MIN $FLOW_LABEL_LOW_3 $FLOW_LABEL_MID_2 $FLOW_LABEL_MAX)
DESTINATION_PORTS=($TRACEROUTE_DEFAULT_PORT)
HITLIST="/root/git/scripts/text-files/short_hitlist.txt"

# Use large or small hitlist
FULL_HITLIST=false

# Experiment stages
STAGE1=true
STAGE2=false
STAGE3=false

if [ "$STAGE1" = true ]; then
    # Stage 1
    # The goal of stage 1 is to figure out if the flow-label is maintained across all hops to a destination
    FLOW_LABELS=($FLOW_LABEL_MIN $FLOW_LABEL_LOW_3 $FLOW_LABEL_MID_2 $FLOW_LABEL_MAX)
    DESTINATION_PORTS=($TRACEROUTE_DEFAULT_PORT)
elif [ "$STAGE2" = true ]; then
    # Stage 2
    # In stage 2, the flow label will be constant (0).
    # The goal is to figure out if we can get a change in path by changing the port number
    FLOW_LABELS=($FLOW_LABEL_MIN)
    DESTINATION_PORTS=($TRACEROUTE_DEFAULT_PORT $SSH_PORT $HTTP_PORT $HTTPS_PORT $DNS_PORT) # get destination tcp-port from input args
elif [ "$STAGE3" = true ]; then
    # Stage 3
    # The goal of this step is to delve into the cases from stage 2
    # We want to know if we get the same path if we use a different port-number. Mix of well-known ports
    FLOW_LABELS=($FLOW_LABEL_LOW_1 $FLOW_LABEL_LOW_1 $FLOW_LABEL_LOW_1 $FLOW_LABEL_LOW_1) # Do the experiment 4 times
    #FLOW_LABELS=($FLOW_LABEL_LOW_1 $FLOW_LABEL_LOW_3 $FLOW_LABEL_MID_2 $FLOW_LABEL_MAX)
    DESTINATION_PORTS=($TRACEROUTE_DEFAULT_PORT $SSH_PORT $HTTP_PORT $HTTPS_PORT) # get destination tcp-port from input args
fi

if [ "$FULL_HITLIST" = true ]; then
    # Short hitlist (20 lines)
    #HITLIST="/root/git/scripts/text-files/short_hitlist.txt"

    # Long hitlist (15757 lines)
    HITLIST="/root/git/scripts/text-files/hitlist.txt"
else
    # Short hitlist (Alexa top 500)
    HITLIST="/root/git/scripts/text-files/ipv6-adress-list-alexa-top500-pruned.txt"
fi

# other definitions
TAR_DIR="/root/tarballs"
N_ITERATIONS=1                    # the number of iterations that you wish to run the script. from input args
HITLIST_LENGTH=$(wc -l <$HITLIST) # get the number of lines in file
DATE=$(date '+%Y-%m-%dT%H_%M_%SZ')

create_tarball() {
    cd $TAR_DIR
    echo "Creating tarball..."
    local l_TAR_FILENAME="tar-$HOSTNAME-${DATE}.tar.gz"
    tar -czvf ${l_TAR_FILENAME} -C /root/csv/ .
    echo "Tarball saved to $TAR_DIR/$l_TAR_FILENAME. Cleaning up the /root/csv/-directory..."
    find /root/csv/ -maxdepth 1 -name "*.csv" -print0 | xargs -0 rm
    #find /root/logs/$HOSTNAME/ -maxdepth 1 -name "*.json" -print0 | xargs -0 rm
    echo "Transferring tarball to remote host"
    scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i /root/.ssh/scp-key $TAR_DIR/$l_TAR_FILENAME 209.97.138.74:/root/csv-storage/$l_TAR_FILENAME
    if [ $? -eq 0 ]; then
        echo "Transfer completed successfully. Deleting tarball..."
        rm $TAR_DIR/$l_TAR_FILENAME
        echo "Tarball deleted"
        echo "Cleaning up raw data..."
        #rm /root/raw/*
        find /root/raw/ -maxdepth 1 -name "*.txt" -print0 | xargs -0 rm
    else
        echo "Transfer to remote host failed"
    fi
}

pt_run() {
    local l_DESTINATION_ADDR="$1"
    local l_DESTINATION_PORT="$2"
    local l_FLOW_LABEL="$3"
    local l_FILEPATH="/root/csv/"
    local l_FILENAME="$HOSTNAME-${DATE}.csv"

    echo "Creating .csv"
    touch $l_FILEPATH$l_FILENAME

    echo "Starting paris-traceroute"
    sudo paris-traceroute --num-queries=1 -T -p $l_DESTINATION_PORT $l_FILEPATH$l_FILENAME $l_FLOW_LABEL $l_DESTINATION_ADDR
    echo "paris-traceroute finished. Output saved to $l_FILEPATH$l_FILENAME."
}

for i in $(seq 1 $N_ITERATIONS); do
    for DESTINATION_PORT in "${DESTINATION_PORTS[@]}"; do
        N=1
        let M=$N+9
        while [ $N -lt $HITLIST_LENGTH ]; do
            readarray -t my_array < <(sed -n "${N},${M}p" $HITLIST)
            for FLOW_LABEL in "${FLOW_LABELS[@]}"; do
                for ADDRESS in ${my_array[@]}; do
                    #pt_run "$ELEMENT" &
                    pt_run "$ADDRESS" "$DESTINATION_PORT" "$FLOW_LABEL" &
                done
                wait
            done
            let N=$N+10
            let M=$N+9
        done
    done
    wait
    #create_tarball
done

echo "All done!"
