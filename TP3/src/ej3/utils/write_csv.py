import csv
import os
from datetime import datetime


def get_filename(name):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    CSV = name + "_" + timestamp + ".csv"
    return CSV


def create_csv(name, headers):
    CSV = get_filename(name)
    os.makedirs(os.path.dirname(CSV), exist_ok=True)
    with open(CSV, "w", newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(headers)
    return CSV


def append_row_to_csv(filename, row):
    with open(filename, "a", newline='') as csv_file:
        CSV = csv.writer(csv_file)
        CSV.writerow(row)


def write_csv(name, headers, rows):
    CSV = get_filename(name)
    os.makedirs(os.path.dirname(CSV), exist_ok=True)
    with open(CSV, "w", newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(headers)
        csv_writer.writerows(rows)
    return CSV
