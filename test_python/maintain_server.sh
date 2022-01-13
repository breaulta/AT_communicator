#!/bin/bash
# Respawns main.py unless a graceful exit code is received.

until sudo python main.py; do
	echo "Server main.py crashed with exit code $?. Respawning..." >&2
	sleep 1
done
