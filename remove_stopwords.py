import json
import sys
from nltk.corpus import stopwords
import nltk

nltk.download("stopwords")

assert len(sys.argv) == 2

filename = sys.argv[1]

with open(filename, "r") as f:
    data = json.load(f)

stops = stopwords.words("english")

new_data = {
    "version": data["version"],
    "data": [
        {
            "title": article["title"],
            "paragraphs": [
                {
                    "context": paragraph["context"],
                    "qas": [
                        {
                            "question": " ".join([w for w in qa["question"].split(" ") if w not in stops]),
                            "id": qa["id"],
                            "answers": qa["answers"].copy()
                        }
                        for qa in paragraph["qas"]
                    ]
                }
                for paragraph in article["paragraphs"]
            ]
        }
        for article in data["data"]
    ]
}

with open(".".join(filename.split(".")[:-1]) + "-nostops.json", "w") as f:
    json.dump(new_data, f)

