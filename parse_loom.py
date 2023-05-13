#!/usr/bin/env python

import numpy as np
import sys
import scipy
from scipy import stats
import h5py

n_chunks = 1000
goi_filename = 'genes_of_interest.tsv'
loom_obj='/data/CARD_AA/projects/2022_10_CA_singlecell_humanbrain/data/adult_human_20221007.loom'
out_filename = 'goi_percentiles.tsv'


# 59480 genes
# 3369219 cells
# I use h5py to read the datasets because loom is stupid

def get_chunk(ds, idx_start, idx_end):
    # p represents the nth percent of the matrix
    return(ds[:, idx_start : idx_end])


def get_goi_percentiles(sample_expression_array, genes_of_interest):
    output = []
    for gene in genes_of_interest:
        idx = genes_of_interest[gene]
        goi_expression = sample_expression_array[idx]
        goi_percentile = scipy.stats.percentileofscore(sample_expression_array, goi_expression, kind='strict')
        output.append(int(goi_percentile))
    return([str(x) for x in output])


# Import genes of interest
genes_of_interest = {}
with open('genes_of_interest.tsv', 'r', encoding='utf-8') as infile:
    for line in infile:
        gene, ensembl = line.strip().split('\t')
        genes_of_interest[gene] = ensembl


# Load row and column names from h5
with(h5py.File(loom_obj, 'r')) as f:
    cell_ids = [x.decode() for x in f['col_attrs/CellID'][:]]
    gene_ids = [x.decode() for x in f['row_attrs/Gene'][:]]

total_cols = len(cell_ids)
chunk_size = int(np.floor(total_cols / float(n_chunks)))
chunk_vals = [(chunk_size*i, chunk_size*(i+1)) for i in range(0, n_chunks+1)]

# Get vector of gene indices for GOI
indices = {}
for gene in genes_of_interest:
    idx = np.where(np.array(gene_ids) == gene)[0][0]
    indices[gene] = int(idx)


# build header for output file
header = ['CellID'] + [goi for goi in genes_of_interest]

with(h5py.File(loom_obj, 'r')) as f:
    with open(out_filename, 'w') as out:
        out.write('\t'.join(header)+'\n')
        for start, stop in chunk_vals:
            print(f"loading chunk from {start} to {stop}", flush=True)
            chunk = f['matrix'][:, start:stop]
            chunk = list(np.transpose(chunk))
            chunk_out = ''
            for i, cell_array in enumerate(chunk):
                cell_id = cell_ids[i + start]
                o = [cell_id]
                o += get_goi_percentiles(cell_array, indices)
                chunk_out += ('\t'.join(o)+'\n')
            out.write(chunk_out)
