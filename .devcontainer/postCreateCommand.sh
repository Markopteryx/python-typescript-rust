#!/bin/bash

# Base directory
base_dir="/workspaces/python-typescript-rust"

# Define directories for npm install
npm_dirs=(
    "$base_dir/typescript"
)

# Execute npm install in each directory
for dir in "${npm_dirs[@]}"; do
    cd "$dir" && npm install &
done

# Execute poetry update in specific directories
cd "$base_dir/python" && poetry update &

# Wait for all background jobs to complete
wait