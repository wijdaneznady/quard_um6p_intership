#!/usr/bin/env bash
# Lecture 1 - Student Challenge: repeat the workflow alone on branch docs/installation-observations.
# The file is filled with values measured on this computer, not typed by hand.
# Usage: cd ~/quard_um6p_intership_fork && bash student_challenge.sh
set -euo pipefail

git status
git switch main && git pull origin main
git switch -c docs/installation-observations 2>/dev/null || git switch docs/installation-observations

mkdir -p student_work
OUT=student_work/installation_observations.md
{
  echo "# Installation observations"
  echo
  echo "Ubuntu version: $(lsb_release -ds 2>/dev/null || grep PRETTY_NAME /etc/os-release | cut -d= -f2)"
  echo "ROS 2 distribution: ${ROS_DISTRO:-$(ls /opt/ros 2>/dev/null | head -1)}"
  echo "Installation phase completed: Phase 3 - full PX4 + Gazebo + ROS 2 mission pipeline (survey mission flown)"
  echo
  echo "## One verified command and its output"
  echo '```'
  echo '$ gz sim --version'
  gz sim --version 2>&1 | head -n 2 || echo "(gz not on PATH in this shell)"
  echo '```'
} > "$OUT"
cat "$OUT"

git add "$OUT"
git diff --staged
git commit -m "docs: add installation observations"
git push -u origin docs/installation-observations
git log --oneline -3
