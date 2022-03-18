#!/usr/bin/env bash

LIST="/root/git/scripts/text-files/ipv6-address-list-pruned-2.txt"
LIST_LENGTH=$(wc -l < $LIST) # get the number of lines in file
#echo "$LIST_LENGTH"
N=1
let M=$N+9

pt_test()
{
    destination_address=$line
    hash=$(echo -n ${destination_address} | md5sum | awk '{print $1}')
    short="${hash:0:6}"
    date=$(date '+%d-%H-%M-%S')
    filepath="/root/raw/"
    filename="$HOSTNAME-${short}-${date}.txt"
    echo $filepath$filename $HOSTNAME ${destination_port} ${host_ip} ${flow_label} > "/root/test/$filename"
}

pt_run()
{
    destination_address=$line
    hash=$(echo -n ${destination_address} | md5sum | awk '{print $1}')
    short="${hash:0:6}"
    date=$(date '+%d-%H-%M-%S')
    filepath="/root/raw/"
    filename="$HOSTNAME-${short}-${date}.txt"
    echo "Starting paris-traceroute"
    sudo paris-traceroute -T -p ${destination_port} "${flow_label}" "${destination_address}" > $filepath$filename
    echo "paris-traceroute finished. Output saved in $filename."
    echo "Converting to JSON..."
    python3 /root/git/scripts/python-scripts/text-to-json-2.py $filepath$filename $HOSTNAME ${destination_port} ${host_ip} ${flow_label}
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
FLOW_LABEL_MID_1=277
FLOW_LABEL_MID_2=131071
FLOW_LABEL_MAX=1048575

#flow_labels=($FLOW_LABEL_MIN)
flow_labels=($FLOW_LABEL_MID_2)
#flow_labels=($FLOW_LABEL_MIN $FLOW_LABEL_MID_1 $FLOW_LABEL_MID_2 $FLOW_LABEL_MAX)
destination_ports=($TRACEROUTE_DEFAULT_PORT $SSH_PORT $HTTP_PORT $HTTPS_PORT) # get destination tcp-port from input args
# destination_port=$1 # get destination tcp-port from input args
host_ip=$(hostname -I | grep -o -E "((([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])))")

for destination_port in "${destination_ports[@]}"; do
    for flow_label in "${flow_labels[@]}"; do
        while [ $N -lt $LIST_LENGTH ]; do
        readarray -t my_array < <(sed -n "${N},${M}p" $LIST)
            for ELEMENT in ${my_array[@]}; do
                #echo $ELEMENT
                #pt_run "$ELEMENT" &
                pt_test "$ELEMENT" &
            done
        let N=$N+10
        let M=$N+9
        #echo "N: $N"
        #echo "M: $M"
        done

    done
done

wait
echo "All done!"