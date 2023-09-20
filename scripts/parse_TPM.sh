#!/usr/bin/env bash
#SBATCH --time 0:29:00
#SBATCH --partition quick,norm
#SBATCH --mem 20G
#SBATCH --nodes 1
#SBATCH --ntasks 1


## EDIT IF NECESSARY #################################################

# Input h5 object
h5_object='/data/CARD_AA/users/wellerca/data/adult_human_20221007.loom'

# Genes of interest filename
goi_filename='goi-2.txt'

# directory containing TPM files
TPM_dir='/data/CARD_AA/users/wellerca/data/'

# directory to output percentile files
output_dir='/data/CARD_AA/users/wellerca/goi_percentiles/'

######################################################################


## Run

module load R/4.2

mkdir -p ${output_dir}
N=${SLURM_ARRAY_TASK_ID}

Rscript parse_TPM.R \
    ${h5_object} \
    ${goi_filename} \
    ${TPM_dir} \
    ${output_dir} \
    ${N}


