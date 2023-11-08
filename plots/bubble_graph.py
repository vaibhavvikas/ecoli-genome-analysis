import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

fill_colors = {
        "Human": "#d92938",
        "Animal": "#2484bf",
        "Bird": "#32a62e",
        "Unknown": "#a47dc6",
        "Environment": "#f2620f"
    }

data = {
    'Human': {'Tn2': 980, 'Tn801': 220, 'Tn1721': 60, 'Tn7': 1520, 'Tn4401': 580, 'Tn6092': 20, 'Tn21': 60},
    'Animal': {'Tn2': 560, 'Tn801': 60, 'Tn1721': 60, 'Tn7': 200, 'Tn4401': 0, 'Tn6092': 0, 'Tn21': 0},
    'Bird': {'Tn2': 280, 'Tn801': 40, 'Tn1721': 160, 'Tn7': 60, 'Tn4401': 0, 'Tn6092': 0, 'Tn21': 0},
    'Environment': {'Tn2': 320, 'Tn801': 0, 'Tn1721': 0, 'Tn7': 40, 'Tn4401': 0, 'Tn6092': 0, 'Tn21': 0}
}

# Create a list to store the data
data_list = []

x = {
    'Human': 20,
    'Animal': 30,
    'Bird': 40,
    'Environment': 50
}

y = {}
i = 1
for key in data['Human']:
    y[key] = i * 20
    i += 1

# Iterate over the dictionary and convert it into the desired format
for species, genes_data in data.items():
    for gene, size in genes_data.items():
        data_list.append([gene, size, species, x[species], y[gene]])

# Create a DataFrame
df = pd.DataFrame(data_list, columns=['Genes', 'Size', 'Species', 'x', 'y'])

# Display the DataFrame
df = df.sort_values(['Species', 'Size'], ascending=[False, True])
ax = sns.scatterplot(data=df, x="Species", y="Genes", hue="Species", size="Size", sizes=(0, 1000), alpha=0.7, palette=fill_colors)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Legend")
ax.grid(color='grey', linestyle='-', linewidth=0.25,)
plt.tight_layout()
plt.savefig('bubble_frequency_graph.pdf', format='pdf')
plt.show()
