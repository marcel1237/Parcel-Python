#!/usr/bin/env bash
#==============================================================================
# SSQLM Template: Dynamic Project Scaffolder
# Logic: cat_templating_logic.json -> Dynamic Heredocs
#==============================================================================
set -Eeuo pipefail

scaffold_project() {
    local name="${1:-"NewProject"}"
    local author="${2:-"SS QLM Agent"}"
    local version="1.0.0"
    local date
    date=$(date +"%Y-%m-%d")

    mkdir -p "$name/src"

    echo "▶ Scaffolding project: $name..."

    # Notice: Use <<EOF (without quotes) to allow variable expansion
    cat > "$name/README.md" <<EOF
# $name

Generated on: $date
Author: $author
Version: $version

## Description
This project was automatically scaffolded using the SS QLM High-Fidelity logic.

## Usage
\`\`\`bash
./run.sh
\`\`\`
EOF

    # Creation of a script that preserves its own variables
    # We use escaped \$ to keep the variable literal in the output
    cat > "$name/run.sh" <<EOF
#!/usr/bin/env bash
# Project: $name
echo "Starting application..."
CURRENT_DIR=\$(pwd)
echo "Running in \$CURRENT_DIR"
EOF

    chmod +x "$name/run.sh"
    echo "✓ Project $name ready."
}

# Usage Example:
# scaffold_project "MyTool" "Marcel Andrade"
