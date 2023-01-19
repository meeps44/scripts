#!/usr/bin/env bash

apt update && apt -y install sqlite3 libsqlite3-dev libssl-dev
mkdir /root/csv /root/tarballs /root/git /root/db /root/db-storage
git -C /root/git clone https://github.com/meeps44/libparistraceroute.git
cd /root/git/libparistraceroute
mkdir m4
./autogen.sh
./configure
ldconfig
make
make install
export PATH=$PATH:/root/git/libparistraceroute/paris-traceroute
ldconfig
git -C /root/git clone https://github.com/meeps44/scripts.git
