import json
import os
import re
import argparse


def create_generation_data(data, splits):
    print("**Generation Task**")
    for s in splits.keys():
        print("Working on " + s + " split...")
        with open(os.path.join(args.data_dir, "generation", s + ".mrkd.jsonl"), 'w') as outF:
            for i in range(len(splits[s]['ids'])):
                QA = data[splits[s]['ids'][i]]
                title = QA['Title'].replace('\n', ' ')
                title = re.sub(r'\s+', ' ', title).strip()
                body = QA["Body"].strip()
                A = QA['Answers'][splits[s]['A_index'][i]]['Body'].strip()
                Q = "Title: " + title + " Question: " + body
                json.dump({'input': Q, 'output': A}, outF)
                outF.write('\n')
    return


def create_multi_ref_test_set(data, splits):
    print("Working on multi ref dev and test splits...")
    for s in splits.keys():
        if s != 'train':
            test_d = {}
            for i in range(len(splits[s]['ids'])):
                indx = splits[s]['ids'][i]
                QA = data[indx]
                test_d[indx] = {'input': '', 'refs': []}
                title = QA['Title'].replace('\n', ' ')
                title = re.sub(r'\s+', ' ', title).strip()
                body = QA["Body"].strip()
                As = QA['Answers']
                for ii in As:
                    if ii["Score"] > 1 or ii['is_accepted']:
                        A = ii["Body"].strip()
                        test_d[indx]['refs'].append(A)
                Q = "Title: " + title + " Question: " + body
                test_d[indx]['input'] = Q

            with open(os.path.join(args.data_dir, "generation", s + ".multi-ref.mrkd.json"), 'w',
                      encoding="utf8") as fp:
                json.dump(test_d, fp, indent=2, ensure_ascii=False)

    return


def create_classification_data(data, splits, data_dir):
    print("**Classification Task**")
    for s in splits.keys():
        print("Working on " + s + " split...")
        with open(os.path.join(data_dir, "classification", s + ".tsv"), 'w') as outF:
            for i in range(len(splits[s]['ids'])):
                QA = data[splits[s]['ids'][i]]
                body = QA["Body"].strip()
                A = QA['Answers'][splits[s]['A_index'][i]]['Body'].strip()
                l = splits[s]['label'][i]
                outF.write(str(l) + '\t' + body + '\t' + A + '\n')
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, required=True)
    parser.add_argument('--task', type=str, required=True)
    args = parser.parse_args()

    print("Loading data...")
    if args.task == 'generation':
        with open(os.path.join(args.data_dir, 'ell-eng.markdown.json'), "r") as If:
            data = json.load(If)

        with open(os.path.join(args.data_dir, "generation", "splits.json")) as If:
            gen_splits = json.load(If)

        create_generation_data(data, gen_splits)
        create_multi_ref_test_set(data, gen_splits)
    elif args.task == 'classification':
        with open(os.path.join(args.data_dir, 'ell-eng.simple.json')) as If:
            data = json.load(If)

        with open(os.path.join(args.data_dir, "classification", "splits.json")) as If:
            class_splits = json.load(If)

        create_classification_data(data, class_splits, args.data_dir)
    else:
        print("Error: task should be either classification or generation")
