#!/usr/bin/env python3

import json
import argparse


def import_bw_dump(filename):

    grouped_items = {}

    with open(filename, "r") as json_file:
        json_pass = json.load(json_file)

    for item in json_pass["items"]:
        name = item["name"]
        if name in grouped_items:
            pass
        else:
            grouped_items[name] = [item]

    return grouped_items


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="json bw export file")
    args = parser.parse_args()

    print(import_bw_dump(args.filename))
