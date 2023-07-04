import json
import os
import re
import argparse


def get_QA_data_splits(data, splits, o_path):
    print("**Generation Task**")
    for s in splits.keys():
        print("Working on " + s + " split...")
        with open(os.path.join(o_path, s + ".tsv"), 'w') as outG:
            for i in range(len(splits[s])):
                QA = data[splits[s][i][0]]
                title = QA['Title'].replace('\n', ' ')
                title = re.sub(r'\s+', ' ', title).strip()
                body = QA["Body"].replace('\n', ' ')
                body = re.sub(r'\s+', ' ', body).strip()
                if s == "train":
                    for jj in range(len(splits[s][i][1])):
                        A = QA['Answers'][splits[s][i][1][jj]]['Body']
                        A = re.sub(r'\s+', ' ', A).strip()
                        Q = "Title: " + title + " <sep> Body: " + body
                        outG.write(Q + "\t" + A + "\n")

                if s == "dev" or s == "test":
                    A = QA['Answers'][splits[s][i][1][0]]['Body']
                    A = re.sub(r'\s+', ' ', A).strip()
                    Q = "Title: " + title + " <sep> Body: " + body
                    outG.write(Q + "\t" + A + "\n")
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='data/')
    args = parser.parse_args()

    print("Loading data...")
    with open(os.path.join(args.data_dir, 'ELQA.unescaped.small.json'), "r") as If:
        data = json.load(If)

    with open(os.path.join(args.data_dir, "QA-task-splits-small.json")) as If:
        gen_splits = json.load(If)

    get_QA_data_splits(data, gen_splits, args.data_dir)
