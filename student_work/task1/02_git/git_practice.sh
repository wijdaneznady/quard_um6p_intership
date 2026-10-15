#!/usr/bin/env bash
# Lecture 1 (10 Sep) - Live Git demonstration, steps 1 to 17, on your own fork.
# Run it one block at a time the first time, and read every output.
# Usage: GH_USER=your-github-username bash git_practice.sh
set -euo pipefail
: "${GH_USER:?Set GH_USER to your GitHub username}"
FORK="https://github.com/${GH_USER}/quard_um6p_intership.git"

# Step 1: check that Git is available
which git && git --version

# Step 2-4: parent directory, clone the fork once, enter it
cd ~
if [ ! -d quard_um6p_intership_fork ]; then
  git clone "$FORK" quard_um6p_intership_fork
fi
cd quard_um6p_intership_fork

# Step 5: verify the repository
git status
git remote -v
git log --oneline -5

# Step 6: read the documentation before changing anything
ls; head -n 20 README.md 2>/dev/null || true 2>/dev/null || true

# Step 7: synchronize before working
git pull origin main

# Step 8: create a practice branch (switch to it if it already exists)
git switch -c docs/git-practice 2>/dev/null || git switch docs/git-practice
git branch

# Step 9-10: create a safe student file with useful evidence
mkdir -p student_work
echo "Student Git practice" > student_work/git_practice.txt
{ echo "Repository:"; pwd
  echo "Branch:"; git branch --show-current
  echo "Date:"; date; } >> student_work/git_practice.txt
cat student_work/git_practice.txt

# Step 11: ask Git what changed
git status

# Step 12: stage only the intended file (never 'git add .' here)
git add student_work/git_practice.txt

# Step 13: review exactly what will be committed
git diff --staged

# Step 14: commit with a meaningful message
git commit -m "docs: add student Git practice evidence"

# Step 15: verify the local commit
git log --oneline -3

# Step 16: publish the branch
git push -u origin docs/git-practice

# Step 17: verify local and remote agree
git status
git branch -vv
echo "Now open https://github.com/${GH_USER}/quard_um6p_intership/tree/docs/git-practice"
