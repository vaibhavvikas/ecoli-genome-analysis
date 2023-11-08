import csv
import os
import random

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from netgraph import Graph
from recordclass import recordclass

# Defining named tuple for our data
MobileCassette = recordclass('MobileCassette', ['gene', 'amr_class', 'frequency', 'distance', 'source', 'element'])


def read_csv_data(filename):
    data = []
    with open(filename, 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader) 
        data = list(csv_reader)
        return data


def prepare_data(filename):
    data = read_csv_data(filename)

    # we need to prepare nodes based on their frequency if it is found at the same distance.
    freq_data = {}
    max_freq = 1
    for info_data in data:
        # Ignore outliers i.e. distance > 10000
        if int(info_data[4]) > 10000:
            continue
        if (info_data[2], info_data[4]) in freq_data:
            freq_data[(info_data[2], info_data[4])].frequency += 1
            max_freq = max(max_freq, freq_data[(info_data[2], info_data[4])].frequency)
        else:
            freq_data[(info_data[2], info_data[4])] = MobileCassette(info_data[2], info_data[3], 1, int(info_data[4]), info_data[0].title(), info_data[1])

    data_list = []
    for key, val in freq_data.items():
        data_list.append([val.source, val.element, val.gene, val.amr_class, val.distance, val.frequency])
    df = pd.DataFrame(data_list, columns=["Source", "IS", "Gene", "AMR_Class", "Distance", "Frequency"])
    return df


def make_graph(gene_frequencies, filename, ax):
    n = len(gene_frequencies)
    source_markers = {'Bird': 'o', 'Animal': 's', 'Human': '^', 'Environment': 'v'}
    amr_class_colors = {
        "Beta-Lactam": "blue",
        "Sulphonamide": "green",
        "Aminoglycoside": "red",
        "Trimethoprim": "orange",
        "Disinfectant": "cyan",
        "Fosfomycin": "magenta",
        "Tetracycline": "yellow",
        "Macrolide": "brown",
        "Phenicol": "coral",
        "Quinolone": "silver",
        "Colistin": "mediumpurple",
        "Rifampicin": "goldenrod"
    }

    element = filename.split(".")[0].split("_")[1]
    
    ax.plot(0, 0, marker='o', markersize=5, color='r', label='IS Element')

    # Draw circular grids
    num_circular_grids = 0
    num_subgrids = 10
    max_distance = 100
    inner_distance = 100
    subgrid_distance = 10

    for i in range(num_circular_grids + 1):
        r_grid = i * inner_distance
        theta = np.linspace(0, 2 * np.pi, 360)
        for j in range(num_subgrids + 1):
            r_subgrid = r_grid + j * subgrid_distance
            r_values = np.full_like(theta, r_subgrid)
            ax.plot(theta, r_values, color='gray', alpha=0.1)

    angles = np.linspace(5, 360, len(gene_frequencies)+5)
    used = set()

    # Plot resistance genes with different shapes based on the source and add edges
    i = 0
    for _, row in gene_frequencies.iterrows():
        angle = np.radians(1)
        random_angle = random.choice(angles)
        while random_angle in used:
            random_angle = random.choice(angles)

        angle = np.radians(random_angle) # Random angle for visualization
        used.add(random_angle)
        distance = row['Distance']**(1/2)
        amr_class = row['AMR_Class']
        gene_name = row['Gene']
        color = amr_class_colors.get(amr_class, 'gray')  # Default to gray for unknown classes
        frequency = row['Frequency']
        source = row['Source']
        marker_style = source_markers.get(source, 'o')  # Default to circle if source is unknown
        dot_size = frequency * 4  # Adjust the scaling factor as needed
        ax.plot([angle], [distance], marker=marker_style, markersize=dot_size, color=color, alpha=1)
        ax.annotate(gene_name, (angle, distance), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8)
        
        # Add edges from center to genes
        ax.plot([0, angle], [0, distance], color='black', alpha=0.5, linestyle='-', lw=0.5)

    ax.set_xticks([])
    
    legend_handles = []

    # Source legend handles
    for source, marker_style in source_markers.items():
        legend_handles.append(plt.Line2D([0], [0], marker=marker_style, color='k', label=source))

    # AMR class legend handles
    for amr_class, color in amr_class_colors.items():
        legend_handles.append(plt.Line2D([0], [0], marker='o', color=color, label=amr_class))

    ax.legend(handles=legend_handles, title='Legend', loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_title(element)


def multiplot():
    # Getting files to make graph
    files = os.listdir("network_graph")
    files = list(filter(lambda x: x.endswith(".csv") and x.startswith("network"), files))

    matplotlib.rcParams['font.family'] = 'Calibri'
    matplotlib.rcParams['font.weight'] = 'bold'
    matplotlib.rcParams['font.style'] = 'italic'

    i = 0
    fig, axes = plt.subplots(6, 5, figsize=(60, 50),
                         subplot_kw=dict(polar=True))
    for file in files:
        filename = 'network_graph/' + file
        freq_data = prepare_data(filename)
        make_graph(freq_data, file, fig.axes[i])
        i += 1
    
    plt.tight_layout()
    plt.savefig("radial_combined.pdf")


if __name__ == "__main__":
    multiplot()