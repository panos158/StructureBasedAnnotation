import pandas as pd
import requests
import time
import os

# Function fetching the UniProt data
def fetch_uniprot_data(accession):
    url = f"https://www.uniprot.org/uniprot/{accession}.txt"
    response = requests.get(url)
    if response.ok:
        return response.text
    else:
        return None

# Function extracting the accessions
def extract_accession(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('==='):
                return line.strip().split()[1]

# List of input files containing the Foldseek hits for the peptides of each phage and corresponding output directories where each Foldseek hit's UniProt fetched data will be saved 
# 'input_directory_path' and 'output_directory_path' should be replaced with the actual paths 
inputs_outputs = [
    ("input_directory_path/first_phage_Foldseek_results.txt", "output_directory_path/first_phage_uniprot_data"),
    ("input_directory_path/second_phage_Foldseek_results.txt", "output_directory_path/second_phage_uniprot_data")
]

# Iterating through each file and output directory pair
for input_file, output_subdir in inputs_outputs:
    # Loading the data from the input file
    data = pd.read_csv(input_file, sep='\t', usecols=["query", "target", "bits", "evalue", "alnlen", "fident"])

    # Making the full output path by by connecting the base path with each phage's specific subdirectory
    output_dir = os.path.join('output_directory_path', output_subdir)
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory has been created: {output_dir}")

    # Processing each unique query peptide from the Foldseek hits, filtering the data so that only those regarding the peptide currently being processed are included and sorting the data based on higher bit score and lower evalue.
    for query_protein in data['query'].unique():
        relevant_data = data[data['query'] == query_protein]
        # Sorting by bit score in descending order and after by e-value in ascending order
        sorted_hits = relevant_data.sort_values(by=['bits', 'evalue'], ascending=[False, True])

        # Printing the sorted Foldseek hits
        print(f"Sorted Foldseek hits for query {query_protein}:")
        print(sorted_hits)

        # Creating a directory for each specific currently processed peptide
        query_output_dir = os.path.join(output_dir, query_protein.replace('|', '_'))
        os.makedirs(query_output_dir, exist_ok=True)
        print(f"Query output directory has been successfully created: {query_output_dir}")

        # Retrieving and saving the UniProt data for each target protein (Foldseek hit)
        for _, row in sorted_hits.iterrows():
            target_protein = row['target']
            bits = row['bits']
            evalue = row['evalue']
            alnlen = row['alnlen']
            fident = row['fident']
            accession = target_protein.split('-')[1] if '-' in target_protein else None
            if accession:
                print(f"Fetching data for {accession}")
                try:
                    uniprot_data = fetch_uniprot_data(accession)
                    target_file_path = os.path.join(query_output_dir, f"{accession}.txt")
                    with open(target_file_path, 'w') as file:
                        if uniprot_data:
                            file.write(f"=== {accession} ===\n")
                            file.write(f"Bit score: {bits}\nE-value: {evalue}\n")
                            file.write(f"Alignment Length: {alnlen}\n")
                            file.write(f"Percentage Identity: {fident}\n")
                            file.write(f"{uniprot_data}\n")
                        else:
                            file.write(f"=== {accession} ===\n")
                            file.write(f"Bit score: {bits}\nE-value: {evalue}\n")
                            file.write(f"Alignment Length: {alnlen}\n")
                            file.write(f"Percentage Identity: {fident}\n")
                            file.write("Data not found\n")
                    time.sleep(1)  
                except Exception as e:
                    print(f"Error in retrieving UniProt data for {accession}: {e}")
                    with open(os.path.join(query_output_dir, 'error_log.txt'), 'a') as log_file:
                        log_file.write(f"Error fetching data for {accession}: {e}\n")

print("All data has been processed and saved ")
