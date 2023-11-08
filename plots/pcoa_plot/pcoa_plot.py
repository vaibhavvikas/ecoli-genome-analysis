import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.spatial.distance import pdist, squareform
from skbio.stats.ordination import pcoa

# Load the dataset
data = pd.read_csv("dataset_Level2_with_country_source.csv")
sample_ids = data['Sample']

# Remove non-numeric columns and handle missing values by replacing with zeros
features = data.select_dtypes(include=[np.number])
features = features.fillna(0)

# Center and scale the data to ensure all values are greater than zero
centered_scaled_data = features - features.min() + 1e-10

# Calculate the braycurtis distance matrix
distance_matrix = squareform(pdist(centered_scaled_data, metric='braycurtis'))

# Perform PCoA
pcoa_results = pcoa(distance_matrix)

# Extract and display eigenvalues
eigenvalues = pcoa_results.eigvals

# Calculate the percentage variation explained by each axis
total_variation = np.sum(eigenvalues)
percentage_variation = (eigenvalues / total_variation) * 100

print("Eigenvalues and Percentage Variation:")
for i, (eigenvalue, variation) in enumerate(zip(eigenvalues, percentage_variation)):
    print(f"PC{i + 1}: Eigenvalue = {eigenvalue:.4f}, Percentage Variation = {variation:.2f}%")

# Extract PCoA coordinates
pcoa_coords = pcoa_results.samples

# Add grouping information
data['group'] = data['Group']

# Create PCoA plots
sns.set(style='white')
fig, ax = plt.subplots(figsize=(8, 6))

for group, color in zip(data['group'].unique(), sns.color_palette('bright')):
    group_data = data[data['group'] == group]
    sns.scatterplot(x=pcoa_coords['PC1'][group_data.index], 
                    y=pcoa_coords['PC2'][group_data.index], 
                    label=group, 
                    color=color,
                    s=70,
                    ax=ax)


ax.set_xlabel(f'PCoA1 ({percentage_variation[0]:.2f}%)')
ax.set_ylabel(f'PCoA2 ({percentage_variation[1]:.2f}%)')
ax.set_title('PCoA Plot')
plt.legend(title='Group', loc='upper right')
ax.grid(False)  # Remove grid lines

# Save the plot to a file
# plt.savefig('pcoa_final_tpm.pdf')

plt.show()
