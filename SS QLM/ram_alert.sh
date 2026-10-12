#!/bin/bash
# Alert if memory usage is above 90%

threshold=90
current=$(free | grep Mem | awk '{print $3/$2 * 100.0}' | cut -d. -f1)

if [ "$current" -gt "$threshold" ]; then
    echo "CRITICAL: RAM usage at ${current}%!"
    # Add notification or email command here
fi
