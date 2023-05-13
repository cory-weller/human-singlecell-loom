#!/usr/bin/env bash
#SBATCH --mem 20G
#SBATCH --ntasks 1
#SBATCH --nodes 1
#SBATCH --partition norm
#SBATCH --time 10:00:00

module load python/3.9
python -u parse_loom.py