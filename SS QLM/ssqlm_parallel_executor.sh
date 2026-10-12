#!/usr/bin/env bash
#==============================================================================
# SSQLM Template: Safe Parallel Executor
# Logic: parallel_processing.json -> Bounded Background Tasks
#==============================================================================
set -Eeuo pipefail

# Extraordinary Parallel Loop
run_parallel_tasks() {
    local max_jobs="${1:-4}"
    local task_list=("item1" "item2" "item3" "item4" "item5" "item6" "item7" "item8")

    echo "▶ Starting batch processing (Limit: $max_jobs concurrent)..."

    for item in "${task_list[@]}"; do
        # Check current running jobs
        # Wait for any job to finish if limit is reached
        while [[ $(jobs -p | wc -l) -ge $max_jobs ]]; do
            wait -n 2>/dev/null || sleep 0.1
        done

        # Dispatch task to background
        (
            echo "  [TASK] Processing $item (PID: $$)..."
            sleep $((RANDOM % 3 + 1)) # Simulate work
            echo "  [DONE] Finished $item"
        ) &
    done

    # Wait for remaining jobs
    echo "▶ Finalizing remaining tasks..."
    wait
    echo "✓ All tasks completed successfully."
}

# Example Usage
# run_parallel_tasks 3
