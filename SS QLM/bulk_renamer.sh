#!/bin/bash
# Bulk Rename Files (Prefix addition)

PREFIX="v1_"
for file in *; do
    if [[ -f "$file" ]]; then
        mv "$file" "${PREFIX}${file}"
        echo "Renamed: $file -> ${PREFIX}${file}"
    fi
done
