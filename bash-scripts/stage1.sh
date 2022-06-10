#!/usr/bin/env bash

# Stage 1
# The goal of stage 1 is to figure out if the flow-label is maintained across all hops to a destination

create_tarball()
{
    cd $TAR_DIR
    echo "Creating tarball..."
    local l_DATE=$(date -u +'%Y-%m-%dT%H%M%SZ')
    #local l_DATE=$(date '+%d-%m-%y-%H-%M-%S')
    local l_TAR_FILENAME="tar-$HOSTNAME-${l_DATE}.tar.gz"
    tar -czvf ${l_TAR_FILENAME} -C /root/logs/$HOSTNAME/ .
    echo "Tarball saved to $TAR_DIR/$l_TAR_FILENAME. Cleaning up the /root/logs/$HOSTNAME/-directory..."
	# Clean up JSON-files
    find /root/logs/$HOSTNAME/ -maxdepth 1 -name "*.json" -print0 | xargs -0 rm
    echo "Transferring tarball to remote host"
    scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i /root/.ssh/scp-key $TAR_DIR/$l_TAR_FILENAME 209.97.138.74:/root/archived-logs/$l_TAR_FILENAME
    if [ $? -eq 0 ];
    then
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

pt_run()
{
    local l_DESTINATION_ADDR="$1"
    local l_DESTINATION_PORT="$2"
    local l_FLOW_LABEL="$3"
    local l_HASH=$(echo -n ${l_DESTINATION_ADDR} | md5sum | awk '{print $1}')
    local l_SHORT="${l_HASH:0:8}"
    #local l_DATE=$(date '+%d-%H-%M-%S')
    local l_DATE=$(date -u +'%Y-%m-%dT%H%M%SZ')
    local l_FILEPATH="/root/raw/"
    local l_FILENAME="$HOSTNAME-${l_SHORT}-${l_DATE}.txt"

    echo "Starting paris-traceroute"
    sudo paris-traceroute --num-queries=1 -T -p ${l_DESTINATION_PORT} "${l_FLOW_LABEL}" "${l_DESTINATION_ADDR}" > $l_FILEPATH$l_FILENAME
    echo "paris-traceroute finished. Output saved to $l_FILEPATH$l_FILENAME."
    echo "Converting to JSON..."
    python3 /root/git/scripts/python-scripts/json_convert_single-2.py $l_FILEPATH $l_FILENAME ${l_DESTINATION_PORT} ${HOST_IP} ${l_SHORT} ${l_FLOW_LABEL}
    #python3 /root/git/scripts/python-scripts/json_convert_single-3.py $l_FILEPATH $l_FILENAME ${l_DESTINATION_PORT} ${HOST_IP} ${l_SHORT} ${l_FLOW_LABEL}
}

main()
{
	# Number of iterations to run the entire sequence
	N_ITERATIONS=1 
	N_PARALLEL=20 # the number of parallel running instances of Paris traceroute

	# Port definitions
	TRACEROUTE_DEFAULT_PORT=33434
	HTTP_PORT=80
	HTTPS_PORT=443
	SSH_PORT=22
	DNS_PORT=53

	# Flow-label definitions
	FLOW_LABEL_MIN=0
	FLOW_LABEL_LOW=1
	FLOW_LABEL_MID=256
	FLOW_LABEL_HIGH=524288
	FLOW_LABEL_MAX=1048575
	
	# default values
	FLOW_LABELS=(
        $FLOW_LABEL_MIN  
        $FLOW_LABEL_LOW  
        $FLOW_LABEL_MID  
        $FLOW_LABEL_HIGH 
        )
	DESTINATION_PORTS=($HTTPS_PORT) 
	HITLIST="/root/git/scripts/text-files/responsive-alexatop500-addresses-3105.txt"
	

	# Use large or small hitlist
	USE_FULL_HITLIST=false

	if [ "$USE_FULL_HITLIST" = true ] ; then
		# Full hitlist
		HITLIST="/root/git/scripts/text-files/hitlist.txt"
	else
		# Short hitlist (Alexa top 500)
		HITLIST="/root/git/scripts/text-files/responsive-alexatop500-addresses-3105.txt"
	fi

	# Other definitions
	HOST_IP=$(hostname -I | grep -o -E "((([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])))")
	TAR_DIR="/root/tarballs"
	HITLIST_LENGTH=$(wc -l < $HITLIST) # get the number of lines in file
	host_ip=$(hostname -I | grep -o -E "((([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])))")

	# Paris traceroute loop starts here
	for i in $(seq 1 $N_ITERATIONS); do
	for DESTINATION_PORT in "${DESTINATION_PORTS[@]}"; do
		for FLOW_LABEL in "${FLOW_LABELS[@]}"; do
		N=1
		let M=$N+$N_PARALLEL-1
		while [ $N -lt $HITLIST_LENGTH ]; do
			readarray -t my_array < <(sed -n "${N},${M}p" $HITLIST)
			for ADDRESS in ${my_array[@]}; do
				pt_run "$ADDRESS" "$DESTINATION_PORT" "$FLOW_LABEL" &
			done
			let N=$N+$N_PARALLEL
			let M=$N+$N_PARALLEL-1
			wait
		done
		done
	done
	wait
	create_tarball
	done

	echo "All done!"
}

main

