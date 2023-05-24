#!/usr/bin/env python

import gzip
import numpy as np
import sys
import scipy
from scipy import stats
import h5py
import os
import glob
import pandas as pd

goi_filename = 'genes_of_interest.tsv'
loom_obj='/data/CARD_AA/projects/2022_10_CA_singlecell_humanbrain/data/adult_human_20221007.loom'
out_filename = 'goi_percentiles.tsv'
file_dir = '/data/CARD_AA/users/wellerca/data/'


# 59480 genes
# 3369219 cells




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

ensembl_goi = [genes_of_interest[x] for x in genes_of_interest]
symbol_goi = [x for x in genes_of_interest]


# Load row and column names from h5
with(h5py.File(loom_obj, 'r')) as f:
    cell_ids = [x.decode() for x in f['col_attrs/CellID'][:]]
    gene_ids = [x.decode() for x in f['row_attrs/Gene'][:]]
    ensembl_ids = [x.decode() for x in f['row_attrs/Accession'][:]]




# Get vector of gene indices for GOI
indices = {}
for gene in genes_of_interest:
    idx = np.where(np.array(gene_ids) == gene)[0][0]
    indices[gene] = int(idx)



file_list = glob.glob(f"{file_dir}/TPM*.tsv.gz")
# take Nth file in the array
# N = int(os.getenv('SLURM_ARRAY_TASK_ID'))
N = 0
in_filename = file_list[N]

in_basename = os.path.basename(in_filename)
out_basename = in_basename.replace('TPM_', 'pct_1_').replace('.gz','')


# Start collecting output; begin with header
output = ['\t'.join(['cell_id'] + symbol_goi) + '\n']

# in_filename = 'TPM_160001_165000.tsv'


df = pd.read_csv(in_filename, compression='gzip', sep='\t')
df.set_index('cell_ID')

pd.read_table(text, sep='\t')

newdf1 = pd.DataFrame(mat)

import io   


df = pd.read_csv(io.StringIO(TESTDATA), sep=";")
print(df)

# iterate over gzfile


import timeit

def direct(f):
    df = pd.read_csv(f, compression='gzip', sep='\t')


def stringio(f):
    with gzip.open(f) as infile:
        text = infile.read().decode()
    df = pd.read_csv(io.StringIO(text), sep="\t", engine='pyarrow')


timeit.timeit(stringio(in_filename), number=1)


timeit.timeit(direct(in_filename), number=1)









    
df = pd.DataFrame(text, index=])

        if i > 0:
            print(i)
            line = list(line.decode().split())
            cell_id = line[0]
            #line = [int(x) for x in line[1:]]
            line = np.array(line[1:])
            output = [cell_id]
            output += get_goi_percentiles(line, indices)
            output.append('\t'.join(output)+'\n')

# iterate over gzfile
with gzip.open(in_filename) as infile:
    for i, line in enumerate(infile):
        if i > 0:
            print(i)
            line = list(line.decode().split())
            cell_id = line[0]
            #line = [int(x) for x in line[1:]]
            line = np.array(line[1:])
            output = [cell_id]
            output += get_goi_percentiles(line, indices)
            output.append('\t'.join(output)+'\n')

with open(out_basename, 'w') as outfile:
    outfile.write(''.join(output))


# with(h5py.File(loom_obj, 'r')) as f:
#     with open(out_filename, 'w') as out:
#         out.write('\t'.join(header)+'\n')
#         for start, stop in chunk_vals:
#             print(f"loading chunk from {start} to {stop}", flush=True)
#             chunk = f['matrix'][:, start:stop]
#             chunk = list(np.transpose(chunk))
#             chunk_out = ''
#             for i, cell_array in enumerate(chunk):
#                 cell_id = cell_ids[i + start]
#                 o = [cell_id]
#                 o += get_goi_percentiles(cell_array, indices)
#                 chunk_out += ('\t'.join(o)+'\n')
#             out.write(chunk_out)
