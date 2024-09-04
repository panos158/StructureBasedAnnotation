Copyright © 2023-2024 Panagiotis Delaroudis. All Rights Reserved.

# Structure-Based Functional Annotation of Phage Peptides
&nbsp;

The analysis included a small benchmark where ColabFold was decided as the best option. ColabFold was then used for the prediction of the dataset's peptides' structures. The most confident of those was selected and was used as a query with Foldseek to identify structural homologs. A prefiltering step excluded all the statistically insignificant Foldseek. UniProt data was then fetched for the statistically significant ones and their functions were afterwards extracted. These functions were then sorted in descending order with the highest percentage of occurrence appearing at the top.
### **Files**
All final pdb peptide structures from the ColabFold structure prediction process can be found inside the **Structures** folder with the ones up to 100 amino acids long located in the files named after each phage and the ones between 100-150 aa located in the files named after each phage ending with _150. 
&nbsp;

The predicted functions for each peptide along with the percentages of occurrence can be found in the next files:
&nbsp;

1. **0-100_functions** : Contains files with the predicted functions for the peptides up to 100 aa long, along with the target's name, and information about the Foldseek hit, such as evalue, bit score, alignment length and percentage identity.

2. **100-150_functions** : Contains files with the predicted functions for the peptides that are 100-150 aa long, along with the target's name, and information about the Foldseek hit, such as evalue, bit score, alignment length and percentage identity.

3. **0-100_function_percentages** : Contains files with the percentages of occurrence in descending order for the predicted functions of the up to 100 aa long peptides.

4. **100-150_function_percentages** : Contains files with the percentages of occurrence in descending order for the predicted functions of peptides that are 100-150 aa long.

5. **Best_entries**: Contains the most statistically significant Foldseek hit that had the consensus function and the most significant overall hit for each peptide.


### **Benchmark**
**ColabFold** was utilized through the Google Colab infrastructure, found here: ColabFold v1.5.5: AlphaFold2 w/ MMseqs2 BATCH, and **ESMFold** was utilized through the Google Colab server as well. The **Alphafold** job script used for the structure prediction is:


```bash

#!/bin/bash
#PBS -N AlphaFold_script
#PBS -l nodes=1:ppn=8:gpus=1
#PBS -l mem=64gb
#PBS -l walltime=24:00:00

# Loading the appropriate AlphaFold module
module load AlphaFold/2.3.1-foss-2022a-CUDA-11.7.0

# Setting the AlphaFold data directory
export ALPHAFOLD_DATA_DIR=/arcanine/scratch/gent/apps/AlphaFold/20230310	# Should be replaced with the user's actual path or environment variable

# Directory where the input FASTA files are located
FASTA_DIR=/data/leuven/351/vsc35100/Thesis/fasta_sequences3          # Should be replaced with the user's actual path or environment variable

# Output directory for AlphaFold predictions
OUTPUT_DIR=/data/leuven/351/vsc35100/Thesis/New_Alphafold_output     # Should be replaced with the user's actual path or environment variable

# Making sure that the output path exists
mkdir -p ${OUTPUT_DIR}

# Moving to the FASTA directory
cd ${FASTA_DIR}

# Iterating through each FASTA file and running Alphafold
for fasta_file in *.fasta; do
    echo "Currently processing ${fasta_file}..."
     # Creating an output directory for each prediction
    fasta_output_dir=${OUTPUT_DIR}/$(basename ${fasta_file} .fasta)_af_output
    mkdir -p ${fasta_output_dir}

    # Main Alphafold process
    alphafold --fasta_paths=${fasta_file} \
              --max_template_date=2022-01-01 \
              --model_preset=monomer \
              --output_dir=${fasta_output_dir} \
              --db_preset=full_dbs

    echo "${fasta_file} completed. Results in ${fasta_output_dir}"
done

echo "{fasta_file} structure prediction complete. Results saved in ${fasta_output_dir}"


```

### Structure Similarity Search with Foldseek

After structure prediction for the main dataset's peptides was completed, the obtained pdb files were used in the next Foldseek job script:

```bash
#!/bin/bash
#SBATCH --clusters=wice
#SBATCH --job-name=foldseek_run
#SBATCH --output=foldseek_%j.out
#SBATCH --error=foldseek_%j.err
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=24
#SBATCH --mem-per-cpu=4G
#SBATCH --account=account_name      # Shoule be replaced with the account name

# Making sure foldseek path is added to PATH
export PATH=$PATH:/user/leuven/351/vsc35100/foldseek/bin

# Printing the PATH to verify it's properly set
echo "PATH: $PATH"

# Defining directories containing PDB files, the path to the Foldseek database, a temporary directory for Foldseek and the output, these should be replaced with the user's actual paths
PDB_DIR="/scratch/leuven/351/vsc35100/Original"
DB_PATH="/staging/leuven/stg_00144/foldseek_db/af50m_2024mar"          
TMP_DIR="/scratch/leuven/351/vsc35100/tmp_directory"
OUTPUT_DIR="/scratch/leuven/351/vsc35100/Original_foldseek_out"

# Creating output and temporary directories if they don't exist
mkdir -p ${TMP_DIR}
mkdir -p ${OUTPUT_DIR}

# Array of PDB subdirectories which should only contain PDB files
PDB_SUBDIRS=("subdir1" "subdir2" "subdir3" "subdir4")  # Should be replaced with the actual subdirectories

# Iterating through each PDB subdirectory and runing Foldseek, defining the specific outputs we want to see in the end
for subdir in "${PDB_SUBDIRS[@]}"; do
    pdb="${PDB_DIR}/${subdir}"
    output_file="${OUTPUT_DIR}/${subdir}_filtered150_af_out"
    /user/leuven/351/vsc35100/foldseek/bin/foldseek easy-search $pdb $DB_PATH $output_file $TMP_DIR --format-output "query,target,fident,alnlen,mismatch,gapopen,qstart,qend,tstart,tend,evalue,bits,qlen,tlen,prob"
done
```

### Rest of the analysis

The code used for the fetching of the functional data from UniProt, extracting the functions and computing the number of occurences can be found in the folder named **analysis_code**





### References
Mirdita, M., Schütze, K., Moriwaki, Y., Heo, L., Ovchinnikov, S. and Steinegger, M., 2022. ColabFold: making protein folding accessible to all. Nature methods, 19(6), pp.679-682.

Jumper, J., Evans, R., Pritzel, A., Green, T., Figurnov, M., Ronneberger, O., Tunyasuvunakool, K., Bates, R., Žídek, A., Potapenko, A. and Bridgland, A., 2021. Highly accurate protein structure prediction with AlphaFold. nature, 596(7873), pp.583-589.

Rives, A., Meier, J., Sercu, T., Goyal, S., Lin, Z., Liu, J., Guo, D., Ott, M., Zitnick, C.L., Ma, J. and Fergus, R., 2021. Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences. Proceedings of the National Academy of Sciences, 118(15), p.e2016239118.

Lin, Z., Akin, H., Rao, R., Hie, B., Zhu, Z., Lu, W., dos Santos Costa, A., Fazel-Zarandi, M., Sercu, T., Candido, S. and Rives, A., 2022. Language models of protein sequences at the scale of evolution enable accurate structure prediction. BioRxiv, 2022, p.500902.

Van Kempen, M., Kim, S.S., Tumescheit, C., Mirdita, M., Lee, J., Gilchrist, C.L., Söding, J. and Steinegger, M., 2024. Fast and accurate protein structure search with Foldseek. Nature biotechnology, 42(2), pp.243-246.

### VSC acknowledgment 
The resources and services used in this work were provided by the VSC (Flemish Supercomputer Center), funded by the Research Foundation - Flanders (FWO) and the Flemish Government.
