## Instructions

First, please unzip the 7zipped files in the data directory (you should have cloned the repository with git LFS since data files are large). <br>
Then you can run the following commands one by one to get data in JSON format, and also train/dev/test splits for the tasks described in the paper. <br>

Assuming you will unzip files in the data directory:<br>

```.bash
python process_data.py --data_path ../data/ --site ell.stackexchange.com --output_file ../data/ell --map_file ../data/ell.mapping
python process_data.py --data_path ../data/ --site english.stackexchange.com --output_file ../data/eng --map_file ../data/eng.mapping
python merge_data.py --data_dir ../data/
python process_for_clustering.py --data_dir ../data/
python get_data_splits.py --data_dir ../data/ --task classification
python get_data_splits.py --data_dir ../data/ --task generation

```