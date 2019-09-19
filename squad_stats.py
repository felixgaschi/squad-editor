import sys
import json
import numpy as np



class CountDict(dict):

    def __getitem__(self, key):
        if key not in super(CountDict, self).keys():
            return 0
        else:
            return super(CountDict, self).__getitem__(key)

    def get_mean(self):
        num = 0
        denom = 0
        for key in self.keys():
            num += key * self[key]
            denom += self[key]
        return num * 1. / denom



if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        data = json.load(f)

    par_lengths = CountDict()
    ans_lengths = CountDict()

    for article in data["data"]:
        for paragraph in article["paragraphs"]:
            par_lengths[len(paragraph["context"].split(" "))] += 1
            for qa in paragraph["qas"]:
                for answer in qa["answers"]:
                    ans_lengths[len(answer["text"].split(" "))] += 1
    
    par_mean = par_lengths.get_mean()
    ans_mean = ans_lengths.get_mean()

    print(par_mean, ans_mean) 