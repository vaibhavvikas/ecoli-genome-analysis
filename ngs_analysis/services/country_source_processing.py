# ---------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------- Reading Country Souce Details File ------------------------------------------------ #
# ---------------------------------------------------------------------------------------------------------------------------- #

from utils import csv_utils, datetime_utils
from collections import namedtuple

# Get all Srr Files details such as their country, source and collection date from the country_source_data.csv
# Csv File Columns
# |  Isolate ID  |   Country   |   Source  |   Date  |  
#
# There are missing values and also the Date is inconsistent. So, to be more precise we will be using the year 

def get_country_source_details():
    country_source_date_file = "input_files/country_source_date.csv"
    country_details = csv_utils.read_csv(country_source_date_file)

    # Defining a named tuple or easy access of data
    Source = namedtuple('Isolate', ['country', 'source', 'year'])

    # Creating a proper object for the details
    isolate_country_details = dict()

    for isolate in country_details:
        year = int(datetime_utils.get_year(isolate["Date"]))
        isolate_country_details[isolate["Isolate ID"]] = Source(isolate["Country"].strip(), isolate["Source"].strip(), year)
    
    # print(len(isolate_country_details))
    # sys.exit()
    
    return isolate_country_details


# Data in isolate_country_details of type
# print(isolate_country_details["SRR13143182"].source) 
# SRR13143182 Isolate(country='china', source='poultry (tissue sample)', date='2017')  ................... Sample Data
# To access various dettails we can directly use the dictionary to get a particular value
