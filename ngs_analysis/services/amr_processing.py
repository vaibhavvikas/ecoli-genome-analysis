# ---------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------- Reading the AMR Class File -------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------- #

from utils import csv_utils
from collections import defaultdict


def get_amr_class():
    amr_class_file = "input_files/amr_class.csv"
    amr_details = csv_utils.read_csv(amr_class_file)

    # Creating a proper object for the details
    amr_class_details = defaultdict(str)

    for amr in amr_details:
        amr_class_details[(amr["resistance_gene"].strip().lower())] = amr["amr_class"].title()

    return amr_class_details
