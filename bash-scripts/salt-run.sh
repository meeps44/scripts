#!/usr/bin/env bash

setup()
{
	salt '*' cmd.run 'mkdir -p /root/.ssh' 
	salt-cp '*' /root/.ssh/scp-key /root/.ssh/
	salt-cp '*' /root/.ssh/scp-key.pub /root/.ssh/
	salt '*' cmd.run 'cat /root/.ssh/scp-key.pub >> /root/.ssh/authorized_keys'
	salt '*' cmd.run 'chmod 600 /root/.ssh/scp-key'
	salt '*' cmd.run 'git -C /root/git/scripts pull'
	salt '*' cmd.run 'mkdir -p /root/tarballs'
}

run()
{
	salt '*' cmd.run 'bash /root/git/scripts/bash-scripts/pt-run-parallel-2.sh'
}