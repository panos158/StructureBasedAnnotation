import os
import re

# Defining the base directory containing all query folders for each phage peptide for a particular phage. The UniProt data files are inside each of those folders.
# 'base_dir' should be replaced with the actual base directory containing the query folders
base_dir = 'path_to_query_folders'  

# Defining the output directory where files ending in functions.txt will be saved
# 'output_dir' should be replaced with the actual output directory
output_dir = 'path_to_output_directory'  
os.makedirs(output_dir, exist_ok=True)  

# Creating a list of all subdirectories inside the base directory where all the UniProt files are located
query_dirs = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

# Function reading function descriptions from UniProt data files and retaining evalue, bit score, alignment length and percentage identity
def read_function_descriptions(file_path):
    descriptions = []
    current_accession = None
    current_info = []
    bit_score_added = False
    evalue_added = False
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('==='):
                if current_accession:
                    descriptions.append('\n'.join(current_info))
                current_accession = line.strip()
                current_info = [current_accession]
                bit_score_added = False
                evalue_added = False
            elif line.startswith('DE'):
                current_info.append(line.strip())
            elif line.startswith('Bit') and not bit_score_added:
                current_info.append(line.replace("Bit score:", "Bit Score:").strip())
                bit_score_added = True
            elif line.startswith('E-value') and not evalue_added:
                current_info.append(line.strip())
                evalue_added = True
            elif line.startswith('Alignment Length'):
                current_info.append(line.strip())
            elif line.startswith('Percentage Identity'):
                current_info.append(line.strip())
    
    if current_accession:
        descriptions.append('\n'.join(current_info))
    
    return descriptions

# Function saving the data into a functions.txt file which contains both the functions for the Foldseek hits and the other relevant data that was retained
def save_summary(data, file_path):
    with open(file_path, 'w') as file:
        for entry in data:
            file.write(f"{entry}\n\n")

# Iterating through each query directory
for query_dir in query_dirs:
    function_descriptions = []
    
    # Iterating through each target file inside the query directory
    for target_file in os.listdir(query_dir):
        if target_file.endswith('.txt'):
            file_path = os.path.join(query_dir, target_file)
            function_descriptions.extend(read_function_descriptions(file_path))
    
    # Saving the summary to functions.txt files
    query_name = os.path.basename(query_dir).split('.')[0]
    summary_file_path = os.path.join(output_dir, f"{query_name}_functions.txt")
    save_summary(function_descriptions, summary_file_path)

print(" Functions have been saved to the specified output directory.")
