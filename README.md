# ELQA: A Corpus of Metalinguistic Questions and Answers about English


This repository provides data and codes for our ACL 2023 papar:

> [ELQA: A Corpus of Metalinguistic Questions and Answers about English](https://arxiv.org/abs/2205.00395) <br>
> [Shabnam Behzad](https://shabnam-b.github.io/), [Keisuke Sakaguchi](https://keisuke-sakaguchi.github.io/), [Nathan Schneider](https://people.cs.georgetown.edu/nschneid/), [Amir Zeldes](https://corpling.uis.georgetown.edu/amir/) <br>


The project was tested using Python 3.8. <br>

Please make sure you clone the repository using git LFS <br>

Original data was collected from [here](https://archive.org/details/stackexchange), Publication date: 2021-12-06, Contributor: Stack Exchange Community. Please adhere to Stack Exchange guidelines if using the data. <br><br>


To get train/dev/spalits for the QA task, run:
```shell script
python QA_splits.py
```
You will find output tsv files will be in "data" directory. <br> <br>

To train T5 models, please refer to [T5x GitHub page](https://github.com/google-research/t5x#training). <br><br>

** Human evaluation scores will be available soon! ** <br>

## Citation
If you find this work useful for your research, please cite our paper:

```
@article{behzad-etal-2023-elqa,
  title={ELQA: A Corpus of Metalinguistic Questions and Answers about English},
  author={Behzad, Shabnam and Sakaguchi, Keisuke and Schneider, Nathan and Zeldes, Amir},
  booktitle = "Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
  year = "2023",
  publisher = "Association for Computational Linguistics",
}
```

