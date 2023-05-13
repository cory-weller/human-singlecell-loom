# README

Contains code used to interface with the `loom` object (subclass of
`h5`) for calculating expression percentile scores for genes of interest
(GOI).


`sbatch` [`submit.sh`](submit.sh) submits job that runs the python
script [`parse_loom.py`](parse_loom.py). Requires input of genes of 
interest [`genes_of_interest.tsv`](genes_of_interest.tsv).

Python interfaces with `loom` object using `h5py`, counting the number
of columns in the `matrix` dataset, then making 1001 chunks for iterating.
For 3369219 cells, that's 1000 chunks of 3369, plus one smaller chunk
finishing off the remainder.

Job completed on Biowulf HPC in ~8 hours with peak of ~4 GB memory.
SLURM output saved as [`slurm-65497588.out`](slurm-65497588.out)

Output percentile counts saved as `goi_percentiles.tsv` which was
manually `gzipped` after completion.

[`make_sparse.py`](make_sparse.py) contains code for generating a
`MatrixMarket` format sparse matrix, though it wasn't used here because
it barely reduced file size anyway.
