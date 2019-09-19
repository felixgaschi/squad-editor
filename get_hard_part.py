import sys, json, os, re
import numpy as np

assert len(sys.argv) == 2

filename = sys.argv[1]

with open(filename, "r") as f:
    data = json.load(f)

hard_data = {"version": data["version"], "data": []}
easy_data = {"version": data["version"], "data": []}

nb_hard = 0
nb_two = 0
nb_easy = 0

def context2sentence(context):
    sentences = re.findall("[^.!\?]+[.!\?]+", context)
    context_len = sum([len(elt) for elt in sentences])
    if len(context) > context_len:
        sentences.append(context[context_len:])
    assert len(context) == sum([len(sent) for sent in sentences])
    return sentences

for art_id, article in enumerate(data["data"]):
    hard_article = {"title": article["title"], "paragraphs": []}
    easy_article = {"title": article["title"], "paragraphs": []}

    for par_id, paragraph in enumerate(article["paragraphs"]):
        hard_paragraph = {"qas": [], "context": paragraph["context"]}
        easy_paragraph = {"qas": [], "context": paragraph["context"]}

        sentences = context2sentence(paragraph["context"])



        for qa in paragraph["qas"]:
            begin = qa["answers"][0]["answer_start"]
            end = begin + len(qa["answers"][0]["text"])

            index_start = 0
            offset = 0
            while begin >= offset + len(sentences[index_start]):
                offset += len(sentences[index_start])
                index_start += 1
            if end > offset + len(sentences[index_start]):
                nb_two += 1
                nb_hard += 1
                hard_paragraph["qas"].append(qa.copy())
                continue
            q_tokens = qa["question"].split(" ")
            
            overlaps = [
                len([w for w in q_tokens if w in sent.split(" ")])
                for sent in sentences
            ]

            best = np.argmax(overlaps)

            if best == index_start:
                nb_easy += 1
                easy_paragraph["qas"].append(qa.copy())
            else:
                nb_hard += 1
                hard_paragraph["qas"].append(qa.copy())
        hard_article["paragraphs"].append(hard_paragraph.copy())
        easy_article["paragraphs"].append(easy_paragraph.copy())
    hard_data["data"].append(hard_article.copy())
    easy_data["data"].append(easy_article.copy())

print("hard: {} (with on two sentences: {}) / easy: {}".format(nb_hard, nb_two, nb_easy))

with open(".".join(filename.split(".")[:-1]) + "-hard-perso.json", "w") as f:
    json.dump(hard_data, f)

with open(".".join(filename.split(".")[:-1]) + "-easy-perso.json", "w") as f:
    json.dump(easy_data, f)