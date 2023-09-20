#!/usr/bin/env bash
#SBATCH --mem 40G
#SBATCH --partition norm
#SBATCH --time 8:00:00

module load R/4.2
Rscript parse_h5.R