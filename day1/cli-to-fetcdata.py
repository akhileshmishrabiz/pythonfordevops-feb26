# cli to fetch stuff like public ip, dns name of ec2
# hostname , ami-id , AccountId, instance-id

import json
import argparse

file_input = "jsondata.txt"
# read from json.txt file and put the data in a dict
with open(file_input, "r") as f:
    data = f.read()
# print(type(data))
useful_data = json.loads(data)
# print(type(useful_data))
# print(useful_data)


def get_ami_id(data_dict):
    return data_dict.get("meta-data").get("ami-id")


# print(get_ami_id(useful_data))


def get_hostname(data_dict):
    return data_dict.get("meta-data").get("hostname")


def get_instance_id(data_dict):
    return data_dict.get("meta-data").get("instance-id")


def get_account_id(data_dict):
    macs = data_dict.get("meta-data").get("network").get("interfaces").get("macs")
    # first_mac = next(iter(macs.values()))
    # return first_mac.get("owner-id")

    # print(macs.values())
    # print(type(macs.values()))
    for item in macs.values():
        return item.get("owner-id")


# take args from user to get the keyword to search for in the dict
# python3 cli-to-fetcdata.py  ami-id
parser = argparse.ArgumentParser(
    description="A simple CLI to fetch data from json file"
)
parser.add_argument(
    "keyword",
    type=str,
    choices=["hostname", "ami-id", "account_id", "instance-id"],
    help="The keyword to search for in the json data",
)

args = parser.parse_args()
keyword = args.keyword

if keyword == "ami-id":
    print(get_ami_id(useful_data))
elif keyword == "hostname":
    print(get_hostname(useful_data))
elif keyword == "instance-id":
    print(get_instance_id(useful_data))
elif keyword == "account_id":
    print(get_account_id(useful_data))
