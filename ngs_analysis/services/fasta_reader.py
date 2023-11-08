# ---------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------- Reading Fasta Files Details -------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------- #


def get_fasta_details(fasta_file: str):
    fasta_details = dict()
    with open(fasta_file, "r") as file:
        for line in file:
            if line.startswith(">"):
                curr_line = (line.strip(">")).split("_")
                fasta_details[int(curr_line[1])] = (line.strip(">"), int(curr_line[3]))

    return fasta_details
