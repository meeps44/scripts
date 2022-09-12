#!/usr/bin/env bash

#sudo apt install libssl-dev -y
apt install libssl-dev -y
mkdir $HOME/csv
mkdir $HOME/tarballs
mkdir ~/git
git -C $HOME/git clone https://github.com/meeps44/libparistraceroute.git
cd $HOME/git/libparistraceroute
mkdir m4
./autogen.sh
./configure
ldconfig
make
make install
export PATH=$PATH:~/git/libparistraceroute/paris-traceroute
ldconfig
