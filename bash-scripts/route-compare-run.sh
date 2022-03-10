#!/usr/bin/env bash

# ref: https://stackoverflow.com/questions/20796200/how-to-loop-over-files-in-directory-and-change-path-and-add-suffix-to-filename

# comparator = the full path to the base file we want to compare against. The route in the comparator will be compared 
# against all files in its current directory
COMPARATOR=$1

DIRECTORY="$(dirname "${COMPARATOR}")/"
echo "$DIRECTORY"

# Get the route-tag from the filename
TAG=$(echo "$COMPARATOR" | grep -Eo '[0-9a-f]{6}')
echo "Tag: $TAG"

#directory=$1
# comparator = the base file we want to compare against
#comparator=$2

echo "Starting route comparison"

for FILENAME in ${DIRECTORY}*.json; do
    # Check if file exists, if yes continue:
    [ -e "$FILENAME" ] || continue
    # Run command
    TMP=$(echo "$FILENAME" | grep -Eo '[0-9a-f]{6}')
    #echo "Tmp: $TMP"
    # python3 /home/erlend/git/scripts/python-scripts/route-compare-2.py "$comparator" "$filename"
    # python3 /home/erlend/git/scripts/python-scripts/route-compare-2.py "${directory}/$comparator" "$filename"
    # python3 /Users/admin/git/scripts/python-scripts/route-compare-2.py "$comparator" "$filename"
    if [ "$TAG" = "$TMP" ]
    then
        echo "Comparing route"
        #python3 /root/git/scripts/python-scripts/route-compare-3.py "$comparator" "$filename"
        python3 /root/git/scripts/python-scripts/route-compare-3.py "$COMPARATOR" "$FILENAME"
    fi
done

echo "Route comparison complete. Results written to logfile:    /root/logs/route_comparison_output.log"