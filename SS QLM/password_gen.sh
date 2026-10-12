#!/bin/bash
# Secure Password Generator

length=${1:-16}
pass=$(tr -dc 'A-Za-z0-9!@#$%^&*()_+' < /dev/urandom | head -c "$length")
echo "Generated Password: $pass"
