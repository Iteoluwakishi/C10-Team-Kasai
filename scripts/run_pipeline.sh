#!/bin/bash
set -e

echo "======================================"
echo " Starting NTA/NTAA Processing Pipeline"
echo "======================================"

# Ensure we are in the project root directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "1. Creating metadata..."
python3 scripts/create_metadata.py

echo "2. Running extraction..."
python3 scripts/deliverable.py

echo "3. Running cleaning and chunking..."
python3 scripts/clean_and_chunk.py

echo "4. Running validation..."
python3 scripts/validate.py

echo "5. Generating progress report..."
python3 scripts/progress.py

echo "======================================"
echo " Pipeline execution completed successfully!"
echo " Final JSONL datasets are in data/processed/current/"
echo "======================================"
