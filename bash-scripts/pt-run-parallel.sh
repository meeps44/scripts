#!/usr/bin/env bash

LIST="/root/git/scripts/text-files/ipv6-address-list-pruned-2.txt"
LIST_LENGTH=$(wc -l < $LIST) # get the number of lines in file
#echo "$LIST_LENGTH"
#N=1
#let M=$N+9

pt_test()
{
    echo "Hello from pt_test()"
    local l_DESTINATION_PORT=$1
    local l_FLOW_LABEL=$2
    local l_DESTINATION_ADDR=$3
    echo $l_DESTINATION_PORT $l_FLOW_LABEL $l_DESTINATION_ADDR

    local l_HASH=$(echo -n ${l_DESTINATION_ADDR} | md5sum | awk '{print $1}')
    local l_SHORT="${l_HASH:0:6}"
    local l_DATE=$(date '+%d-%H-%M-%S')
    local l_FILEPATH="/root/raw/"
    local l_FILENAME="$l_HOSTNAME-${l_SHORT}-${l_DATE}.txt"
    #echo $l_FILEPATH$l_FILENAME $l_HOSTNAME ${l_DESTINATION_PORT} ${l_HOST_IP} ${l_FLOW_LABEL} > "/root/test/$l_FILENAME"
    echo "Executing tracepath. Dst addr: $l_DESTINATION_ADDR"
    #tracepath -m 8 $l_DESTINATION_ADDR > "/root/test/$l_FILENAME"
}

#pt_run()
#{
    #destination_address=$line
    #hash=$(echo -n ${destination_address} | md5sum | awk '{print $1}')
    #short="${hash:0:6}"
    #date=$(date '+%d-%H-%M-%S')
    #filepath="/root/raw/"
    #filename="$HOSTNAME-${short}-${date}.txt"
    #echo "Starting paris-traceroute"
    #sudo paris-traceroute -T -p ${destination_port} "${flow_label}" "${destination_address}" > $filepath$filename
    #echo "paris-traceroute finished. Output saved in $filename."
    #echo "Converting to JSON..."
    #python3 /root/git/scripts/python-scripts/text-to-json-2.py $filepath$filename $HOSTNAME ${destination_port} ${host_ip} ${flow_label}
#}

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
FLOW_LABELS=($FLOW_LABEL_MID_2)
#flow_labels=($FLOW_LABEL_MIN $FLOW_LABEL_MID_1 $FLOW_LABEL_MID_2 $FLOW_LABEL_MAX)
DESTINATION_PORTS=($TRACEROUTE_DEFAULT_PORT $SSH_PORT) # get destination tcp-port from input args
#DESTINATION_PORTS=($TRACEROUTE_DEFAULT_PORT $SSH_PORT $HTTP_PORT $HTTPS_PORT) # get destination tcp-port from input args
# destination_port=$1 # get destination tcp-port from input args
host_ip=$(hostname -I | grep -o -E "((([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])))")

for DESTINATION_PORT in "${DESTINATION_PORTS[@]}"; do
    for FLOW_LABEL in "${FLOW_LABELS[@]}"; do
        N=1
        let M=$N+9
        while [ $N -lt $LIST_LENGTH ]; do
            readarray -t my_array < <(sed -n "${N},${M}p" $LIST)
                for ADDRESS in ${my_array[@]}; do
                    #echo "$DESTINATION_PORT $FLOW_LABEL $ADDRESS"
                    #echo $ELEMENT
                    #pt_run "$ELEMENT" &
                    pt_test "$DESTINATION_PORT $FLOW_LABEL $ADDRESS" &
                done
            let N=$N+10
            let M=$N+9
            wait
            #echo "N: $N"
            #echo "M: $M"
        done
    done
done

wait
echo "All done!"