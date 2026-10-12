#!/bin/bash
# Basic System Health Monitor

echo "--- System Report ---"
echo "Date: $(date)"
echo "Uptime: $(uptime -p)"
echo "Memory Usage:"
free -h | grep -E "Mem|Total"
echo "Disk Usage:"
df -h | grep '^/dev/'
echo "Top Processes:"
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head -n 6
