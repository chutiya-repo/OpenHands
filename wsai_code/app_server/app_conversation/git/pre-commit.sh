#!/bin/bash
# This hook was installed by WSAI CODE
# It calls the pre-commit script in the .wsai_code directory

if [ -x ".wsai_code/pre-commit.sh" ]; then
    source ".wsai_code/pre-commit.sh"
    exit $?
else
    echo "Warning: .wsai_code/pre-commit.sh not found or not executable"
    exit 0
fi
