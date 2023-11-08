from collections import defaultdict

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load tn_plasmid data
df = pd.read_excel('tn_plasmid.xlsx', index_col='plasmid')
df = df.T

fig, ax = plt.subplots()
df.plot(kind='bar', stacked=True, colormap='plasma', ax=ax)

x_label = 'Unit Transposons'
y_label = 'Mobile Genetic Elements'

ax.set_xlabel(x_label)
ax.set_ylabel(y_label)
plt.xticks(rotation=0)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Legend")
plt.tight_layout()
plt.show()
