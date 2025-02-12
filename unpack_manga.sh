#!/usr/bin/env bash

# Use this script if you have all one piece volumes bundled into "zip" files.

# List all .cbz files
readarray -d '' files < <(find . -type f -name '*.cbz' -print0)

# Loop over each file
for file in "${files[@]}"; do
    # Extract the volume number (v001, v002, etc.)
    volume=$(echo "$file" | sed -E 's/.*v([0-9]{3}).*/\1/')

    # Create the directory for that volume if it doesn't exist
    mkdir -p "v$volume"
    
    # Unpack the cbz file (treat as a zip file0)
    unzip "$file" -d "data/v$volume/"
    
    echo "Unpacked $file into v$volume/"
done
