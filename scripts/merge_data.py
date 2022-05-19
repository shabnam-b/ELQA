import argparse
import os
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, required=True)
    args = parser.parse_args()

    types = ['simple', 'markdown', 'unescaped']
    for t in types:
        m = {}
        for filename in os.listdir(args.data_dir):
            if t in filename:
                n = filename.split('.')[0]
                with open(os.path.join(args.data_dir, filename), "r") as f:
                    data = json.load(f)
                    for id in data:
                        m[n + '_' + str(id)] = data[id]

        with open(os.path.join(args.data_dir, 'ell-eng.' + t + '.json'), 'w', encoding="utf8") as fp:
            json.dump(m, fp, indent=2, ensure_ascii=False)
