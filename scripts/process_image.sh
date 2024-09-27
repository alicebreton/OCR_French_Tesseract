#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_folder> <output_folder>"
    exit 1
fi

input_folder="$1"
output_folder="$2"

if [ ! -d "$output_folder" ]; then
    mkdir -p "$output_folder"
fi

log_file="$output_folder/process_log.logs"

python3 ./scripts/process_image.py "$input_folder" "$output_folder"

input_file_count=$(ls -1q "$output_folder"/*_processed.jpg | wc -l)

echo "Processing started at $(date)" > "$log_file"
echo "Number of files to process: $input_file_count" >> "$log_file"

for input_image in "$output_folder"/*_processed.jpg; do
    if [[ -f "$input_image" ]]; then
        echo "Processing $input_image" >> "$log_file"
        base_name=$(basename "$input_image" _processed.jpg)
        
        output_file="$output_folder/${base_name}"
        
        tesseract "$input_image" "$output_file" -l fra &>> "$log_file"
        
        echo "Processed $input_image -> ${output_file}.txt" >> "$log_file"
    fi
done

output_file_count=$(ls -1q "$output_folder"/*.txt | wc -l)

# End logging
echo "Number of processed files: $output_file_count" >> "$log_file"
echo "Processing complete at $(date)" >> "$log_file"

# Echo the counts to the console
echo "Number of files to process: $input_file_count"
echo "Number of processed files: $output_file_count"
