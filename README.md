# README

Contains code used to interface with the `loom` object (subclass of
`h5`) for calculating expression percentile scores for genes of interest
(GOI). `loom` object link available [here](https://github.com/linnarsson-lab/adult-human-brain).

GTF was retrieved from google storage:
```bash
if [ ! -f 'gb_pri_annot.gtf' ]; then
    wget https://storage.googleapis.com/linnarsson-lab-tmp/gb_pri_annot.gtf
fi
```

## Convert feature counts to TPM
This is already done on Biowulf, and does not need to be done again.
```bash
sbatch parse_h5.slurm
```

## Calculate expression percentiles for genes of interest
You will want to add a text file containing genes of interest, one gene symbol per line.

Then edit [`parse_TPM.slurm`](parse_TPM.slurm) to point to the correct files.
- `h5_object` is the adult human brain `.loom` file
- `goi_filename` is a text file containing gene symbols, one per line, for genes of interest
- `TPM_dir` is the directory containing preprocessed TPM files
- `output_dir` is the directory to output percentile files.

Lastly, submit the job array:
```bash
# Submit 673 jobs (batches of 5000 cells), max 20 at a time
sbatch --array=1-673%20 parse_TPM.slurm
```
