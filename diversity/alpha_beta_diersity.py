from collections import defaultdict
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import wilcoxon
from skbio.diversity import alpha_diversity, beta_diversity
from skbio.stats.distance import anosim, permanova
from skbio.stats.ordination import pcoa

fill_colors = {
        "Human": "#d92938",
        "Animal": "#2484bf",
        "Bird": "#32a62e",
        "Unknown": "#a47dc6",
        "Environment": "#f2620f"
    }

class Reader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.read_abundance_data(filepath)

    def read_abundance_data(self, filepath=None):
        if filepath != None:
            self.filepath = filepath
        
        # Read file
        data = pd.read_csv(filepath, header=0)
        
        # Remove source and country as we need only numeric values and these
        # two fields can be used to group the data
        self.group = data.pop("Group").values.tolist()
        self.isolate = data["Sample"].values.tolist()
        # self.country = data.pop("Country").values.tolist()

        # Extracting the data
        self.otu_ids = [col for col in data.columns][1:]
        self.abundance_data = np.array(data.set_index("Sample").values.tolist())


def calculate_bray_curtis_density(data):
    bc_dm = beta_diversity("braycurtis", data.abundance_data, data.isolate)
    wu_pc = pcoa(bc_dm, number_of_dimensions=2)

    sample_md = {data.isolate[i]: data.group[i] for i in range(len(data.isolate))}
    sample_md = pd.DataFrame.from_dict(sample_md, columns=['source'], orient='index')

    adiv_alpha_div = alpha_diversity('simpson', data.abundance_data, data.isolate)
    sample_md['Diversity (Simpson)'] = adiv_alpha_div
    
    results = permanova(bc_dm, sample_md, column='source', permutations=999)
    print("test statistic", results['test statistic'], "p-value", results['p-value'] < 0.1)

    # Plot Alpha Diversity density plot
    fill_colors = {
        "Human": "#d92938",
        "Animal": "#2484bf",
        "Bird": "#32a62e",
        "Unknown": "#a47dc6",
        "Environment": "#f2620f"
    }
    sns.kdeplot(
        data=sample_md, x="Diversity (Simpson)", hue="source",
        fill=True, common_norm=True, palette=fill_colors,
        alpha=0.5, linewidth=0.5,
    )
    
    plt.savefig("simpson.pdf")
    plt.close()

    adiv_alpha_div = alpha_diversity('shannon', data.abundance_data, data.isolate)
    sample_md['Diversity (Shannon)'] = adiv_alpha_div
    
    # Plot Alpha Diversity density plot
    fill_colors = {
        "Human": "#d92938",
        "Animal": "#2484bf",
        "Bird": "#32a62e",
        "Unknown": "#a47dc6",
        "Environment": "#f2620f"
    }
    sns.kdeplot(
        data=sample_md, x="Diversity (Shannon)", hue="source",
        fill=True, common_norm=True, palette=fill_colors,
        alpha=0.5, linewidth=0.5,
    )
    
    plt.savefig("Shannon.pdf")
    plt.close()

    adiv_alpha_div = alpha_diversity('chao1', data.abundance_data, data.isolate)
    sample_md['Diversity (Chao1)'] = adiv_alpha_div
    
    results = permanova(bc_dm, sample_md, column='source', permutations=999)
    print("test statistic", results['test statistic'], "p-value", results['p-value'] < 0.1)

    # Plot Alpha Diversity density plot
    fill_colors = {
        "Human": "#d92938",
        "Animal": "#2484bf",
        "Bird": "#32a62e",
        "Unknown": "#a47dc6",
        "Environment": "#f2620f"
    }
    sns.kdeplot(
        data=sample_md, x="Diversity (Chao1)", hue="source",
        fill=True, common_norm=True, palette=fill_colors,
        alpha=0.5, linewidth=0.5,
    )
    
    plt.savefig("chao1.pdf")
    plt.close()   


def calculate_bray_curtis_box(data):
    bc_dm = beta_diversity("braycurtis", data.abundance_data, data.isolate)
    wu_pc = pcoa(bc_dm, number_of_dimensions=2)

    sample_md = {data.isolate[i]: data.group[i] for i in range(len(data.isolate))}
    sample_md = pd.DataFrame.from_dict(sample_md, columns=['source'], orient='index')

    adiv_alpha_div = alpha_diversity('simpson', data.abundance_data, data.isolate)
    sample_md['Diversity (Simpson)'] = adiv_alpha_div

    results = permanova(bc_dm, sample_md, column='source', permutations=999)
    print("test statistic", results['test statistic'], "p-value", results['p-value'] < 0.1)

    # Plot Alpha Diversity density plot
    fill_colors = {
        "Human": "#d92938",
        "Animal": "#2484bf",
        "Bird": "#32a62e",
        "Unknown": "#a47dc6",
        "Environment": "#f2620f"
    }
    
    sns.boxplot(x="source", y="Diversity (Simpson)", data=sample_md, palette=fill_colors)
    
    plt.savefig("simpson_box.pdf")
    plt.close()

    adiv_alpha_div = alpha_diversity('shannon', data.abundance_data, data.isolate)
    sample_md['Diversity (Shannon)'] = adiv_alpha_div
    
    # Plot Alpha Diversity density plot
    fill_colors = {
        "Human": "#d92938",
        "Animal": "#2484bf",
        "Bird": "#32a62e",
        "Unknown": "#a47dc6",
        "Environment": "#f2620f"
    }
    sns.boxplot(x="source", y="Diversity (Shannon)", data=sample_md, palette=fill_colors)
    
    plt.savefig("Shannon_box.pdf")
    plt.close()

    adiv_alpha_div = alpha_diversity('chao1', data.abundance_data, data.isolate)
    sample_md['Diversity (Chao1)'] = adiv_alpha_div
    
    results = permanova(bc_dm, sample_md, column='source', permutations=999)
    print("test statistic", results['test statistic'], "p-value", results['p-value'] < 0.1)

    # Plot Alpha Diversity density plot
    fill_colors = {
        "Human": "#d92938",
        "Animal": "#2484bf",
        "Bird": "#32a62e",
        "Unknown": "#a47dc6",
        "Environment": "#f2620f"
    }
    sns.boxplot(x="source", y="Diversity (Chao1)", data=sample_md, palette=fill_colors)
    
    plt.savefig("chao1_box.pdf")
    plt.close()


def pairwise_diversity(data, filename):
    bc_dm = beta_diversity("braycurtis", data["abundance_data"], data["isolate"])
    sample_md = {data["isolate"][i]: data["group"][i] for i in range(len(data["isolate"]))}
    sample_md = pd.DataFrame.from_dict(sample_md, columns=['source'], orient='index')

    # Anosim
    results = anosim(bc_dm, sample_md, column='source', permutations=999)
    print(filename, "test statistic", results['test statistic'], "p-value", results["p-value"], results['p-value'] < 0.1)

    adiv_alpha_div = alpha_diversity('chao1', data["abundance_data"], data["isolate"])
    sample_md['Observed Genes'] = adiv_alpha_div

    # Plot Alpha Diversity box plot
    fig = sample_md.boxplot(column='Observed Genes', by='source')
    plt.tight_layout()
    plt.savefig(filename)


def pairwise_significance(data):
    groups = {} # Id and source, data
    group = list(set(data.group))
    pairs = list(combinations(group, 2))
    
    for pair in pairs:
        pair_name = "_".join(pair)
        groups[pair_name] = {"group": [], "isolate": [], "abundance_data": []}
        for i in range(len(data.group)):
            if data.group[i] in pair:
                groups[pair_name]["group"].append(data.group[i])
                groups[pair_name]["isolate"].append(data.isolate[i])
                groups[pair_name]["abundance_data"].append(data.abundance_data[i])

    for key, val in groups.items():
        pairwise_diversity(val, key)


def calculate_bray_curtis(data):
    plt.figure(figsize=(10,10))
    bc_dm = beta_diversity("braycurtis", data.abundance_data, data.isolate)
    wu_pc = pcoa(bc_dm, number_of_dimensions=2)

    sample_md = {data.isolate[i]: data.group[i] for i in range(len(data.isolate))}
    sample_md = pd.DataFrame.from_dict(sample_md, columns=['source'], orient='index')

    twod_data = wu_pc.samples[['PC1', 'PC2']]
    sample_md = sample_md.join(twod_data)
    sns.scatterplot(data=sample_md, x="PC1", y="PC2", hue="source", palette=fill_colors)
    plt.tight_layout()
    plt.savefig("braycurtis.pdf")
    plt.close()


def calculate_jaccard(data):
    plt.figure(figsize=(10,10))
    bc_dm = beta_diversity("jaccard", data.abundance_data, data.isolate)
    wu_pc = pcoa(bc_dm, number_of_dimensions=2)

    sample_md = {data.isolate[i]: data.group[i] for i in range(len(data.isolate))}
    sample_md = pd.DataFrame.from_dict(sample_md, columns=['source'], orient='index')

    twod_data = wu_pc.samples[['PC1', 'PC2']]
    sample_md = sample_md.join(twod_data)
    sns.scatterplot(data=sample_md, x="PC1", y="PC2", hue="source", palette=fill_colors)
    plt.tight_layout()
    plt.savefig("jaccard.pdf")
    plt.close()


def calculate_manhattan(data):
    plt.figure(figsize=(10,10))
    bc_dm = beta_diversity("manhattan", data.abundance_data, data.isolate)
    wu_pc = pcoa(bc_dm, number_of_dimensions=2)

    sample_md = {data.isolate[i]: data.group[i] for i in range(len(data.isolate))}
    sample_md = pd.DataFrame.from_dict(sample_md, columns=['source'], orient='index')

    twod_data = wu_pc.samples[['PC1', 'PC2']]
    sample_md = sample_md.join(twod_data)
    sns.scatterplot(data=sample_md, x="PC1", y="PC2", hue="source", palette=fill_colors)
    plt.tight_layout()
    plt.savefig("manhattan.pdf")
    plt.close()


def main():
    filepath = "level2.csv"
    data = Reader(filepath)

    # Diversity scatterplot
    calculate_bray_curtis(data)
    calculate_jaccard(data)
    calculate_manhattan(data)

    # Calculate Pairwise Significance
    pairwise_significance(data)

    # Calculate Beta diversity and box plot
    calculate_bray_curtis_box(data)

    # Calculate Beta diversity and density plots
    calculate_bray_curtis_density(data)
    
if __name__ == "__main__":
    main()
