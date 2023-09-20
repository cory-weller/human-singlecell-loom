#!/usr/bin/env bash
#SBATCH --mem 40G
#SBATCH --partition norm
#SBATCH --time 8:00:00


# Purge existing modules
module purge


# Testing for arg 1, input h5 file
## use realpath just in case
INFILE=$(realpath ${1})
[[ -f ${INFILE} ]] && echo "INFO: input h5 file is ${INFILE}" || { echo "ERROR: ${INFILE} does not exist"; exit 1; }
[[ -r ${INFILE} ]]  || { echo "ERROR: ${INFILE} is not readable"; exit 1; }


# Testing for arg 2, output directory
OUTDIR=${2}
## Create ${OUTDIR} if does not exist
echo "INFO: output directory is ${OUTDIR}"
[[ ! -d ${OUTDIR} ]] && mkdir -p ${OUTDIR} 
[[ -d ${OUTDIR} ]] || { echo "ERROR: Could not create ${OUTDIR}" exit 1; }
## Exit if ${OUTDIR} is not writable
[[ -w ${OUTDIR} ]] || { echo "ERROR: ${OUTDIR} is not writable" exit 1; }
## use realpath just in case
OUTDIR=$(realpath ${OUTDIR})


# Load R/4.2 and run script
module load R/4.2
echo -e "\n\n"
echo "INFO: Running command: Rscript scripts/parse_h5.R ${INFILE} ${OUTDIR}"
echo -e "\n\n"
Rscript scripts/parse_h5.R ${INFILE} ${OUTDIR}
