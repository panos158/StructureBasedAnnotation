import os
import re
from collections import Counter

# Defining the base directory to the locationg with the functions.txt files
# 'base_dir' should be replaced with the actual base directory
main_dir = 'path_to_main_directory'  
# Defining the output directory where files ending in percentages.txt will be saved
# 'output_dir' should be replaced with the actual output directory
output_dir = 'path_to_output_directory'  
os.makedirs(output_dir, exist_ok=True)

# Creating a list where extracted function names following 'RecName' or 'SubName' are saved
def extract_functions(file_path):
    functions = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('DE'):
                match = re.search(r'(RecName: Full=|SubName: Full=)([^}{]+)', line)
                if match:
                    function = match.group(2).strip()
                    functions.append(function)
    return functions

# Calculating the occurence of each function based on the previously extracted functions and then sorts the percentages in descending order
def save_function_percentages(functions, output_file_path):
    total_count = len(functions)
    function_counts = Counter(functions)
    sorted_functions = sorted(function_counts.items(), key=lambda item: item[1], reverse=True)
    with open(output_file_path, 'w') as file:
        file.write("Function\tPercentage\n")
        for function, count in sorted_functions:
            percentage = (count / total_count) * 100
            file.write(f"{function}\t{percentage:.1f}%\n")

# Iterating through the main directory and processing each _functions.txt file
for root, _, files in os.walk(main_dir):
    for file in files:
        if file.endswith('_functions.txt'):
            file_path = os.path.join(root, file)
            functions = extract_functions(file_path)

            # Creating output file name based on the name of the input file
            input_filename = os.path.basename(file_path)
            percentages_filename = f"{os.path.splitext(input_filename)[0]}_function_percentages.txt"
            percentages_file_path = os.path.join(output_dir, percentages_filename)

            save_function_percentages(functions, percentages_file_path)

print("All files processed and outputs saved.")
