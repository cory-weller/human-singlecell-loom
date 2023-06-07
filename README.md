# README

Contains code used to interface with the `loom` object (subclass of
`h5`) for calculating expression percentile scores for genes of interest
(GOI). `loom` object link available [here](https://github.com/linnarsson-lab/adult-human-brain).

GTF retrieved from google storage:
```bash
if [ ! -f 'gb_pri_annot.gtf' ]; then
    wget https://storage.googleapis.com/linnarsson-lab-tmp/gb_pri_annot.gtf
fi
```

## Convert feature counts to TPM
```bash
sbatch parse_h5.slurm
```

## Calculate expression percentiles for genes of interest
```bash
sbatch parse_TPM.slurm
```
