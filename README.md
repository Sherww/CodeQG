# CodeQG
This repository stores the details of paper "CodeQG: Automated Multiple Question Generation for Source Code Comprehension". Here are some key details about the project:

## Dataset

The complete data set can be found at https://drive.google.com/drive/folders/1j_GC58IEBezeBUK_DhvgY-wSHxNp3d9f?usp=sharing

## Inline comment-to-question
- The `comm2question` folder contains the comment-to-question model, which converts inline comments into questions.

## Question Generation 

- The `CodeBERT` folder contains the question generation model, which is used to generate questions for given code snippets.
## Statistics

- The `statistics` folder contains the code used in statistical analysis.

### Dependency
- pip install torch
- pip install transformers

### Train
* The model training and prediction were conducted on a machine with Nvidia GTX 1080 GPU, Intel(R) Core(TM) i7-6700 CPU and 16 GB RAM. The operating system is Ubuntu.
* Please refer to the paper for the detailed parameters of the model.
