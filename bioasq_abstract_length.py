from squad_stats import CountDict

import json
import sys

with open(sys.argv[1], "r") as f:
    data = json.load(f)

ideal_lengths = CountDict()
snippet_lengths = CountDict()

for q in data["questions"]:
    for ans in q["ideal_answer"]:
        ideal_lengths[len(ans.split(" "))] += 1
    for s in q["snippets"]:
        snippet_lengths[len(s["text"].split(" "))] += 1

print(ideal_lengths.get_mean(), snippet_lengths.get_mean())