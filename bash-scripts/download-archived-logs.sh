#!/usr/bin/env bash
# Downloads archived logs from salt master server

LOCAL_DIR="/home/erlend/logs/db-storage/"
REMOTE_DIR="/root/db-storage/"
REMOTE_HOST="209.97.138.74"

scp -i "/home/erlend/.ssh/scp-key" -r root@$REMOTE_HOST:$REMOTE_DIR $LOCAL_DIR

echo "Files saved to $LOCAL_DIR"

