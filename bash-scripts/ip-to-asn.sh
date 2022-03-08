#! /usr/bin/bash

END=3

# Iterates from 1 up to and including $END
for i in $(seq 1 $END); do 
	echo $i 
done

# Iterates through each line in a text file
cat /home/erlend/python-programming/ipv6-addresses-test.txt | while read line; do
	# echo $i 
	echo "IP: $line"
	echo $(whois $line | grep origin)
	
	# grep multiple patterns:
	echo $(whois $line | grep -E 'origin|route6')
done