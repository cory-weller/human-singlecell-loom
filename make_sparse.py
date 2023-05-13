#!/usr/bin/env python

# For importing tabular data and converting to sparse MatrixMarket

import numpy as np
import scipy
from scipy import io, sparse
import pandas as pd

in_filename = 'goi_percentiles.tsv'
mtx_fn = in_filename.split('.tsv')[0] + '.mtx'


# Import full csv and format row names correctly
mat = pd.read_csv(in_filename, sep='\t')
mat.rename(columns={'Unnamed: 0':'gene_id'}, inplace=True)
mat.set_index('CellID', inplace=True)

# Convert to sparse
mat_sparse = scipy.sparse.csr_matrix(mat)

# Write sparse matrix
scipy.io.mmwrite(mtx_fn, mat_sparse, field='integer')

# Import sparse matrix
readin = scipy.io.mmread(mtx_fn).toarray()

# Note that column and row names are not saved in the sparse matrix!
# They will need to be saved as a separate text file to add back in later