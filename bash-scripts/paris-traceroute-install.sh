#!/usr/bin/env bash

mkdir /root/csv /root/csv-storage /root/git /root/raw /root/logs
sudo apt -y install libssl-dev
git -C /root/git clone https://github.com/meeps44/libparistraceroute.git
cd /root/git/libparistraceroute
mkdir m4
./autogen.sh
./configure
ldconfig
make
make install
export PATH=$PATH:~/git/libparistraceroute/paris-traceroute
ldconfig
#apt -y install python3-pip
#python3 -m pip install pysubnettree