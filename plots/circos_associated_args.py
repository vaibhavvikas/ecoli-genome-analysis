from pycirclize import Circos
import pandas as pd
import matplotlib.colors as mclr

# Create matrix data
col_names = list("Birds Human Environment Animal".split(" "))
row_names= list("Bla Sul Qui Ami Tri Phe Fos Dis Tet Rif Mac Col".split(" "))
matrix_data = [
    [19, 34, 3, 2],
    [16, 3, 2, 0],
    [0, 2, 1, 0],
    [27, 11, 3, 7],
    [7, 2, 2, 0],
    [12, 2, 0, 2],
    [3, 0, 0, 0],
    [3, 1, 1, 0],
    [3, 16, 1, 0],
    [1, 0, 0, 0],
    [0, 4, 2, 0],
    [0, 0, 1, 0]
]
matrix_df = pd.DataFrame(matrix_data, index=row_names, columns=col_names)

# Initialize from matrix (Can also directly load tsv matrix file)
circos = Circos.initialize_from_matrix(
    matrix_df,
    space=3,
    r_lim=(93, 100),
    cmap = "rainbow",
    ticks_interval=500,
    label_kws=dict(r=94, size=12, color="black"),
)

circos.savefig("chord_amr_contigs.pdf")
