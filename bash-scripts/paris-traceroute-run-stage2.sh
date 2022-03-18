#!/usr/bin/env bash

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
        cat /root/git/scripts/text-files/ipv6-address-list-pruned-2.txt | while read line; do
        #cat /root/git/scripts/text-files/ipv6-address-list-pruned.txt | while read line; do
        #cat /root/git/scripts/python-scripts/ipv6-address-list-new.txt | while read line; do
            destination_address=$line
            hash=$(echo -n ${destination_address} | md5sum | awk '{print $1}')
            short="${hash:0:6}"
            date=$(date '+%d-%H-%M-%S')
            filepath="/root/raw/"
            filename="$HOSTNAME-${short}-${date}.txt"
            #sudo paris-traceroute -T "${flow_label}" "${destination_address}" > tmp.txt

            #sudo paris-traceroute -T -p ${destination_port} "${flow_label}" "${destination_address}" > tmp.txt
            echo "Starting paris-traceroute"
            sudo paris-traceroute -T -p ${destination_port} "${flow_label}" "${destination_address}" > $filepath$filename
            #date=$(date '+%Y-%m-%d-%H-%M-%S')
            #filename="$HOSTNAME-${date}-${short}.txt"
            #grep -o -E "((([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])) | \* \* \*)" tmp.txt >> $filename
            #grep -o -E "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))" tmp.txt >> $filename
            echo "paris-traceroute finished. Output saved in $filename."
            echo "Converting to JSON..."
            #python3 /root/git/scripts/python-scripts/text-to-json-2.py /root/git/scripts/bash-scripts/${filename} $HOSTNAME ${destination_port} ${host_ip} ${flow_label}
            python3 /root/git/scripts/python-scripts/text-to-json-2.py $filepath$filename $HOSTNAME ${destination_port} ${host_ip} ${flow_label}
            # Create directory:
            #ssh -i ~/.ssh/scp-key 209.97.138.74 "mkdir -p /root/logs/${HOSTNAME}/${short}"
            #scp -i ~/.ssh/scp-key ../bash-scripts/${filename} 209.97.138.74:/root/logs/${HOSTNAME}/${short}
        done
    done
done
