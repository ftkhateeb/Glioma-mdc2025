#!/bin/bash

INPUT_DIR_TRAIN="/home/aelkhate/anaconda3/envs/glioma-prep/Glioma-mdc2025/data/original_data/train"  
INPUT_DIR_TEST="/home/aelkhate/anaconda3/envs/glioma-prep/Glioma-mdc2025/data/original_data/test"               # Folder containing your JSON files
 
OUTPUT_DIR_TRAIN="/home/aelkhate/anaconda3/envs/glioma-prep/Glioma-mdc2025/data/original_data_fixed/train"  # Where all PNGs and JSONs will be saved
OUTPUT_DIR_TEST="/home/aelkhate/anaconda3/envs/glioma-prep/Glioma-mdc2025/data/original_data_fixed/test"  # Where all PNGs and JSONs will be saved

mkdir -p "$OUTPUT_DIR_TEST"

for json_file in "$INPUT_DIR_TEST"/*.json; do
    base_name=$(basename "$json_file" .json)
    temp_dir="./temp_${base_name}_json"

    echo "Processing $json_file..."
    labelme_json_to_dataset "$json_file" -o "$temp_dir"

    # Copy and rename the image
    cp "$temp_dir/img.png" "$OUTPUT_DIR_TEST/${base_name}.png"

    # Copy the original JSON
    cp "$json_file" "$OUTPUT_DIR_TEST/${base_name}.json"

    # Clean up temp folder
    rm -r "$temp_dir"
done