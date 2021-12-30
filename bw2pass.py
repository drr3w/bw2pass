#!/usr/bin/env python3

import csv
import argparse

from subprocess import Popen, PIPE
from collections import namedtuple

_BWItem = namedtuple(
    "_BWItem",
    [
        "folder",
        "favorite",
        "type",
        "name",
        "notes",
        "fields",
        "reprompt",
        "login_uri",
        "login_username",
        "login_password",
        "login_totp",
    ],
)


class BWVault:
    """
    This class represents the whole bitwardent vault containing all the items
    """

    def __init__(self):
        self.items = []

    def import_bw_dump(self, filename):

        grouped_items = {}
        item_count = 0
        with open(filename, "r") as vault_file:
            reader = csv.DictReader(vault_file)

            # this is some dedupe logic, there is probably a better way
            for row in reader:
                name = row["name"]
                if name in grouped_items:
                    pass
                else:
                    grouped_items[name] = row["name"]
                    self.items.append(
                        _BWItem(
                            row["folder"],
                            row["favorite"],
                            row["type"],
                            row["name"],
                            row["notes"],
                            row["fields"],
                            row["reprompt"],
                            row["login_uri"],
                            row["login_username"],
                            row["login_password"],
                            row["login_totp"],
                        )
                    )

    def create_pass_entry(self, bw_item):

        msg = f"{bw_item.login_password}\nUSERNAME: {bw_item.login_username}\n NOTES: {bw_item.notes}"
        pass_process = Popen(
            ["pass", "insert", "--multiline", bw_item.name], stdin=PIPE, stdout=PIPE
        )
        pass_process.communicate(msg.encode())
        pass_process.wait()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="bw export file")
    args = parser.parse_args()

    vault = BWVault()
    vault.import_bw_dump(args.filename)
    for item in vault.items:
        vault.create_pass_entry(item)
