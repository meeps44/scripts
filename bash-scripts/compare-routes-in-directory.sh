#!/usr/bin/env bash

# ref: https://stackoverflow.com/questions/20796200/how-to-loop-over-files-in-directory-and-change-path-and-add-suffix-to-filename

# comparator = the full path to the base file we want to compare against. The route in the comparator will be compared 
# against all files in its current directory
comparator=$1

directory="$(dirname "${comparator}")/"
echo "$directory"

#directory=$1
# comparator = the base file we want to compare against
#comparator=$2

echo "Starting route comparison"

for filename in ${directory}*.json; do
    # Check if file exists, if yes continue:
    [ -e "$filename" ] || continue
    # Run command
    echo "Comparing route"
    # python3 /home/erlend/git/scripts/python-scripts/route-compare-2.py "$comparator" "$filename"
    # python3 /home/erlend/git/scripts/python-scripts/route-compare-2.py "${directory}/$comparator" "$filename"
    # python3 /Users/admin/git/scripts/python-scripts/route-compare-2.py "$comparator" "$filename"
    python3 /root/git/scripts/python-scripts/route-compare-3.py "$comparator" "$filename"
done

echo "Route comparison complete. Results written to logfile:    /root/logs/comparison_output.log"