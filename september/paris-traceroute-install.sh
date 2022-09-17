#!/usr/bin/env bash

#sudo apt install libssl-dev -y
apt -y install libssl-dev
mkdir /root/csv /root/tarballs /root/git
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
git -C /root/git clone https://github.com/meeps44/scripts.git
