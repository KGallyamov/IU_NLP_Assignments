import json
import os
import pandas as pd


df = pd.read_json("raw_test.jsonl")
test_df = pd.read_json('data/test.jsonl', lines=True).drop([2, 3], axis=1)
ids = test_df['id'].to_list()

output_file = "test.jsonl"

if os.path.exists(output_file):
    os.remove(output_file)

for i in range(len(df)):
    ners = [x for x in df.iloc[i].to_list() if len(x)]
    ners_dict = {(x[0], x[1]): (x[2], float(x[3])) for x in ners[0]}
    for ner in ners[1:]:
        for _from, _to, tag, conf, depth in ner:
            if (_from, _to) not in ners_dict:
                ners_dict[(_from, _to)] = (tag, float(conf))
            elif ners_dict[(_from, _to)][-1] > float(conf):
                ners_dict[(_from, _to)] = (tag, float(conf))
    merged_ners = [[k[0], k[1], v[0]] for k, v in ners_dict.items() if v[1] > 0.33]

    json_obj = {"ners": merged_ners, "id": ids[i]}

    # Write the JSON object to the file (in jsonlines format)
    with open(output_file, "a") as f:
        f.write(json.dumps(json_obj) + "\n")