#!/usr/bin/env bash

# parses paris-traceroute json-data and creates statistics and/or figures

# first find and unpack all zipped data
tar -xf /root/archived-logs/tar-*

# call a python-script to parse json-data
python3 generate-statistics.py

# call a python-script to generate CDF (done via matplotlib)
python3 generate-CDF.py