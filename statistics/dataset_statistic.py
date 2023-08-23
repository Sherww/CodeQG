import jsonlines
import nltk.stem.porter as pt
import numpy as np
import re
import string
from tqdm import tqdm
from collections import Counter
def readdata(a):
    # with open(f'D:\\Research\\Codeqg\\CodeQG\\data\\dataset\\{a}.jsonl\\{a}.jsonl','r', encoding='utf-8') as f:
    #     i=0
    #     questions=[]
    #     for data in jsonlines.Reader(f):
    #        i+=1
    #        question=data['questions']
    #        for q in question:
    #            que=q['question']
    #        # nee=que.split('?')
    #        # for da in nee:
    #            questions.append(que)
    #     print(i)
    #     print(len(questions))
    with open(f'D:\\Research\\Codeqg\\CodeQG\\data\\qg_data\\{a}.jsonl\\{a}.jsonl','r', encoding='utf-8') as f:
        print(f'quest--------strating------{a}')

        i=0
        questions=[]
        questions_length=[]
        seesee=[]
        datas=[]
        # codes=[]
        for data in jsonlines.Reader(f):
            datas.append(data)
            i+=1
            # question=data['code']
            question=data['question']

            questions.append(question)
            questions_length.append(len(question.split()))
            if len(question.split())<=2:
                seesee.append(question)
        statis_comm=np.percentile(questions_length,[0,25,50,75,100])

        print('data_num'+ str(i))
        print(len(questions))
        print('num_of_token_per_data:'+ str(statis_comm))
        
    ptstem=pt.PorterStemmer()
    #获取所有数据的unique token
    print("start uniquetoken all:" )
    data_allword=[]
    data_allwords=[]
    for que in questions:
        # print(len(data_all))
        stem_allwords=[]

        punc=string.punctuation
        
        que=re.sub(r"[%s]+" %punc, " ",que)
           
        for word in que.split():
            stem_allword = ptstem.stem(word)
            # print(stem_comm)
            stem_allwords.append(stem_allword)
        data_allword.extend(stem_allwords)
    print("stem all done")
    for b in data_allword:
        if not b in data_allwords:
            data_allwords.append(b)
    print( len(data_allwords))
    repeat=[]
    repeat_num=0
    for j in tqdm(range(len(datas))):
        if datas[j] not in repeat:
            repeat.append(datas[j])
        else:
            repeat_num+=1
    print('repeat_num:'+str(repeat_num))
    print('repeat_num/all_data: '+str(repeat_num/len(datas)))
    # repeat=set(datas)
    # print('repeat_num/all_data: '+str((len(datas)-len(repeat))/len(datas)))
    # return seesee
def readdata_code(a):
    # with open(f'D:\\Research\\Codeqg\\CodeQG\\data\\dataset\\{a}.jsonl\\{a}.jsonl','r', encoding='utf-8') as f:
    #     i=0
    #     questions=[]
    #     for data in jsonlines.Reader(f):
    #        i+=1
    #        question=data['questions']
    #        for q in question:
    #            que=q['question']
    #        # nee=que.split('?')
    #        # for da in nee:
    #            questions.append(que)
    #     print(i)
    #     print(len(questions))
    with open(f'D:\\Research\\Codeqg\\CodeQG\\data\\qg_data\\{a}.jsonl\\{a}.jsonl','r', encoding='utf-8') as f:
        print(f'code--------strating--------{a}')
        i=0
        questions=[]
        questions_length=[]
        seesee=[]
        datas=[]
        # codes=[]
        for data in jsonlines.Reader(f):
            datas.append(data)
            i+=1
            # question=data['code']
            question=data['code']

            questions.append(question)
            questions_length.append(len(question.split()))
            if len(question.split())<=2:
                seesee.append(question)
        statis_comm=np.percentile(questions_length,[0,25,50,75,100])

        print('data_num'+ str(i))
        print(len(questions))
        print('num_of_token_per_data:'+ str(statis_comm))
        
    ptstem=pt.PorterStemmer()
    #获取所有数据的unique token
    print("start uniquetoken all:" )
    data_allword=[]
    data_allwords=[]
    for que in questions:
        # print(len(data_all))
        stem_allwords=[]

        punc=string.punctuation
        
        que=re.sub(r"[%s]+" %punc, " ",que)
           
        for word in que.split():
            stem_allword = ptstem.stem(word)
            # print(stem_comm)
            stem_allwords.append(stem_allword)
        data_allword.extend(stem_allwords)
    print("stem all done")
    for b in data_allword:
        if not b in data_allwords:
            data_allwords.append(b)
    print( len(data_allwords))
    # repeat=[]
    # repeat_num=0
    # for j in tqdm(range(len(datas))):
    #     if datas[j] not in repeat:
    #         repeat.append(datas[j])
    #     else:
    #         repeat_num+=1
    # print('repeat_num:'+str(repeat_num))
    # print('repeat_num/all_data: '+str(repeat_num/len(datas)))
    # repeat=set(datas)
    # print('repeat_num/all_data: '+str((len(datas)-len(repeat))/len(datas)))

    # return seesee
def repeat():
    with open('D:\\Research\\Codeqg\\CodeQG\\data\\qg_data\\test.jsonl\\test.jsonl','r', encoding='utf-8') as f:
        datas_test=[]
        # codes=[]
        for data in jsonlines.Reader(f):
            datas_test.append(data)
    with open('D:\\Research\\Codeqg\\CodeQG\\data\\qg_data\\valid.jsonl\\valid.jsonl','r', encoding='utf-8') as ff:
        datas_valid=[]
        # codes=[]
        for data in jsonlines.Reader(ff):
            datas_valid.append(data)
    with open('D:\\Research\\Codeqg\\CodeQG\\data\\qg_data\\train.jsonl\\train.jsonl','r', encoding='utf-8') as fff:
        datas_train=[]
        # codes=[]
        for data in jsonlines.Reader(fff):
            datas_train.append(data)  
    repeat_test_num=0
    # repeat_test=[]
    for i in tqdm(range(len(datas_test))):
        if datas_test[i] in datas_train:
            repeat_test_num+=1
        else:
            pass
    repeat_valid_num=0
    # repeat_test=[]
    for j in tqdm(range(len(datas_valid))):
        if datas_valid[j] in datas_train:
            repeat_valid_num+=1
        else:
            pass        
    print('test_repeat_against_train:'+ str(repeat_test_num/len(datas_train)))
    print('valid_repeat_against_train:'+ str(repeat_valid_num/len(datas_train)))

if __name__=='__main__':
    # name=['test']

    name=['valid','test','train']
    for a in name:
        readdata(a)
        readdata_code(a)
    repeat()