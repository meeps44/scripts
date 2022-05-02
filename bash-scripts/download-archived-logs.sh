#!/usr/bin/env bash
# Downloads archived logs from salt master server

LOCAL_DIR="/home/erlend/logs/"
REMOTE_DIR="/root/archived-logs/"
REMOTE_HOST="209.97.138.74"

scp -i /home/erlend/.ssh/new-key -r $REMOTE_HOST:$REMOTE_DIR $LOCAL_DIR
