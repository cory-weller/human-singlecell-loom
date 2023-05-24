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


```bash
wget https://github.com/linnarsson-lab/adult-human-brain/raw/main/scripts/optimize_lda.py
```
```R
# Calculation gene-specific exon lengths
library(GenomicFeatures) 

gtf_filename <- 'gb_pri_annot.gtf'

# Import GTF into R 
txdb <- makeTxDbFromGFF(gtf_filename,format="gtf")

# Build gene-specific exon list
exons.list.per.gene <- exonsBy(txdb,by="gene")

# Calculate intron-removed transcript length table
exonic.gene.sizes <- as.data.frame(sum(width(reduce(exons.list.per.gene))))

dat <- as.data.table(exonic.gene.sizes, keep.rownames=TRUE)
setnames(dat, c('ENSEMBLV', 'LENGTH'))
dat[, ENSEMBL := tstrsplit(ENSEMBLV, '\\.')[1]]

# Convert ENSEMBL to SYMBOL

library(org.Hs.eg.db)


gene_symbols <- select(
                    org.Hs.eg.db, 
                    keys = dat$ENSEMBL,
                    columns = "SYMBOL",
                    keytype = "ENSEMBL"
                )

dat[ENSEMBLV %like% 'PAR', ENSEMBL := ENSEMBLV]

setDT(gene_symbols)
gene_symbols[is.na(SYMBOL), SYMBOL := ENSEMBL]
gene_symbols <- as.data.table(gene_symbols)
gene_symbols <- unique(gene_symbols)

```