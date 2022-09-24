#!/usr/bin/env bash
# Port definitions:
TRACEROUTE_DEFAULT_PORT=33434
HTTP_PORT=80
HTTPS_PORT=443
SSH_PORT=22
DNS_PORT=53

# Other definitions:
DESTINATION_PORTS=($HTTPS_PORT)
HITLIST="/root/git/scripts/text-files/short_hitlist.txt"
FLOW_LABEL_LIST="/root/git/scripts/text-files/flow_labels.txt"
LOCALHOST_IP=$(hostname -I | grep -o -E "((([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])))")
TAR_DIR="/root/tarballs"
N_ITERATIONS=1
HITLIST_LENGTH=$(wc -l <$HITLIST)
DATE=$(date '+%Y-%m-%dT%H_%M_%SZ')
CSV_FILEPATH="/root/csv/"
CSV_FILENAME="$HOSTNAME-$DATE.csv"
TAR_FILENAME="tar-$HOSTNAME-$DATE.tar.gz"

pt_run() {
    local l_DESTINATION_ADDR_LIST="$1"
    local l_DESTINATION_PORT="$2"
    local l_FLOW_LABEL_LIST="$3"

    echo "Starting paris-traceroute."
    #sudo /root/git/libparistraceroute/paris-traceroute/paris-traceroute --num-queries=1 -T -p $l_DESTINATION_PORT $N_ITERATIONS $LOCALHOST_IP $CSV_FILEPATH$CSV_FILENAME $l_FLOW_LABEL_LIST $l_DESTINATION_ADDR_LIST >/dev/null
    echo "/root/git/libparistraceroute/paris-traceroute/paris-traceroute --num-queries=1 -T -p $l_DESTINATION_PORT $N_ITERATIONS $LOCALHOST_IP $CSV_FILEPATH$CSV_FILENAME $l_FLOW_LABEL_LIST $l_DESTINATION_ADDR_LIST"
    sudo /root/git/libparistraceroute/paris-traceroute/paris-traceroute --num-queries=1 -T -p $l_DESTINATION_PORT $N_ITERATIONS $LOCALHOST_IP $CSV_FILEPATH$CSV_FILENAME $l_FLOW_LABEL_LIST $l_DESTINATION_ADDR_LIST
    echo "Paris-traceroute finished. Output saved to $CSV_FILEPATH$CSV_FILENAME."
}

# Declare an array of string with type
#declare -a StringArray=("/root/git/scripts/text-files/hitlist/hitlist1.txt" "/root/git/scripts/text-files/hitlist/hitlist2.txt" "/root/git/scripts/text-files/hitlist/hitlist3.txt" "/root/git/scripts/text-files/hitlist/hitlist4.txt" "/root/git/scripts/text-files/hitlist/hitlist5.txt" "/root/git/scripts/text-files/hitlist/hitlist6.txt" "/root/git/scripts/text-files/hitlist/hitlist7.txt" "/root/git/scripts/text-files/hitlist/hitlist8.txt" "/root/git/scripts/text-files/hitlist/hitlist9.txt" "/root/git/scripts/text-files/hitlist/hitlist10.txt")
declare -a StringArray=("/root/git/scripts/text-files/hitlist/hitlist1.txt" "/root/git/scripts/text-files/hitlist/hitlist2.txt")

# Iterate the string array using for loop
for item in ${StringArray[@]}; do
    echo "$item"
    pt_run "$item" "$DESTINATION_PORT" "$FLOW_LABEL_LIST" &
done
wait
echo "All done!"
