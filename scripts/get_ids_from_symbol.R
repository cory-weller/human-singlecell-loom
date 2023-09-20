#!/usr/bin/env Rscript
# in R/4.2

library(data.table)
library(org.Hs.eg.db)
library(GenomicFeatures)


gtf_filename <- '/fdb/cellranger/refdata-gex-GRCh38-2020-A/genes/genes.gtf'



# Import GTF into Rm takes a min or two
txdb <- makeTxDbFromGFF(gtf_filename,format="gtf")

genes <- genes(txdb)
genes <- as.data.table(genes)
setnames(genes, 'gene_id', 'ENSEMBL')

# Make table of ENSG and SYMBOL
ids <- select(
                    org.Hs.eg.db,
                    keys = genes$ENSEMBL,
                    columns = "SYMBOL",
                    keytype = "ENSEMBL"
                )

# convert to data.table
setDT(ids)

genes <- merge(genes, ids, by='ENSEMBL')

# restructure
setkey(genes, seqnames, start, end)
setcolorder(genes, c('SYMBOL','ENSEMBL','seqnames','start','end','width','strand'))

# output
fwrite(genes, file='gene_table_GRCh38-2020-A.tsv', sep='\t')