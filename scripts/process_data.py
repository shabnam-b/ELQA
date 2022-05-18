import argparse
import os
import json
import create_json


def build_json(dump_folder, out_file, map_file):
    with open(map_file) as mf:
        maps = json.load(mf)
    df = create_json.generate_dataframe(dump_folder)
    data_simple, data_markdown, data_unescape = create_json.generate_QA(df, maps)
    with open(out_file + '.simple.json', 'w', encoding="utf8") as fp:
        json.dump(data_simple, fp, indent=2, ensure_ascii=False)
    with open(out_file + '.markdown.json', 'w', encoding="utf8") as fp:
        json.dump(data_markdown, fp, indent=2, ensure_ascii=False)
    with open(out_file + '.unescaped.json', 'w', encoding="utf8") as fp:
        json.dump(data_unescape, fp, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str,required=True)
    parser.add_argument('--site', type=str, required=True)
    parser.add_argument('--output_file', type=str, required=True)
    parser.add_argument('--map_file', type=str, required=True)
    args = parser.parse_args()

    dump_folder = os.path.join(args.data_path, args.site)

    if not os.path.exists(os.path.join(dump_folder, 'Posts.xml')):
        print("ERROR: The files for the chosen topic do not exist")
        exit(-1)

    build_json(dump_folder, args.output_file, args.map_file)
