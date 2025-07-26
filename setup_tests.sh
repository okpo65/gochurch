#!/bin/bash
# Simple test environment setup script

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set PYTHONPATH to include the project root
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Change to project directory
cd "$SCRIPT_DIR"

echo "🚀 GoChurch Test Environment Setup"
echo "=================================="
echo "This script will:"
echo "1. Setup test database hosting on port 5433"
echo "2. Run unit tests"
echo "3. Run API tests"
echo ""

# Check if Poetry is available
if command -v poetry &> /dev/null; then
    echo "✅ Using Poetry environment"
    poetry run python scripts/setup_test_environment.py "$@"
else
    echo "⚠️  Poetry not found, using system Python"
    python scripts/setup_test_environment.py "$@"
fi
