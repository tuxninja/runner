#!/bin/bash 

port=$1
jump_host=$2

if [[ -n "$port" && -n "$jump_host" ]]; then
	ssh -o ServerAliveInterval=300 -CfgNT -D $port $jump_host
else
	echo "Usage: " 
	echo "./starttunnel <port> <jump_host>"
fi
