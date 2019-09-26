import json
import sys
from tqdm import tqdm

assert len(sys.argv) == 2

fname = sys.argv[1]

with open(fname, "r") as f:
    data = json.load(f)

count_fail = 0
count_right = 0
new_data = {"version": data["version"], "data": []}
for article in tqdm(data["data"]):
    new_article = {"title": article["title"], "paragraphs": []}
    for paragraph in article["paragraphs"]:
        new_paragraph = {"context": paragraph["context"], "qas": []}
        for i, qa in enumerate(paragraph["qas"]): 
            new_qa = {
                "question": qa["question"],
                "id": qa["id"],
                "answers": [
                    {
                        "answer_start": answer["answer_start"],
                        "text": answer["text"]
                    }
                    for answer in qa["answers"]
                    if answer["answer_start"] + len(answer["text"]) < len(paragraph["context"])
                    and paragraph["context"][answer["answer_start"]:answer["answer_start"]+len(answer["text"])] == answer["text"]
                ]
            }
            if len(new_qa["answers"]) != 0:
                new_paragraph["qas"].append(new_qa.copy())
                count_right += 1
            else:
                count_fail += 1
        new_article["paragraphs"].append(new_paragraph.copy())
    new_data["data"].append(new_article.copy())

del data

print("fail: {}/ success: {}".format(count_fail, count_right))

with open(fname[-5:] + "-clean.json", "w") as f:
    json.dump(new_data, f)