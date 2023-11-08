import csv

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from netgraph import Graph
from recordclass import recordclass

# Defining named tuple for our data
MobileCassette = recordclass('MobileCassette', ['gene', 'amr_class', 'frequency', 'source'])


def read_csv_data(filename):
    data = []
    with open(filename, 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader) 
        data = list(csv_reader)
        return data


def prepare_data(filename):
    data = read_csv_data(filename)
    # Is gene, class (amr)
    # we need to prepare nodes based on their frequency if it is found at the same distance.
    freq_data = {}
    for info_data in data:
        freq_data[(info_data[2], info_data[4])] = MobileCassette(info_data[2], info_data[3], int(info_data[4]), info_data[0].title())

    return freq_data


def make_graph(data: dict[tuple: MobileCassette], filename, ax):
    color_map_list = ['blue', 'orange', 'green', 'cyan', 'red', 'magenta', 'coral', 'goldenrod', 'yellow', 'indigo', 'deepskyblue', 'mediumpurple', "silver"]
    element = filename.split(".")[0].split("_")[1]
    
    # Node label prep
    color_map = {}
    node_labels = {0: element}
    node_size = {0: 0.5}
    edge_length = {}
    node_color = {0: 'deepskyblue'}
    node_shapes = {0:'o'}
    node_shapes_data = {'Bird': 'o', 'Animal': 's', 'Human': '^', 'Environment': 'v'}

    i = 0
    for _, val in data.items():
        if val.amr_class not in color_map:
            color_map[val.amr_class] = color_map_list[i]
            i += 1

    i = 1
    for _, val in data.items():
        node_labels[i] = val.gene
        # node_size[i] = int(val.frequency)*1
        node_size[i] = int(np.log2(val.frequency + 1))*10
        edge_length[(0, i)] = 1
        node_color[i] = color_map[val.amr_class]
        node_shapes[i] = node_shapes_data[val.source]
        i += 1

    edges = list(edge_length.keys())
    Graph(edges,
          node_labels=node_labels,
          node_size=node_size,
          node_color=node_color,
          node_layout='spring',
          node_shape=node_shapes,
          edge_width=2,
          node_label_fontdict=dict(size=10, horizontalalignment='center', verticalalignment='top'),
          scale=(10.,10.),
          ax=ax)
    
    # Using color_map for color legend
    node_colors_legend = []
    for node, color in color_map.items():
        proxy = plt.Line2D(
            [], [],
            linestyle='None',
            color=color,
            marker='o',
            markersize=4,
            label=node
        )
        node_colors_legend.append(proxy)

    node_legend_color = ax.legend(handles=node_colors_legend, loc='upper left', title='Node Colors')

    # Using color_shapes for shape legend
    node_shape_legend = []
    for node, shape in node_shapes_data.items():
        proxy = plt.Line2D(
            [], [],
            linestyle='None',
            color='black',
            marker=shape,
            markersize=4,
            label=node
        )
        node_shape_legend.append(proxy)

    node_legend_shape = ax.legend(handles=node_shape_legend, loc='lower left', title='Node Shapes')
    ax.add_artist(node_legend_color)
    ax.add_artist(node_legend_shape)
    ax.set_aspect('equal')


def multiplot():
    matplotlib.rcParams['font.family'] = 'Calibri'
    matplotlib.rcParams['font.weight'] = 'bold'
    matplotlib.rcParams['font.style'] = 'italic'
    figure, axis = plt.subplots(1,1, figsize=(5,5), dpi=20)
    
    # We take our tnfile and make a network graph for the same, Sample csv data of a file
    # Source,   Element,    Gene,       AMR class,      Frequency
    # bird,     Tn1721,     tet(A),     Tetracycline,   8
    # human,    Tn1721,     tet(A),     Tetracycline,   3
    # animal,   Tn1721,     tet(A),     Tetracycline,   3

    filename = 'network_graph/' + "network_tn4401.csv"
    freq_data = prepare_data(filename)
    make_graph(freq_data, "network_tn4401.csv", figure.axes[0])

    plt.savefig("network_tn4401.pdf")


if __name__ == "__main__":
    multiplot()