#!/usr/bin/env bash
#==============================================================================
# SSQLM Template: High-Performance String Engine
# Logic: string_manipulation_precision.json
#==============================================================================
set -Eeuo pipefail

# Extraordinary String Processor
process_path_logic() {
    local full_path="$1"

    echo "▶ Analyzing path: $full_path"

    # 1. Get Directory (Simulating dirname)
    local dir_name="${full_path%/*}"

    # 2. Get Filename (Simulating basename)
    local base_name="${full_path##*/}"

    # 3. Get Extension
    local ext="${base_name##*.}"

    # 4. Get Filename without extension
    local raw_name="${base_name%.*}"

    cat <<EOF
Summary:
  Dir:  $dir_name
  File: $base_name
  Ext:  $ext
  Name: $raw_name
EOF
}

# String Sanitizer (Slugifier)
create_slug() {
    local input="$1"
    local slug

    # Convert to lowercase
    slug="${input,,}"

    # Replace spaces with hyphens
    slug="${slug// /-}"

    # Remove special characters (basic example)
    slug="${slug//[^a-zA-Z0-9-]/}"

    echo "$slug"
}

# Example Usage
# process_path_logic "/opt/ssqlm/source/core.logic.sh"
# create_slug "Extraordinary Shell Model v1.0!"
