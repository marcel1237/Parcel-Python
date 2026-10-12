#!/usr/bin/env bash
#==============================================================================
# SSQLM Template: Safe Docker Environment Setup
# Logic: container_quality.json -> Safe Secret Injection & Isolation
#==============================================================================
set -Eeuo pipefail

setup_container_env() {
    local env_file=".env.local"
    local container_name="parcel-dev-env"
    local image="ubuntu:22.04"

    echo "▶ Preparing secure environment..."

    # Use SSQLM Atomic Pattern to create env file if missing
    if [[ ! -f "$env_file" ]]; then
        cat > "$env_file" <<'EOF'
DEBUG_MODE=true
API_PORT=8080
# DO NOT COMMIT SECRETS TO VCS
DB_PASSWORD=ssqlm_dev_pass
EOF
        chmod 600 "$env_file"
    fi

    echo "▶ Launching isolated container: $container_name"

    # Run with standard SSQLM flags:
    # --rm (clean up), -v (mount project), --env-file (safe secrets)
    docker run --rm -it \
        --name "$container_name" \
        -v "${PWD}:/app" \
        -w /app \
        --env-file "$env_file" \
        "$image" bash
}

# Example Usage
# setup_container_env
