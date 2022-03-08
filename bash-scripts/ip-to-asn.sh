#! /usr/bin/bash

END=3

# Iterates from 1 up to and including $END
for i in $(seq 1 $END); do 
	echo $i 
	echo $(whois 240e:398:303:44ac:7e03:c9f1:238f:b530 | grep origin)
done