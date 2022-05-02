#!/usr/bin/env bash

# Stage 3
# The goal of this step is to delve into the cases from stage 2
# We want to know if we get the same path if we use a different port-number. 

create_tarball()
{
    cd $TAR_DIR
    echo "Creating tarball..."
    local l_DATE=$(date '+%d-%m-%y-%H-%M-%S')
    local l_TAR_FILENAME="tar-$HOSTNAME-${l_DATE}.tar.gz"
    tar -czvf ${l_TAR_FILENAME} -C /root/logs/$HOSTNAME/ .
    echo "Tarball saved to $TAR_DIR/$l_TAR_FILENAME. Cleaning up the /root/logs/$HOSTNAME/-directory..."
    find /root/logs/$HOSTNAME/ -maxdepth 1 -name "*.json" -print0 | xargs -0 rm
    #rm /root/logs/$HOSTNAME/*
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
    local l_SHORT="${l_HASH:0:6}"
    local l_DATE=$(date '+%d-%H-%M-%S')
    local l_FILEPATH="/root/raw/"
    local l_FILENAME="$HOSTNAME-${l_SHORT}-${l_DATE}.txt"

    echo "Starting paris-traceroute"
    sudo paris-traceroute --num-queries=1 -T -p ${l_DESTINATION_PORT} "${l_FLOW_LABEL}" "${l_DESTINATION_ADDR}" > $l_FILEPATH$l_FILENAME
    #sudo paris-traceroute --first=2 --num-queries=1 -T -p ${l_DESTINATION_PORT} "${l_FLOW_LABEL}" "${l_DESTINATION_ADDR}" > $l_FILEPATH$l_FILENAME # skips the first router in the path
    echo "paris-traceroute finished. Output saved in $l_FILENAME."
    echo "Converting to JSON..."
    python3 /root/git/scripts/python-scripts/text-to-json-2.py $l_FILEPATH$l_FILENAME $HOSTNAME ${l_DESTINATION_PORT} ${HOST_IP} ${l_FLOW_LABEL}
}

main()
{
	N_ITERATIONS=1 # the number of iterations that you wish to run the entire sequence

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
	FLOW_LABELS=(
        $FLOW_LABEL_MIN $FLOW_LABEL_MIN $FLOW_LABEL_MIN $FLOW_LABEL_MIN 
        $FLOW_LABEL_LOW_1 $FLOW_LABEL_LOW_1 $FLOW_LABEL_LOW_1 $FLOW_LABEL_LOW_1
        $FLOW_LABEL_MID_2 $FLOW_LABEL_MID_2 $FLOW_LABEL_MID_2 $FLOW_LABEL_MID_2 
        $FLOW_LABEL_HIGH_1 $FLOW_LABEL_HIGH_1 $FLOW_LABEL_HIGH_1 $FLOW_LABEL_HIGH_1 
        $FLOW_LABEL_MAX $FLOW_LABEL_MAX $FLOW_LABEL_MAX $FLOW_LABEL_MAX 
        )
	DESTINATION_PORTS=($TRACEROUTE_DEFAULT_PORT $SSH_PORT $HTTP_PORT $HTTPS_PORT $DNS_PORT) 
	HITLIST="/root/git/scripts/text-files/responsive-alexatop500-addresses.txt"
	

	# Use large or small hitlist
	USE_FULL_HITLIST=false

	if [ "$USE_FULL_HITLIST" = true ] ; then
		# Full hitlist
		HITLIST="/root/git/scripts/text-files/hitlist.txt"
	else
		# Short hitlist (Alexa top 500)
		HITLIST="/root/git/scripts/text-files/responsive-alexatop500-addresses.txt"
	fi

	# other definitions
	HOST_IP=$(hostname -I | grep -o -E "((([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])))")
	TAR_DIR="/root/tarballs"
	HITLIST_LENGTH=$(wc -l < $HITLIST) # get the number of lines in file
	host_ip=$(hostname -I | grep -o -E "((([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])))")
	FLOW_LABELS=($FLOW_LABEL_MIN $FLOW_LABEL_MIN $FLOW_LABEL_MIN $FLOW_LABEL_MIN)
	DESTINATION_PORTS=($TRACEROUTE_DEFAULT_PORT) 

	# paris traceroute loop starts here
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
	create_tarball
	done

	echo "All done!"
}

main

