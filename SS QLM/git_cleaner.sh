#!/bin/bash
# Remove local branches that were already merged into main

main_branch="main"
git checkout $main_branch
git branch --merged | grep -v "\*" | grep -v "$main_branch" | xargs -n 1 git branch -d
echo "Cleanup complete."
