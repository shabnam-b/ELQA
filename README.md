# ELQA: A Corpus of Metalinguistic Questions and Answers about English


This repository provides data and codes for our ACL 2023 paper:

> [ELQA: A Corpus of Metalinguistic Questions and Answers about English](https://aclanthology.org/2023.acl-long.113/) <br>
> [Shabnam Behzad](https://shabnam-b.github.io/), [Keisuke Sakaguchi](https://keisuke-sakaguchi.github.io/), [Nathan Schneider](https://people.cs.georgetown.edu/nschneid/), [Amir Zeldes](https://corpling.uis.georgetown.edu/amir/) <br>


Make sure you have git LFS installed before cloning this repository.
```shell script
git lfs install
git lfs clone https://github.com/shabnam-b/ELQA.git
```

Original data was collected from [here](https://archive.org/details/stackexchange), Publication date: 2021-12-06, Contributor: Stack Exchange Community. Please adhere to Stack Exchange guidelines if using the data. License: https://stackoverflow.com/help/licensing  <br><br>


To get train/dev/test splits for the QA task, run:
```shell script
python QA_splits.py
```
You will find output tsv files in "data" directory. The project was tested using Python 3.8. <br> <br>

To train T5 models, please refer to [T5x GitHub page](https://github.com/google-research/t5x#training). <br><br>

** Human evaluation scores will be available soon! ** <br>

## Citation
If you find this work useful for your research, please cite our paper:

```
@inproceedings{behzad-etal-2023-elqa,
    title = "{ELQA}: A Corpus of Metalinguistic Questions and Answers about {E}nglish",
    author = "Behzad, Shabnam  and
      Sakaguchi, Keisuke  and
      Schneider, Nathan  and
      Zeldes, Amir",
    booktitle = "Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2023",
    address = "Toronto, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.acl-long.113",
    pages = "2031--2047",
}
```

