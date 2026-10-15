#!/usr/bin/env bash
# Lecture 1 (10 Sep) - "Project Exercise" boxes, applied to the internship repository.
# Only creates and edits files inside student_work/. Nothing in PX4, Gazebo or ROS 2 is changed.
# Usage: bash project_exercises.sh   (from anywhere)
set -euo pipefail

REPO="${REPO:-$HOME/quard_um6p_intership}"

# Chain with && : nothing below runs if the cd fails (slide 53).
cd "$REPO" && pwd && ls gazebo/models

# Navigation and listing (slides 42-45)
ls -la "$REPO" | head -n 15

# Create files and directories (slide 46)
mkdir -p student_work/logs
touch student_work/observations.txt

# Copy and move safely (slide 47)
cp config/project.env student_work/project.env.backup
mv student_work/observations.txt student_work/day1_notes.txt

# Remove with care: practise only in a throw-away folder (slide 48)
mkdir -p ~/bash_practice_remove && cd ~/bash_practice_remove
touch temporary.txt && ls
pwd && rm temporary.txt && ls
cd "$REPO"

# Read text files (slide 50)
head -n 20 config/project.env
[ -f README.md ] && head -n 15 README.md

# Produce output and keep a record (slide 51)
echo "Day 1 terminal verification" > student_work/run.log
date >> student_work/run.log
pwd >> student_work/run.log
ls -la >> student_work/run.log
echo "Inspection complete" >> student_work/run.log
tail -n 5 student_work/run.log

# Find files and search their content (slide 52)
find . -name "package.xml" -not -path "*/dependencies/*" | head
find gazebo/models -name "model.sdf"
grep -Rni "camera" docs 2>/dev/null | head || true

# Environment variables (slides 54-55)
source config/project.env
echo "ROS_DISTRO=${ROS_DISTRO:-not set}"
env | grep -E "^(ROS_|PX4_|GZ_)" | sort | tee -a student_work/run.log

# Permissions (slide 56): make our own script executable, check the result
chmod +x student_work/*.sh 2>/dev/null || true
ls -l student_work

# Processes (slide 59): look at running simulation programs without killing anything
ps -eo pid,etime,args | grep -E "px4|gz sim|MicroXRCE" | grep -v grep || echo "no simulation running"

echo "Project exercises done. Evidence in student_work/run.log"
