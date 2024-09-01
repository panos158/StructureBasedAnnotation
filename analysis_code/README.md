
**retrieve_uniprot_data.py**
&nbsp;

This script processes Foldseek result files and does the following:

1. Loads Foldseek results and processes them to identify and sort hits based on bit score and e-value.
2. Retrieves UniProt data for the identified hits (target proteins) corresponding to each peptide.
3. Saves the UniProt data along with other relevant statistics such as bit score, e-value, alignment length, and percentage identity into text files, organized in directories specific to each query peptide.


**function_data_extractor.py**
&nbsp;

This script processes the previously obtained UniProt data files: 

1. The script goes through the appropriate query directories and processes each file.

2. It extracts the functions along with relevant statistics (bit score, e-value, alignment length, and percentage identity) found in the UniProt data files for each Foldseek target hit.
 
2. It saves the extracted data into separate functions.txt files for each peptide in a specified output folder. 



**calculate_function_percentages.py**
&nbsp;

This script processes the previously obtained files with the extracted functions:

1.  It looks in the specified directories for files ending in _functions.txt.

2. It extracts the function names and then computes the frequency of each function as a percentage of the total number of functions. 

3. The results are saved in new files, ending with the added "_function_percentages.txt" to the original file names, in the appropriate output directory.
