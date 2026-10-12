#!/usr/bin/env bash
#==============================================================================
# SSQLM Template: Idempotent Configuration Appender
# Logic: cat_safety_and_rollback.json -> The 'Cat-Guard' Check
#==============================================================================
set -Eeuo pipefail

append_unique_block() {
    local target="$1"
    local unique_identifier="$2" # A string that only exists in this block

    echo "▶ Checking for existing configuration in $target..."

    if grep -q "$unique_identifier" "$target" 2>/dev/null; then
        echo "ℹ Configuration already exists. Skipping."
    else
        echo "▶ Appending new configuration block..."
        cat >> "$target" <<EOF

# --- BEGIN $unique_identifier ---
# Added via SS QLM Idempotent Patcher
export PATH="\$PATH:/opt/ssqlm/bin"
alias ssqlm-check='bash /opt/ssqlm/tools/verify.sh'
# --- END $unique_identifier ---
EOF
        echo "✓ Success: Configuration added."
    fi
}

# Usage Example:
# append_unique_block "$HOME/.bashrc" "SSQLM_TOOLS_V1"
