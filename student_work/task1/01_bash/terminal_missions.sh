#!/usr/bin/env bash
# Lecture 1 (10 Sep) - Terminal Sandbox, Missions 1 to 3.
# Runs in a throw-away folder so it can never touch the project.
# Usage: bash terminal_missions.sh
set -euo pipefail

SANDBOX="$(mktemp -d)"
cd "$SANDBOX"
echo "Sandbox: $SANDBOX"

echo "== Mission 1: the workspace =="
pwd                    # 1. print the current working directory
ls -la                 # 2. list the existing files
mkdir drone_ws         # 3. create the workspace folder
cd drone_ws            # 4. move inside it
ls -la                 # 5. verify it is empty (only . and ..)

echo "== Mission 2: configuration files =="
echo "ROS_DOMAIN_ID=42" > config.env   # 1. create the file with echo + redirection
cat config.env                         # 2. read it back
mkdir backup                           # 3. backup folder
cp config.env backup/                  # 4. copy the file
ls backup/

echo "== Mission 3: system administration =="
mv backup archive                      # 1. rename backup -> archive
ls
grep "ROS" archive/config.env          # 2. search for ROS in the archived file
# 3. clean up. Before any rm: check where we are and what we delete.
pwd && ls archive
rm -rf archive/
ls

cd / && rm -rf "$SANDBOX"
echo "Sandbox removed. Missions 1-3 completed."
