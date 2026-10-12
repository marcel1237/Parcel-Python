#!/usr/bin/env bash
#==============================================================================
# SSQLM Template: Surgical Code Patcher
# Logic: robust_io.json -> Surgical Patching
#==============================================================================
set -Eeuo pipefail

# patch_block: Injects new content between two markers in a file
patch_block() {
    local target="$1"
    local start_marker="$2"
    local end_marker="$3"
    local temp_patch
    temp_patch=$(mktemp)

    if [[ ! -f "$target" ]]; then
        echo "❌ Error: Target file $target not found."
        return 1
    fi

    # 1. Copy until start marker
    sed -n "1,/$start_marker/p" "$target" > "$temp_patch"

    # 2. Inject new content from standard input (via CAT)
    cat >> "$temp_patch"

    # 3. Copy from end marker to end of file
    sed -n "/$end_marker/,\$p" "$target" >> "$temp_patch"

    # 4. Atomic swap
    mv "$temp_patch" "$target"
    echo "✓ File $target patched successfully between $start_marker and $end_marker."
}

# Usage Example:
# patch_block "src/App.cpp" "// AI_START" "// AI_END" <<'EOF'
#     void new_autonomous_logic() {
#         printf("Action executed by Agent\n");
#     }
# EOF
