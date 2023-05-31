import numpy as np 
import pandas as pd 
import os
import re

for dirname, _, filenames in os.walk('/docs'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
summary = pd.read_csv('input/news-summary/news_summary.csv', encoding='iso-8859-1')
raw = pd.read_csv('input/news-summary/news_summary_more.csv', encoding='iso-8859-1')
# 从raw和summary数据集中选择所需的列，并存储在pre1和pre2变量中。
pre1 =  raw.iloc[:,0:2].copy()
pre2 = summary.iloc[:,0:6].copy()

pre2['text'] = pre2['author'].str.cat(pre2['date'].str.cat(pre2['read_more'].str.cat(pre2['text'].str.cat(pre2['ctext'], sep = " "), sep =" "),sep= " "), sep = " ")
pre = pd.DataFrame()
# 将pre1['text']和pre2['text']合并为一个Series，并存储在pre['text']中。
pre['text'] = pd.concat([pre1['text'], pre2['text']], ignore_index=True)
# 将pre1['headlines']和pre2['headlines']合并为一个Series，并存储在pre['summary']中。
pre['summary'] = pd.concat([pre1['headlines'],pre2['headlines']],ignore_index = True)

#Removes non-alphabetic characters:
def text_strip(column):
    for row in column:
        #移除转义字符
        row=re.sub("(\\t)", ' ', str(row)).lower() 
        row=re.sub("(\\r)", ' ', str(row)).lower() 
        row=re.sub("(\\n)", ' ', str(row)).lower()
        #如果_连续出现多次，移除_
        row=re.sub("(__+)", ' ', str(row)).lower()   
        #如果-连续出现多次，移除-
        row=re.sub("(--+)", ' ', str(row)).lower()  
        #如果~连续出现多次，移除~
        row=re.sub("(~~+)", ' ', str(row)).lower()   
        #如果+连续出现多次，移除+
        row=re.sub("(\+\++)", ' ', str(row)).lower()   
        #如果.连续出现多次，移除.
        row=re.sub("(\.\.+)", ' ', str(row)).lower()   
        #移除<>()|&©ø"',;?~*!
        row=re.sub(r"[<>()|&©ø\[\]\'\",;?~*!]", ' ', str(row)).lower()
        #移除mailto:
        row=re.sub("(mailto:)", ' ', str(row)).lower() 
        #移除文本中的\x9*
        row=re.sub(r"(\\x9\d)", ' ', str(row)).lower() 
        #将INC数字替换为INC_NUM
        row=re.sub("([iI][nN][cC]\d+)", 'INC_NUM', str(row)).lower() 
        #将CM#和CHG#替换为CM_NUM
        row=re.sub("([cC][mM]\d+)|([cC][hH][gG]\d+)", 'CM_NUM', str(row)).lower() 
        #移除单词末尾的句号（不在单词中间的句号）
        row=re.sub("(\.\s+)", ' ', str(row)).lower() 
        #移除单词末尾的连字符（不在单词中间的连字符）
        row=re.sub("(\-\s+)", ' ', str(row)).lower() 
        #移除单词末尾的冒号（不在单词中间的冒号）
        row=re.sub("(\:\s+)", ' ', str(row)).lower() 
        
        row=re.sub("(\s+.\s+)", ' ', str(row)).lower() #移除两个空格之间悬挂的任何单个字符
        #将形如https://abc.xyz.net/browse/sdf-5327的URL替换为abc.xyz.net
        try:
            url = re.search(r'((https*:\/*)([^\/\s]+))(.[^\s]+)', str(row))
            repl_url = url.group(3)
            row = re.sub(r'((https*:\/*)([^\/\s]+))(.[^\s]+)',repl_url, str(row))
        except:
            pass #可能存在没有URL的电子邮件
        row = re.sub("(\s+)",' ',str(row)).lower() #移除多个空格
        
        #应该始终放在最后
        row=re.sub("(\s+.\s+)", ' ', str(row)).lower()
        yield row


brief_cleaning1 = text_strip(pre['text'])
brief_cleaning2 = text_strip(pre['summary'])

from time import time
import spacy
nlp = spacy.load('en_core_web_sm', disable=['ner', 'parser'])
# 将pre['text']和pre['summary']分别传入nlp.pipe函数中，使用spaCy进行批量处理和清洗，结果存储在text和summary变量中。
t = time()
print("Starting to clean the text data....")
#Batch the data points into 5000 and run on all cores for faster preprocessing
text = [str(doc) for doc in nlp.pipe(brief_cleaning1, batch_size=5000)]
#Takes 7-8 mins
print('Time to clean up everything: {} mins'.format(round((time() - t) / 60, 2)))
t = time()

print("Starting to clean the summary data....")
# 在summary的每个句子前添加"START"标记，并在句子末尾添加"END"标记。
summary = ['_START_ '+ str(doc) + ' _END_' for doc in nlp.pipe(brief_cleaning2, batch_size=5000)]
#Takes 7-8 mins
print('Time to clean up everything: {} mins'.format(round((time() - t) / 60, 2)))

# 将清理后的文本存储在pre['cleaned_text']中，将清理后的摘要存储在pre['cleaned_summary']中。
pre['cleaned_text'] = pd.Series(text)
pre['cleaned_summary'] = pd.Series(summary)
# 将清理后的文本和摘要存储在csv文件中。
# pre[['cleaned_text']].to_csv('cleaned_text.csv', index=False)
# pre[['cleaned_summary']].to_csv('cleaned_summary.csv', index=False)


text_count = []
summary_count = []
for sent in pre['cleaned_text']:
    text_count.append(len(sent.split()))
for sent in pre['cleaned_summary']:
    summary_count.append(len(sent.split()))
graph_df= pd.DataFrame()
graph_df['text']=text_count
graph_df['summary']=summary_count
# 定义max_text_len和max_summary_len的最大长度。
max_text_len=1000
max_summary_len=35

cleaned_text =np.array(pre['cleaned_text'])
cleaned_summary=np.array(pre['cleaned_summary'])
# 从清理后的文本和摘要中选择符合长度要求的样本，存储在short_text和short_summary中。
short_text=[]
short_summary=[]

for i in range(len(cleaned_text)):
    if(len(cleaned_summary[i].split())<=max_summary_len and len(cleaned_text[i].split())<=max_text_len):
        short_text.append(cleaned_text[i])
        short_summary.append(cleaned_summary[i])

# 创建DataFrame post_pre，并将short_text和short_summary存储在相应的列中。
post_pre=pd.DataFrame({'text':short_text,'summary':short_summary})
# 在摘要的每个句子前添加"sostok"标记，在句子末尾添加"eostok"标记。
post_pre['summary'] = post_pre['summary'].apply(lambda x : 'sostok '+ x + ' eostok')
post_pre.to_csv('post_pre.csv', index=False)