# ---------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------- Reading files from mefinder_output ----------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------- #

from utils import csv_utils
import os

# We have multiple files, we only need to take the csv files and that too we have to format as the actual data start after the 
# initial comments
# Sample data:
#   date: 2023-01-15_01:39
#   sample: SRR3722017
#   mge_finder version: 1.0.5
#   mgedb version: 1.0.3
#   blastn version: 2.9.0+
#   mge_no,name,synonyms,prediction,type,allele_len,depth,e_value,identity,coverage,gaps,substitution,contig,start,end,cigar
#   1,MITEYpe1,,predicted,mite,115,15.545,0.0,0.786,0.902,4,21,NODE_1_length_200102_cov_15.544997,32949,33063,M40 D1 M4 I1 M21 I1 M5 D1 M43
# 
# If we look at the data, the first 5 lines are info about the file, and the column name and actual data start after that.

def get_mefinder_result():
    # Get all the files that endswith .csv in mefinder_folder.
    mefinder_folder = "input_files/mefinder_output"
    mefinder_files = [isolate for isolate in os.listdir(mefinder_folder) if isolate.endswith(".csv")]

    # Now we need to open each file and get the result for that we can have a dictionary where each key will map to its data inside
    # mefinder result

    mefinder_result = dict()

    for mefinder_file in mefinder_files:
        file_location = mefinder_folder + "/" + mefinder_file                   # file location is like mefinder_output/SRR3722017.csv
        isolate = mefinder_file.split(".")[0]                                   # get only the SRR number from SRR3722017.csv
        mefinder_result[isolate] = csv_utils.read_csv(filename=file_location, skiplines=5)

    # print(len(mefinder_result))
    # sys.exit()
    return mefinder_result
