#!/usr/bin/env bash

TAR_DIR="/root/tarballs"
DATE=$(date '+%Y-%m-%dT%H_%M_%SZ')
TAR_FILENAME="tar-$HOSTNAME-$DATE.tar.gz"
cd $TAR_DIR
echo "Creating tarball..."
tar -czvf $TAR_FILENAME -C /root/csv/ .
echo "Tarball saved to $TAR_DIR/$TAR_FILENAME."
echo "Transferring tarball to remote host..."
scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i /root/.ssh/scp-key $TAR_DIR/$TAR_FILENAME 209.97.138.74:/root/csv-storage/$TAR_FILENAME
if [ $? -eq 0 ]; then
    echo "Transfer completed successfully!"
else
    echo "Transfer to remote host failed."
fi
echo "All done!"
