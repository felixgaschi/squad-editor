import json
import sys

with open(sys.argv[1], "r") as f:
    data = json.load(f)

def print_data(data, offset=0):
    if isinstance(data, list):
        if data == []:
            print("  " * offset + "[]")
        else:
            print("  " * offset + "[")
            print_data(elt[0], offset=offset+1)
            print("  " * offset + "]")
    if isinstance(data, dict):
        for key in data.keys():
            print("  " * offset + "{")
            print("  " * (offset + 1) + key + ":")
            print_data(data[key], offset=offset+1)
            print("  " * offset + "}")
    else:
        return

print_data(data)