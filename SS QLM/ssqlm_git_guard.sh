#!/usr/bin/env bash
#==============================================================================
# SSQLM Template: Git Branch Guard
# Logic: git_workflow_quality.json -> Main Branch Immunity
#==============================================================================
set -Eeuo pipefail

verify_git_safety() {
    local protected_branch="main"
    local current_branch

    current_branch=$(git branch --show-current)

    echo "▶ Validating Git state on branch: $current_branch"

    if [[ "$current_branch" == "$protected_branch" ]]; then
        echo "❌ FATAL: Direct modification to '$protected_branch' is prohibited by SSQLM standards."
        echo "💡 Please create a feature branch: git checkout -b feat/your-feature"
        exit 1
    fi

    echo "▶ Checking for sensitive files..."
    local leaks
    leaks=$(find . -maxdepth 1 -name "*.env" -o -name "*.key" -o -name "*.pem")

    if [[ -n "$leaks" ]]; then
        echo "⚠️ WARNING: Potential credential leaks detected:"
        echo "$leaks"
        echo "💡 Ensure these are in .gitignore"
    fi

    echo "✓ Environment ready for commit."
}

# Example Usage
# verify_git_safety
