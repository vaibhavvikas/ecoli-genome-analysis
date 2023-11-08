# ---------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------- Reading the Plasmid Size File -------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------- #

from utils import csv_utils
from collections import defaultdict


def get_plasmid_size():
    plasmid_size_file = "input_files/plasmid_size.csv"
    plasmid_info = csv_utils.read_csv(plasmid_size_file)

    # Creating a proper object for the details
    plasmid_details = dict()

    for plasmid in plasmid_info:
        plasmid_details[(plasmid["data"].strip().lower())] = int(plasmid["size"])

    # print(len(plasmid_details))
    # sys.exit()
    return plasmid_details
