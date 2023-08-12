import csv
from datetime import datetime


def write_to_csv(filename_prefix, data):
    current = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = filename_prefix + "_" + current + ".csv"
    with open(filename, 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)
