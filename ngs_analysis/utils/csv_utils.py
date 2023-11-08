import csv

def read_csv(filename: str, skiplines: int = 0) -> list:
    res = []
    with open(file=filename, mode="r") as file:
        # skip unwanted lines
        csv_data = file.readlines()[skiplines:]
        
        csv_file = csv.DictReader(csv_data)
        for line in csv_file:
            res.append(line)
    
    return res
