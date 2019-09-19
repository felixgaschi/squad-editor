import sys
import json
import os
from tqdm import tqdm
from squad_stats import CountDict

files = os.listdir(sys.argv[1])

abs_len = CountDict()

for f in files:
    path = os.path.join(sys.argv[1], f)

    try:
        reader = open(path, "r")
        data = json.load(reader)
        abstract = data["abstract"]
        abs_len[len(abstract.split(" "))] += 1
    except:
        continue


print(abs_len.get_mean())