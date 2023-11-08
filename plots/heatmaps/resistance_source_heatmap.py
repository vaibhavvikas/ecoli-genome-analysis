import matplotlib
matplotlib.use('tkagg')
import seaborn as sns
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

data = []
genes = []

first = True

with open('resistance_source_transposed.csv') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter = ',')
    for row in csv_reader:
        if first:
            sample_names = row[1:]
            first = False
        else:
            genes.append(row[0])
            data.append(row[1:])

data = np.array(data).astype(int)
print(data)
print(len(genes))
print(len(sample_names))
print(data.shape)

sns.set_context('paper', font_scale=1.1)
sns_plot = sns.clustermap(data, xticklabels=sample_names, yticklabels=genes, figsize=(8,8), annot=False, standard_scale=1, cmap= 'afmhot', linewidths=0.5, linecolor = 'grey')

sns_plot.savefig('heatmap.pdf')
plt.show()

