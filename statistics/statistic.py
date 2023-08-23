import numpy as np
import re
import string
import nltk.stem.porter as pt
import jsonlines
import nltk.stem.porter as pt
import numpy as np
import re
import string
from tqdm import tqdm
from collections import Counter
def tokens():

    path='D:\\Research\\Codeqg\\codebert_qg\\classify_result\\'
    name=['are','bes','can','dos','forpurpose','have','howmany','howmuch','hows','inwhich','iss','may','must','other','should','whats','whens','wheres','whichs','whos','whys','will']

    nee_files1=[]
    # nee_files3=[]
    ptstem=pt.PorterStemmer()
    for i in range(len(name)):
        a=name[i]
        nee_file = path + f'{a}.jsonl'
        nee_files1.append(nee_file)
    # for i in range(len(name)):
    #     a=name[i]
    #     nee_file = path2 + f'{a}_train.csv'
    #     nee_files2.append(nee_file)
    # for i in range(len(name)):
    #     a=name[i]
    #     nee_file = path3 + f'{a}_valid.csv'
    #     nee_files3.append(nee_file)

    # comments_test=[]
    codes_test=[]
    questions_test=[]
    data_all=[]
    data_all_each=[]
    for i in range(len(nee_files1)):
        print('start_statistic:'+name[i]+'--------')
        data=[]
        # comms=[]
        cods=[]
        quess=[]

        with open(nee_files1[i],'r',encoding='utf-8')as f:
            for da in jsonlines.Reader(f):
                data.append(da)
        # with open(nee_files2[i],'r',encoding='utf-8')as f2:
        #     data2=f2.readlines()
        # with open(nee_files3[i],'r',encoding='utf-8')as f3:
        #     data3=f3.readlines()
        # data = data1+data2+data3
        data_all.extend(data)
        # return data_all
        stem_allwords_each=[]
        data_allword_each=[]
        data_allword_eachs=[]
        for dat in data:
            # stem_comms=[]
            code=dat['code_tokens']
            code=" ".join(code)
            ques=dat['docstring_tokens']
            ques=" ".join(ques)
            stem_codes=[]
            stem_quess=[]
            punc=string.punctuation
            # nee=dat.split(',')
            # comm=nee[3]
            # comm=re.sub(r"[%s]+" %punc, " ",comm)
            # code=nee[6]
            code=re.sub(r"[%s]+" %punc, " ",code)
            # ques=nee[-1]
            ques=re.sub(r"[%s]+" %punc, " ",ques)
            allword_each=code+ques
            # print(allword_each)
            # for word in comm.split():
            #     stem_comm = ptstem.stem(word)
            #     # print(stem_comm)
            #     stem_comms.append(stem_comm)
            # comms.append(len(stem_comms))
            #     # print(stem_comms)
            for word in code.split():
                stem_code = ptstem.stem(word)
                stem_codes.append(stem_code)
            cods.append(len(stem_codes))

            for word in ques.split():
                stem_ques = ptstem.stem(word)
                stem_quess.append(stem_ques)
            quess.append(len(stem_quess))

        #计算一个类别的文件的unique words
            
            for word1 in allword_each.split():
                stem_allword_each = ptstem.stem(word1)
                # print(stem_comm)
                data_allword_each.append(stem_allword_each)
            #     stem_allwords_each.append(stem_allword_each)
            # data_allword_each.extend(stem_allwords_each)
        for a in data_allword_each:
            if not a in data_allword_eachs:
                data_allword_eachs.append(a)
        # print(len(data_allword_eachs))
        # print(name[])
        data_all_each.append( name[i]+': '+str(len(data_allword_eachs)))    
        print("unique_each done")
        #计算每一类的详细统计数据        
        # statis_comm=np.percentile(comms,[0,25,50,75,100])
        statis_code=np.percentile(cods,[0,25,50,75,100])
        statis_codes=[]
        for a in statis_code:
            a=float(a)
            statis_codes.append(a)
        statis_ques=np.percentile(quess,[0,25,50,75,100])
        print('end_statistic:' +name[i])
        # comments_test.append(name[i]+': '+str(statis_comm))
        # codes_test.append(name[i]+': '+str(statis_code))
        codes_test.append(name[i]+': '+str(statis_codes))
        questions_test.append(name[i]+': '+str(statis_ques))   
    
    


         
    return codes_test,questions_test,data_all_each,data_all
def all_token(data_all):
    
    ptstem=pt.PorterStemmer()
    #获取所有数据的unique token
    print("start uniquetoken all:" )
    data_allword=[]
    data_allwords=[]
    for datall in data_all:
        # print(len(data_all))
        stem_allwords=[]

        punc=string.punctuation
        code=datall['code_tokens']
        code=" ".join(code)
        ques=datall['docstring_tokens']
        ques=" ".join(ques)
        # nee=datall.split(',')
        # comm=nee[3]
        # comm=re.sub(r"[%s]+" %punc, " ",comm)
        # code=nee[6]
        code=re.sub(r"[%s]+" %punc, " ",code)
        # ques=nee[-1]
        ques=re.sub(r"[%s]+" %punc, " ",ques)
           
        allword=code+ques
        for word in allword.split():
            stem_allword = ptstem.stem(word)
            # print(stem_comm)
            stem_allwords.append(stem_allword)
        data_allword.extend(stem_allwords)
    print("stem all done")
    for b in data_allword:
        if not b in data_allwords:
            data_allwords.append(b)
    return len(data_allwords)
      

if __name__=='__main__':
    # length 方法可以得到所有的类型的长度统计
    # comments_test,codes_test,questions_test,comments_train,codes_train,questions_train,comments_valid,codes_valid,questions_valid=length()
    # tokens方法是为了计算token的数目
    # comments_test,codes_test,questions_test,all_unique_words=tokens()
    codes_test,questions_test,data_all_each,data_all=tokens()
    # print(codes_test,questions_test,data_all_each)
    with open('output1.txt','w',encoding='utf-8')as f:
        for i in range(len(codes_test)):
            f.write(codes_test[i]+questions_test[i]+data_all_each[i]+'\n')
    dat_all_tokens=all_token(data_all)
    # print(dat_all_tokens)
    with open('output2.txt','w',encoding='utf-8')as ff:
        
        ff.write(str(dat_all_tokens)+'\n')