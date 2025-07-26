#!/bin/bash
# Simple test runner with proper Python path

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set PYTHONPATH to include the project root
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Change to project directory
cd "$SCRIPT_DIR"

# Run the Python test script with all arguments passed through
python scripts/run_tests.py "$@"
