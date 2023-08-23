import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
)

import glob
import json
import numpy as np
import tqdm
import matplotlib.pyplot as plt

def main():
    files = glob.glob('./data/all_data/Output*_clean*.jsonl')
    files = sorted(files)

    dataset = []
    for file in files:
        print(file)
        with open(file, 'r', encoding='utf-8') as f:
            for line in tqdm.tqdm(f.readlines()):
                data = json.loads(line)
                dataset.append(data)
    
    '''
    # count code length and draw a histogram
    code_lengths = [len(d['code']) for d in dataset]
    plt.hist(code_lengths, bins=100)

    # to out.jpg
    plt.savefig('./code_out.jpg')
    '''

    # count question length and draw a histogram
    question_lengths = []
    for d in dataset:
        code = d['code']
        comment = d['inline_comment']
        if len(code) or len(comment) <=3:
            continue
        if 'qa' not in d:
            continue
        for qa in d['qa']:
            question_lengths.append(len(qa['question']))

    temp_question_lengths = sorted(question_lengths)
    l = len(question_lengths)
    temp_question_lengths = temp_question_lengths[: int(0.99 * l)]
    split = temp_question_lengths[-1]

    max_len = max(question_lengths)
    min_len = min(question_lengths)

    print(split)
    
    plt.hist(question_lengths, bins=100, range=(min_len, 500))
    # draw 95% line
    plt.axvline(x=split, color='r')
    plt.savefig('./question_out.jpg')

if __name__ == "__main__":
    main()