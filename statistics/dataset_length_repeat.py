import numpy as np
import re
import string
import nltk.stem.porter as pt
import jsonlines
from tqdm import tqdm

def get_all_data():
    with open('D:\\Research\\Codeqg\\CodeQG\\data\\qg_data\\train.jsonl\\train.jsonl','r',encoding='utf-8')as f:
        datas1=[]
        for dat1 in jsonlines.Reader(f):
            datas1.append(dat1)
    with open('D:\\Research\\Codeqg\\CodeQG\\data\\qg_data\\valid.jsonl\\valid.jsonl','r',encoding='utf-8')as ff:
        datas2=[]
        for dat2 in jsonlines.Reader(ff):
            datas2.append(dat2)
    with open('D:\\Research\\Codeqg\\CodeQG\\data\\qg_data\\test.jsonl\\test.jsonl','r',encoding='utf-8')as fff:
        datas3=[]
        for dat3 in jsonlines.Reader(fff):
            datas3.append(dat3)  
    datas=datas1+datas2+datas3
    return datas
 
def repeat(datas):

    rels=[]
    rels_all=[]
    duls=[]
    num=0
    for data in tqdm(datas):
        context=data['context']
        code=data['code']
        ques=data['question']
        nee=context+','+code+','+ques

        if nee not in rels:
            rels.append(nee)
            rels_all.append(data)
        else:
            num +=1
            duls.append(data)
    print('repeat_num-----'+str(num))
    print('repeat_ratio-----'+str(num/len(datas)))
    return num/len(datas)
def classify(datas):    
    whats=[]
    whys=[]
    whos=[]
    whens=[]
    hows=[]
    whichs=[]
    wheres=[]
    other=[]
    forpurpose=[]
    howmany=[]
    inwhich=[]
    dos=[]
    will=[]
    must=[]
    can=[]
    are=[]
    iss=[]
    have=[]
    should=[]
    howmuch=[]
    may=[]
    bes=[]
    for dat in tqdm(datas):
            codes=[]
            # question_types=[]
            questions=[]
            # data_ids=[]

            code=dat['code']
            
            question_type=dat['question_type']
            question=dat['question']

            codes.append(code)
            questions.append(question)

            if re.match('^What',question):
                whats.append(dat)
            elif re.match('^Why',question):
                whys.append(dat) 
            elif re.match('^Who',question):
                whos.append(dat) 
            elif re.match('^When',question) or re.match('^Till when',question):
                whens.append(dat) 
            # elif re.match('^Till',question):
            #     tillwhens.append(dat) 
            elif re.match('^How',question):
                hows.append(dat) 
            elif re.match('^Which',question)or re.match('^\swhich',question):
                whichs.append(dat) 
            elif re.match('^Where',question):
                wheres.append(dat)
            #这里修改了，之前的都是for开头的就会被选中
            elif re.match('^For what',question):
                forpurpose.append(dat)
            elif "how many" in question:
                howmany.append(dat)
            elif "which direction" in question:
                inwhich.append(dat)
            elif "how much" in question:
                howmuch.append(dat)
            #祈使句的区分，do ,does等等
            elif re.match('^Do',question)or re.match('^Did',question)or re.match('^Does',question):
                     dos.append(dat) 
            elif re.match('^Must',question):
                    must.append(dat) 
            elif re.match('^Will',question)or re.match('^Would',question):
                    will.append(dat) 
            elif re.match('^Can',question)or re.match('^Could',question):
                    can.append(dat)
            elif re.match('^Are',question):
                are.append(dat)
            elif re.match('^May',question)or re.match('^Might',question):
                may.append(dat)
            elif re.match('^Is',question)or re.match('^Was',question):
                    iss.append(dat)
            elif re.match('^Have',question)or re.match('^Has',question)or re.match('^Had',question):
                    have.append(dat)
            elif re.match('^Should',question):
                should.append(dat)
            elif re.match('^Be',question):
                    bes.append(dat) 
            else:
                other.append(dat)
                
    #返回所有的结果，列表格式
    return whats,whys,whos,whens,hows,whichs,wheres,forpurpose,howmany,inwhich,howmuch,dos,must,will,can,are,may,iss,have,should,bes,other

    
def data_length(a,text):        
    ptstem=pt.PorterStemmer()
    #获取所有数据的unique token
    print(f"start uniquetoken all---{a}" )
    data_allword=[]
    data_allwords=[]
    code_word=[]
    code_words=[]
    question_word=[]
    question_words=[]
    codes=[]
    questions=[]
    for datall in tqdm(text):
        stem_allwords=[]
        ccc=[]
        qqq=[]
        punc=string.punctuation
        code=datall['code']
        ques=datall['question']
        code=re.sub(r"[%s]+" %punc, " ",code)
        ques=re.sub(r"[%s]+" %punc, " ",ques)
        codes.append(len(code.split()))
        questions.append(len(ques.split()))
        ######################
        for word in code.split():
                cc = ptstem.stem(word)
                # print(stem_comm)
                ccc.append(cc)
        code_word.extend(ccc)
        ######################
        for word in ques.split():
                qq = ptstem.stem(word)
                # print(stem_comm)
                qqq.append(qq)
        question_word.extend(qqq)
        ######################
        allword=code+ques
        for word in allword.split():
                stem_allword = ptstem.stem(word)
                # print(stem_comm)
                stem_allwords.append(stem_allword)
        data_allword.extend(stem_allwords)
    print("stem all done")
    print(f'code-length---{a}----------'+ str(np.percentile(codes, (0,25, 50, 75,100), interpolation='midpoint')))
    print(f'question-length----{a}---------'+ str(np.percentile(questions, (0,25, 50, 75,100), interpolation='midpoint')))
    # ######################
    for c in tqdm(code_word):
            if not c in code_words:
                code_words.append(c)
    print(f'all_unique_tokens_code--{a}'+str(len(code_words)))
    print(f'all__tokens_code--{a}'+str(len(code_word)))
    # print(code_word)
    ######################
    for q in tqdm(question_word):
            if not q in question_words:
                question_words.append(q)
    print(f'all_unique_tokens_question--{a}'+str(len(question_words)))
    print(f'all__tokens_question--{a}'+str(len(question_word)))

    ######################
    for b in tqdm(data_allword):
            if not b in data_allwords:
                data_allwords.append(b)
    print(f'all_unique_tokens_all--{a}'+str(len(data_allwords)))
    print(f'all__tokens_all--{a}'+str(len(data_allword)))

    return len(code_words),len(question_words),len(data_allwords)
   
if __name__ =='__main__':
    datas=get_all_data()
    whats,whys,whos,whens,hows,whichs,wheres,forpurpose,howmany,inwhich,howmuch,dos,must,will,can,are,may,iss,have,should,bes,other=classify(datas)
    print(len(whats),len(whys),len(whos),len(whens),len(hows),len(whichs),len(wheres),len(forpurpose),len(howmany),len(inwhich),len(howmuch),len(dos))
    print(len(must),len(will),len(can),len(are),len(may),len(iss),len(have),len(should),len(bes),len(other))
    # name=['datas','whats','whys','whos','whens','hows','whichs','wheres','forpurpose','howmany','inwhich','howmuch','dos','must','will','can','are','may','iss','have','should','bes','other']
    # all_text= [datas]+[whats]+[whys]+[whos]+[whens]+[hows]+[whichs]+[wheres]+[forpurpose]+[howmany]+[inwhich]+[howmuch]+[dos]+[must]+[will]+[can]+[are]+[may]+[iss]+[have]+[should]+[bes]+[other]
    name=['whats','whys','whos','whens','hows','whichs','wheres','forpurpose','howmany','inwhich','howmuch','dos','must','will','can','are','may','iss','have','should','bes','other']
    all_text= [whats]+[whys]+[whos]+[whens]+[hows]+[whichs]+[wheres]+[forpurpose]+[howmany]+[inwhich]+[howmuch]+[dos]+[must]+[will]+[can]+[are]+[may]+[iss]+[have]+[should]+[bes]+[other]
    for i in range(len(all_text)):
        data_length(name[i],all_text[i])
    repeat_ratio=repeat(datas)