#! /usr/bin/bash

# ASNMAP="$HOME/git/scripts/text-files/asnmap.txt" # Alternative location
ASNMAP="$HOME/logs/asnmap.txt"
END=3

# Iterates through ASNs from 1 to $END and logs the advertised IPv6 prefixes
for i in $(seq 1 $END); do 
	#echo $i 
	#echo "IP: $i ASN: $(asn -n $i | grep ASN)" >> $ASNMAP
	echo "ASN: $i" >> $ASNMAP
	asn $i | sed -n '/ IPv6 /,$p' >> $ASNMAP
done

# Iterates through each IP-address in a text file and gets the ASN using WHOIS
cat $HOME/git/scripts/text-files/ipv6-addresses-test.txt | while read line; do
	# echo $i 
	echo "IP: $line"
	echo $(whois $line | grep origin)
	
	# grep multiple patterns:
	echo $(whois $line | grep -E 'origin|route6|Origin')
done

# Iterates through each IP-address in a text file and gets the origin ASN using nitefood's ASN lookup tool
# https://github.com/nitefood/asn
cat $HOME/git/scripts/text-files/ipv6-addresses-test.txt | while read line; do
	# echo $i 
	echo "IP: $line ASN: $(asn -n $line | grep ASN)" >> $ASNMAP
done