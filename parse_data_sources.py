#!/usr/bin/env python3
"""
Parse and map the data inventory and map data sources with field information
for each track.

"""
import json
import csv
import os
import argparse
from pathlib import Path
from collections import defaultdict

def read_data_sources(file):
    with open(file, mode='r', newline='') as f:
        reader = csv.DictReader(f)
        inventory = defaultdict(dict)

        for row in reader:
            inventory[row['Track']][row['Data Source']] = row

    return inventory

def map_field_info(fields_path, data_sources):
    mapped_info = {}

    for file in fields_path.iterdir():
        if file.is_file():
            with open(file, mode='r', newline='') as f:
                reader = csv.DictReader(f)
                filename = os.path.basename(file)
                track = filename.split(" ")[-2]
                mapped_info[track] = {}
                data_source = ""

                for row in reader:
                    if row['Data Source']:
                        data_source = row['Data Source']
                        mapped_info[track][data_source] = []
                        continue
                    if data_source and row['Name']:
                        mapped_info[track][data_source].append(row | data_sources[track][data_source])

    return mapped_info


def main():
    parser = argparse.ArgumentParser(description="Map ACCESS data sources and field information")
    parser.add_argument('-d', '--data-sources', type=str, help="File path contain data source information")
    parser.add_argument('-f', '--fields', type=str, help="Directory path containing field information")
    args = parser.parse_args()

    data_sources = read_data_sources(args.data_sources)
    track_fields = map_field_info(Path(args.fields), data_sources)

    print(json.dumps(track_fields, indent=4))

if __name__ == "__main__":
    main()
