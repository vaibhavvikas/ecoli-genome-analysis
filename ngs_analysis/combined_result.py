from collections import defaultdict
from services import country_source_processing, mefinder_processing, amr_processing


# ---------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------ Creating the final result data -------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------- #

# Class for mapping respective entries
class IsolateDetails:

    def __init__(self, country="", source="", date="", data_type="", data="", amr="", synonyms="", predicted_phenotype="",
                 identity_percentage="", overlap_percentage="", hsp_length_by_total_length="", contig="", start="",
                 end="", accession="", allele_length="", depth="", e_value="", gaps="", substitution="", cigar=""):
        self.country = country                                          # from isolate country details 
        self.source = source                                            # from isolate country details 
        self.date = date                                                # from isolate country details 
        self.data_type = data_type                                      # mefinder["type"],          results_file["Data Type"]
        self.data = data                                                # mefinder["name"],          results_file["Data"]
        self.amr = amr                                                  # from amr details
        self.synonyms = synonyms                                        # mefinder["synonyms"],      NA
        self.predicted_phenotype = predicted_phenotype                  # mefinder["prediction"],    results_file["Predicted Phenotype"]
        self.identity_percentage = identity_percentage                  # mefinder["identity"]*100,  results_file["%Identity"]
        self.overlap_percentage  = overlap_percentage                   # mefinder["coverage"]*100,  results_file["%Overlap"]
        self.hsp_length_by_total_length = hsp_length_by_total_length    # NA,                        results_file["HSP Length/Total Length"]
        self.contig = contig                                            # mefinder["contig"],        results_file["Contig"]
        self.start = start                                              # mefinder["start"],         results_file["Start"]
        self.end = end                                                  # mefinder["end"],           results_file["End"]
        self.accession = accession                                      # NA,                        results_file["Accession"]
        self.allele_length = allele_length                              # mefinder["allele_len"],    NA
        self.depth = depth                                              # mefinder["depth"],         NA
        self.e_value = e_value                                          # mefinder["e_value"],       NA
        self.gaps = gaps                                                # mefinder["gaps"],         NA
        self.substitution = substitution                                # mefinder["substitution"],  NA
        self.cigar = cigar                                              # mefinder["cigar"],         NA


final_result = defaultdict(list)
column_names = ["Isolate ID", "Country", "Source", "Date", "Data Type", "Data", "Amr Class", "Synonyms", "Predicted Phenotype", "%Identity",
                "%Overlap", "HSP Length/Total Length", "Contig", "Start", "End", "Accession", "Allele Length", "Depth", "E Value",
                "Gaps", "Substitution", "Cigar"]


# ---------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------- Using services to get the appropriate data ------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------- #


isolate_country_details = country_source_processing.get_country_source_details()
mefinder_result = mefinder_processing.get_mefinder_result()
amr_details = amr_processing.get_amr_class()


# ---------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------- Reading data from final_result.xlsx ---------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------- #

import pandas as pd

staramr_result = "input_files/staramr_result.xlsx"
df = pd.read_excel(staramr_result)

curr_isolate_id = ""
df = df.fillna("")

for index, row in df.iterrows():
    if row['Isolate ID'] != "":
        curr_isolate_id = row['Isolate ID']

        # This first row always have the Data Type as MLST which we can use to keep the country info
        isolate_details = IsolateDetails(data_type=row['Data Type'],
                                         data=row['Data'],
                                         country=isolate_country_details[row['Isolate ID']].country,
                                         source=isolate_country_details[row['Isolate ID']].source,
                                         date=isolate_country_details[row['Isolate ID']].year)
    else:
        isolate_details = IsolateDetails(data_type=row['Data Type'],
                                         data=row['Data'],
                                         amr=amr_details[(row['Data'].strip()).lower()],
                                         predicted_phenotype=row["Predicted Phenotype"],    
                                         identity_percentage=(float(row["%Identity"]) if row["%Identity"] != "" else row["%Identity"]),
                                         overlap_percentage=(float(row["%Overlap"]) if row["%Overlap"] != "" else row["%Overlap"]),
                                         hsp_length_by_total_length=row["HSP Length/Total Length"],
                                         contig=row["Contig"],
                                         start=(int(row["Start"]) if row["Start"] != "" else row["Start"]),
                                         end=(int(row["End"]) if row["End"] != "" else row["End"]),
                                         accession=row["Accession"],
        )

    final_result[curr_isolate_id].append(isolate_details)

# print(len(final_result))
# sys.exit()

# ---------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------- Using MeFinder data to create entries -------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------- #

for isolate in mefinder_result:
    for mefinder in mefinder_result[isolate]:
        if float(mefinder["identity"])*100 >= 90:
            isolate_details = IsolateDetails(data_type=mefinder["type"],
                                            data=mefinder["name"],
                                            amr=amr_details[(mefinder['name'].strip()).lower()],
                                            synonyms=mefinder["synonyms"],
                                            predicted_phenotype=mefinder["prediction"],
                                            identity_percentage=float(mefinder["identity"])*100,
                                            overlap_percentage=float(mefinder["coverage"])*100,
                                            contig=mefinder["contig"],
                                            start=int(mefinder["start"]),
                                            end=int(mefinder["end"]),
                                            allele_length=int(mefinder["allele_len"]),
                                            depth=float(mefinder["depth"]),
                                            e_value=float(mefinder["e_value"]),
                                            gaps=int(mefinder["gaps"]),
                                            substitution=int(mefinder["substitution"]),
                                            cigar=mefinder["cigar"],
                                            )
        
            final_result[isolate].append(isolate_details)

# print(len(final_result))
# sys.exit()

# ---------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------- Using Final data to create Excel FIle -------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------- #

# Now we have the combined data of both startamr and mefinder in our object final result.

# First we sort the data for each isolate based on the contig
for isolate in final_result:
    final_result[isolate].sort(key=lambda x: (int(x.contig.split("_")[1]) if (x.contig != None and x.contig != "") else 0))


# Creating a 2D list to arrange our values in the excel file to be saved
final_result_as_list = []

for isolate in final_result:
    for index, row in enumerate(final_result[isolate]):
        curr_line = [isolate, row.country, row.source, row.date, row.data_type, row.data, row.amr, row.synonyms, row.predicted_phenotype,
                     row.identity_percentage, row.overlap_percentage, row.hsp_length_by_total_length, row.contig, row.start, row.end,
                     row.accession, row.allele_length, row.depth, row.e_value, row.gaps, row.substitution, row.cigar]
        
        if index != 0:
            curr_line[0] = ""

        final_result_as_list.append(curr_line)

# Now We will use this object to create an excel file and save the result
pd_df = pd.DataFrame(final_result_as_list, columns=column_names)
pd_df.to_excel("output/combined_result.xlsx", index=False)
