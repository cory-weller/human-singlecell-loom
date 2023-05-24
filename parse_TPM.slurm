#!/usr/bin/env bash
#SBATCH --time 0:59:00
#SBATCH --partition quick,norm
#SBATCH --mem 20G
#SBATCH --nodes 1
#SBATCH --ntasks 1

module load R/4.2

Rscript parse_TPM.R



