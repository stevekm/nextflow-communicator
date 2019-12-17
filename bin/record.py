#!/usr/bin/env python
import sys
import os
import argparse
import json
"""
Script to record custom key:value pairs into a common JSON file for later parsing
"""

def main(**kwargs):
    """
    Main control function for the script
    """
    key = kwargs.pop('key')
    value = kwargs.pop('value')
    value_type = kwargs.pop('type', 'val')
    current_directory = os.path.realpath(".")
    output_file = "communicator.json"
    output_path = os.path.join(current_directory, output_file)

    # if its a file then get absolute path
    if value_type == 'file':
        if os.path.exists(value):
            value = os.path.realpath(value)

    data = { key: value }

    # load the old data if a file already exists then update with new data and write it back out
    if os.path.exists(output_path):
        old_data = {}
        with open(output_path) as fin:
            old_data = json.load(fin)
        # Python 3.5 or greater; combine old and new data
        data = { **old_data, **data }
        # write it back out
        with open(output_path, "w") as fout:
            json.dump(data, fout)
    else:
        # just write the current data out
        with open(output_path, "w") as fout:
            json.dump(data, fout)


def parse():
    """
    Parses script args
    """
    parser = argparse.ArgumentParser(description='Nextflow Communicator Recorder; custom data recording for Nextflow')
    parser.add_argument("-k", '--key', dest = 'key', required = True, help = "Label for key to save")
    parser.add_argument("-v", '--value', dest = 'value', required = True, help = "Value to save")
    parser.add_argument("-t", '--type', default = 'val', dest = 'type', choices = ['val', 'file'], help = "Type of value")
    args = parser.parse_args()
    main(**vars(args))

if __name__ == '__main__':
    parse()
