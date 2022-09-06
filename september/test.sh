#HITLIST="/home/erlend/git/scripts/text-files/hitlist.txt"
HITLIST="/root/git/scripts/text-files/hitlist.txt"
HITLIST_LENGTH=$(wc -l <$HITLIST) # get the number of lines in file
N=1
readarray -t my_array < <(sed -n "1, ${HITLIST_LENGTH}p" $HITLIST)
for ADDRESS in ${my_array[@]}; do
    #Sleep for 100 seconds
    sleep 100
done
