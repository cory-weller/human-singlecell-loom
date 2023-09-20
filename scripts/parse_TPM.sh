#!/usr/bin/env bash
#SBATCH --time 12:00:00
#SBATCH --partition norm
#SBATCH --mem 400G
#SBATCH --nodes 1
#SBATCH --ntasks 20
#SBATCH --gres lscratch:300

## EDIT IF NECESSARY #################################################

# Input h5 object
# h5_object='/path/to/adult_human_20221007.loom'
output_dir=${1}

# Genes of interest filename
# goi_filename='/path/to/goi.txt'
output_dir=${2}

# directory containing TPM files
# TPM_dir='/path/to/TPM/'
output_dir=${3}

# directory to output percentile files
# output_dir='/path/to/GOI_percentiles/'
output_dir=${4}

######################################################################


## Run

module load R/4.2
TMPDIR="/lscratch/${SLURM_JOB_ID}"
[[ -d ${TMPDIR} ]]  || { echo "No slurm job id for lscratch!"; exit 1; }

mkdir -p ${output_dir}

parallel -j 2
Rscript scripts/parse_TPM.R ::: \
    ${h5_object} ::: \
    ${goi_filename} ::: \
    ${TPM_dir} ::: \
    ${TMPDIR} ::: \
    $(seq 1 2)

tar -czvf ${output_dir}/goi_percentiles.tar.gz ${TMPDIR}/pct*.tsv


