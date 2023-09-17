import csv
import os
from datetime import datetime


def write_csv(name, headers, rows):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    CSV = name + "_" + timestamp + ".csv"
    os.makedirs(os.path.dirname(CSV), exist_ok=True)
    with open(CSV, "w", newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(headers)
        csv_writer.writerows(rows)
    return CSV
