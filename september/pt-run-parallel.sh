#!/usr/bin/env bash
# Exit when any command fails
#set -e
## Keep track of the last executed command
#trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
## Echo an error message before exiting
#trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT

# port definitions
TRACEROUTE_DEFAULT_PORT=33434
HTTP_PORT=80
HTTPS_PORT=443
SSH_PORT=22
DNS_PORT=53

# flow-label definitions
#00000000000000000000:
FLOW_LABEL_MIN=0
#00000000000000000001:
FLOW_LABEL_LOW_1=1
#00000000000000000010:
FLOW_LABEL_LOW_2=2
#00000000000000001010:
FLOW_LABEL_LOW_3=10
#00000000000100010101:
FLOW_LABEL_MID_1=277
#00011111111111111111:
FLOW_LABEL_MID_2=131071
#11111111111111111111:
FLOW_LABEL_MAX=1048575

##00000000000000000000:
#FLOW_LABEL_0=0
##00000000000000001000:
#FLOW_LABEL_1=8
##00000000000010000000:
#FLOW_LABEL_2=128
##00000000100000000000:
#FLOW_LABEL_3=2048
##00001000000000000000:
#FLOW_LABEL_4=32768
##10000000000000000000:
#FLOW_LABEL_5=524288

#00000000000000000000:
FLOW_LABEL_0=0
#00000000000000001111:
FLOW_LABEL_1=15
#00000000000011110000:
FLOW_LABEL_2=240
#00000000111100000000:
FLOW_LABEL_3=3840
#00001111000000000000:
FLOW_LABEL_4=61440
#11110000000000000000:
FLOW_LABEL_5=983040

# default values
FLOW_LABELS=($FLOW_LABEL_MIN $FLOW_LABEL_LOW_3 $FLOW_LABEL_MID_2 $FLOW_LABEL_MAX)
DESTINATION_PORTS=($TRACEROUTE_DEFAULT_PORT)
HITLIST="/root/git/scripts/text-files/short_hitlist.txt"

# Use large or small hitlist
FULL_HITLIST=true

# Experiment stages
STAGE1=true
STAGE2=false
STAGE3=false

if [ "$STAGE1" = true ]; then
    # Stage 1
    # The goal of stage 1 is to figure out if the flow-label is maintained across all hops to a destination
    #FLOW_LABELS=($FLOW_LABEL_MIN $FLOW_LABEL_LOW_3 $FLOW_LABEL_MID_2)
    FLOW_LABELS=($FLOW_LABEL_0 $FLOW_LABEL_1 $FLOW_LABEL_2 $FLOW_LABEL_3 $FLOW_LABEL_4 $FLOW_LABEL_5)
    #FLOW_LABELS=($FLOW_LABEL_0 $FLOW_LABEL_1)
    #FLOW_LABELS=($FLOW_LABEL_MAX)
    #DESTINATION_PORTS=($TRACEROUTE_DEFAULT_PORT)
    DESTINATION_PORTS=($HTTPS_PORT)
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
    #FLOW_LABELS=($FLOW_LABEL_LOW_1 $FLOW_LABEL_LOW_1 $FLOW_LABEL_LOW_1 $FLOW_LABEL_LOW_1) # Do the experiment 4 times
    FLOW_LABELS=($FLOW_LABEL_0 $FLOW_LABEL_1 $FLOW_LABEL_2 $FLOW_LABEL_3 $FLOW_LABEL_4 $FLOW_LABEL_5)
    #FLOW_LABELS=($FLOW_LABEL_LOW_1 $FLOW_LABEL_LOW_3 $FLOW_LABEL_MID_2)
    DESTINATION_PORTS=($HTTPS_PORT)
    #DESTINATION_PORTS=($TRACEROUTE_DEFAULT_PORT $SSH_PORT $HTTP_PORT $HTTPS_PORT) # get destination tcp-port from input args
fi

if [ "$FULL_HITLIST" = true ]; then
    # Short hitlist (20 lines)
    HITLIST="/root/git/scripts/text-files/short_hitlist.txt"

    # Long hitlist (15757 lines)
    #HITLIST="/root/git/scripts/text-files/hitlist.txt"
else
    # Short hitlist (Alexa top 500)
    HITLIST="/root/git/scripts/text-files/ipv6-address-list-alexa-top500-pruned.txt"
fi

# Other definitions
LOCALHOST_IP=$(hostname -I | grep -o -E "((([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])))")
TAR_DIR="/root/tarballs"
N_ITERATIONS=4 # The number of iterations that you wish to run the experiment.
HITLIST_LENGTH=$(wc -l <$HITLIST)
DATE=$(date '+%Y-%m-%dT%H_%M_%SZ')
CSV_FILEPATH="/root/csv/"
CSV_FILENAME="$HOSTNAME-${DATE}.csv"
echo "Creating $CSV_FILEPATH$CSV_FILENAME..."
touch $CSV_FILEPATH$CSV_FILENAME
if [ $? -eq 0 ]; then
    echo "File $CSV_FILEPATH$CSV_FILENAME created successfully."
    echo "Outgoing Flow Label, Outgoing Port, Timestamp, Source IP, Source ASN, Destination IP, Destination ASN, Hop Count, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN, Hop Number, Hop Flow Label, Hop IP, Hop ASN" >$CSV_FILEPATH$CSV_FILENAME
else
    echo "File creation failed."
fi

create_tarball() {
    cd $TAR_DIR
    echo "Creating tarball..."
    local l_TAR_FILENAME="tar-$HOSTNAME-${DATE}.tar.gz"
    tar -czvf ${l_TAR_FILENAME} -C /root/csv/ .
    echo "Tarball saved to $TAR_DIR/$l_TAR_FILENAME."
    echo "Transferring tarball to remote host..."
    scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i /root/.ssh/scp-key $TAR_DIR/$l_TAR_FILENAME 209.97.138.74:/root/csv-storage/$l_TAR_FILENAME
    if [ $? -eq 0 ]; then
        echo "Transfer completed successfully. Deleting local tarball..."
        rm $TAR_DIR/$l_TAR_FILENAME
        echo "Tarball deleted."
        echo "Cleaning up raw data..."
        find /root/csv/ -maxdepth 1 -name "*.csv" -print0 | xargs -0 rm
    else
        echo "Transfer to remote host failed."
    fi
}

pt_run() {
    local l_DESTINATION_ADDR="$1"
    local l_DESTINATION_PORT="$2"
    local l_FLOW_LABEL="$3"

    echo "Starting paris-traceroute."
    sudo paris-traceroute --num-queries=1 -T -p $l_DESTINATION_PORT $LOCALHOST_IP $CSV_FILEPATH$CSV_FILENAME $l_FLOW_LABEL $l_DESTINATION_ADDR >/dev/null
    echo "Paris-traceroute finished. Output saved to $CSV_FILEPATH$CSV_FILENAME."
}

for i in $(seq 1 $N_ITERATIONS); do
    for DESTINATION_PORT in "${DESTINATION_PORTS[@]}"; do
        for FLOW_LABEL in "${FLOW_LABELS[@]}"; do
            N=1
            M=11
            while [ $N -lt $HITLIST_LENGTH ]; do
                readarray -t my_array < <(sed -n "${N},${M}p" $HITLIST)
                for ADDRESS in ${my_array[@]}; do
                    pt_run "$ADDRESS" "$DESTINATION_PORT" "$FLOW_LABEL" &
                done
                wait
                let N=$N+11
                let M=$M+11
            done
        done
    done
    wait
done
create_tarball
echo "All done!"
