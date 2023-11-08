import matplotlib.pylab as plt
import pandas as pd
from PyComplexHeatmap import *
from sklearn.preprocessing import StandardScaler

data = pd.read_csv("dataset_level3_with_country_source.csv", header=0)
df = data.copy()
data = data.set_index("Isolate ID")

source = df.pop("Source")
country = df.pop("Country")

heatmap_data = df.set_index("Isolate ID").T


col_ha = HeatmapAnnotation(Country=anno_simple(data.Country, legend=True),
                           Source=anno_simple(data.Source, legend=True), label_side='left', axis=1,
                           )


for col in heatmap_data.columns:
    max_val = heatmap_data[col].max()
    heatmap_data[col] = heatmap_data[col]/max_val


cm = ClusterMapPlotter(data=heatmap_data, top_annotation=col_ha,
                       row_names_side='left',
                       col_cluster=True, row_cluster=True,
                       label='Value',row_dendrogram=False, col_dendrogram=True,
                       show_rownames=True, show_colnames=False,
                       cmap='viridis',
                       tree_kws={'row_cmap': 'Dark2'},
                       xticklabels_kws={'labelrotation':-45,'labelcolor':'blue'},
                       yticklabels_kws = {'labelsize':8},
                       legend=True
                       )

plt.savefig("cluster_map_heatmap.pdf")
plt.show()