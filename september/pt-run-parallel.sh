#!/usr/bin/env bash

# Test definitions:
TEST=false
LOCALHOST_IP=$(hostname -I | grep -o -E "((([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])))")
TAR_DIR="/root/tarballs/"
N_ITERATIONS=1 # The number of iterations that you wish to run the full experiment.
N_PARALLEL=8   # Number of parallel Paris traceroute instances.
DATE=$(date '+%Y-%m-%dT%H_%M_%SZ')
DB_FILEPATH="/root/db/"
DB_FILENAME="db-$HOSTNAME-$DATE.db"
TAR_FILENAME="tar-$HOSTNAME-$DATE.tar.gz"

# Port definitions:
TRACEROUTE_DEFAULT_PORT=33434
HTTP_PORT=80
HTTPS_PORT=443
SSH_PORT=22
DNS_PORT=53
DESTINATION_PORTS=($HTTP_PORT $HTTPS_PORT)

# Flow-label definitions
#0000 00000000 00000000:
FLOW_LABEL_0=0 #(decimal), 0 hex
#0000 00000000 11111111:
FLOW_LABEL_1=255 #(decimal), FF hex
#0000 11111111 00000000:
FLOW_LABEL_2=65280 #(decimal), FF00 hex
#1111 00000000 00000000:
FLOW_LABEL_3=983040 #(decimal), F0000 hex
#1111 11111111 11111111:
FLOW_LABEL_4=1048575 #(decimal), FFFFF hex

# Flow label and port value definitions:
FLOW_LABELS=($FLOW_LABEL_0 $FLOW_LABEL_1 $FLOW_LABEL_2 $FLOW_LABEL_3 $FLOW_LABEL_4)
if [ "$TEST" = true ]; then
    # Short hitlist (20 lines)
    HITLIST="/root/git/scripts/text-files/short_hitlist.txt"
    # Short hitlist (112 lines)
    # HITLIST="/root/git/scripts/text-files/ipv6-address-list-alexa-top500-pruned.txt"
else
    # Long hitlist (15757 lines)
    HITLIST="/root/git/scripts/text-files/hitlist.txt"
fi

create_tarball() {
    cd $TAR_DIR
    echo "Creating tarball..."
    tar -czvf $TAR_FILENAME -C $DB_FILEPATH $DB_FILENAME
    echo "Tarball saved to $TAR_DIR$TAR_FILENAME."
    echo "Transferring tarball to remote host..."
    scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i /root/.ssh/scp-key $TAR_DIR$TAR_FILENAME 209.97.138.74:/root/db-storage/$TAR_FILENAME
    if [ $? -eq 0 ]; then
        echo "Transfer completed successfully. Deleting local tarball..."
        rm $TAR_DIR$TAR_FILENAME
        echo "Tarball deleted."
        echo "Cleaning up raw data..."
        find /root/db/ -maxdepth 1 -name "*.db" -print0 | xargs -0 rm
    else
        echo "Transfer to remote host failed."
    fi
}

transfer_db() {
    cd $TAR_DIR
    echo "Creating tarball..."
    tar -czvf $TAR_FILENAME -C $DB_FILEPATH $DB_FILENAME
    echo "Tarball saved to $TAR_DIR$TAR_FILENAME."
    echo "Transferring tarball to remote host..."
    scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i /root/.ssh/scp-key $TAR_DIR$TAR_FILENAME 209.97.138.74:/root/db-storage/$TAR_FILENAME
    if [ $? -eq 0 ]; then
        echo "Tarball transfer to remote host completed successfully."
    else
        echo "Tarball transfer to remote host failed."
    fi
}

pt_run() {
    local l_DESTINATION_ADDR="$1"
    local l_DESTINATION_PORT="$2"
    local l_FLOW_LABEL="$3"

    # Start Paris traceroute #
    sudo /root/git/libparistraceroute/paris-traceroute/paris-traceroute --num-queries=1 -T -p $l_DESTINATION_PORT $START_TIME $LOCALHOST_IP $DB_FILEPATH$DB_FILENAME $l_FLOW_LABEL $l_DESTINATION_ADDR >/dev/null
    echo "Paris traceroute finished. Output saved to $DB_FILEPATH$DB_FILENAME."
}

main() {
    HITLIST_LENGTH=$(wc -l <$HITLIST)
    N=1
    M=$N_PARALLEL
    while [ $N -lt $HITLIST_LENGTH ]; do
        readarray -t ip_array < <(sed -n "${N},${M}p" $HITLIST)
        for ADDRESS in ${ip_array[@]}; do
            START_TIME=$(date '+%s')
            for FLOW_LABEL in "${FLOW_LABELS[@]}"; do
                for DESTINATION_PORT in "${DESTINATION_PORTS[@]}"; do
                    for i in $(seq 1 $N_ITERATIONS); do
                        pt_run "$ADDRESS" "$DESTINATION_PORT" "$FLOW_LABEL" &
                    done
                done
            done
            wait
        done
        let N=$N+$N_PARALLEL
        let M=$M+$N_PARALLEL
    done
}

test -f /root/time.log || touch /root/time.log
echo "Start time: $(date)" >>/root/time.log
main
echo "End time: $(date)" >>/root/time.log
transfer_db
echo "All done!"
