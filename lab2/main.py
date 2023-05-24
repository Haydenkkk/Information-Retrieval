import os
import math
from collections import defaultdict
import cut
import re

class RetrievalModel: # 定义一个名为RetrievalModel的类 RetrievalModel:检索模型
    def __init__(self, path): # 定义初始化函数，传入参数为文件路径
        self.path = path # 将文件路径赋值给self.path
        self.index = defaultdict(dict) # 定义一个默认字典用于存储倒排索引 defaultdict是 python 内置的一个类，用于实现默认值的字典
        self.doc_length = {} # 定义一个空字典用于存储每个文档的长度
        self.total_length = 0 # 定义一个变量用于存储所有文档总长度 所有文件长度之和是指所有文件中所有词的长度之和？
        self.docs = [] # 定义一个空列表用于存储所有文档文件名
        self.stop_words = set() # 定义一个空集合用于存储停用词表
        self.load_stop_words() # 载入停用词表
        self.build_index() # 建立倒排索引
        self.compute_lengths() # 计算每个文档的长度


    def load_stop_words(self): # 定义载入停用词表的函数
        with open('stop_words.txt', 'r', encoding='utf-8') as f: # 打开停用词表文件
            for line in f: # 遍历文件中的每一行
                self.stop_words.add(line.strip()) # 将去除空白符的行添加到停用词表中

    #使用一个字典来存储倒排索引。字典的键是单词，值是一个字典，该字典的键是文档ID，值是单词在文档中出现的次数。
    def build_index(self): # 定义建立倒排索引函数
        for doc_id, file in enumerate(os.listdir(self.path)): # 遍历文件夹中的每个文件 enumrate()函数用于将一个可遍历的数据对象组合为一个索引序列，同时列出数据和数据下标
            self.docs.append(file) # 将文件名添加到文档列表中
            with open(os.path.join(self.path, file), 'r', encoding='utf-8') as f: # 打开文件
                for line in f: # 遍历文件中的每一行
                    tokens = line.strip().split() # 将每行转换为单词列表 split()默认以空格为分隔符
                    for token in tokens: # 遍历单词列表中的每个单词
                        if token not in self.stop_words: # 如果单词不在停用词表中
                            self.index[token][doc_id] = self.index[token].get(doc_id, 0) + 1 # 在倒排索引中添加单词和文档ID的映射关系

    def compute_lengths(self): # 定义计算文档长度的函数
        for doc_id in range(len(self.docs)): # 遍历每个文档
            length = 0 # 初始化文档长度为0
            for term, freq in self.index.items(): # 遍历每个单词在倒排索引中的出现频率 items():以列表返回可遍历的(键, 值) 元组数组
                tf = freq.get(doc_id, 0) # 获取该单词在该文档中的出现次数
                if tf > 0: # 如果出现次数大于0
                    length += (1 + math.log(tf)) # 将该单词的长度加到文档长度上 math.log()返回tf的自然对数 加1：避免tf为1时，tf_weight为0
            self.doc_length[doc_id] = length # 将文档长度添加到文档长度字典中
            self.total_length += length # 将文档长度加到所有文档总长度上

    def calculate_query_vector(self, query): # 定义计算查询向量的函数
        query_vector = defaultdict(int) # 定义一个默认字典用于存储查询向量
        for term in query.strip().split(): # 遍历查询中的每个单词
            if term not in self.stop_words: # 如果单词不在停用词表中
                query_vector[term] += 1 # 在查询向量中添加单词和出现次数的映射关系
        length = math.sqrt(sum(map(lambda x: x*x, query_vector.values()))) # 计算查询向量的长度  
        for term, freq in query_vector.items(): # 遍历查询向量中的每个单词和出现次数
            query_vector[term] = freq / length # 将每个单词的出现次数除以查询向量的长度，得到单词的权重
        return query_vector # 返回查询向量

    def calculate_score(self, query, words_counter): # 定义计算文档得分的函数
        query_vector = self.calculate_query_vector(query) # 调用计算查询向量的函数，得到查询向量
        scores = defaultdict(float) # 定义一个默认字典用于存储文档得分
        for term, freq in query_vector.items(): # 遍历查询向量中的每个单词和权重
            if term in self.index: # 如果单词在倒排索引中
                idf = math.log(len(self.docs) / len(self.index[term])) # 计算单词的逆文档频率
                for doc_id, tf in self.index[term].items(): # 遍历单词在倒排索引中的每个文档ID和出现次数
                    words_counter[doc_id][term] = tf # 将单词和出现次数添加到文档ID对应的字典中
                    tf_weight = 1 + math.log(tf) # 计算单词的权重
                    scores[doc_id] += freq * tf_weight * idf # 计算文档得分
        for doc_id, score in scores.items(): # 遍历文档得分中的每个文档ID和得分
            scores[doc_id] /= self.doc_length[doc_id] / self.total_length # 将得分除以文档长度的比例和所有文档总长度的比例
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True) # 将文档得分按照得分从大到小排序
        return sorted_scores # 返回排序后的文档得分列表

    def search(self, query, num_results=10): # 定义查询函数
        query = cut.cut_sentence(query) # 对查询进行分词
        words_counter = defaultdict(dict) # 定义一个默认字典用于存储每个文档中的单词和出现次数
        print('匹配分词:', query)
        results = self.calculate_score(query, words_counter)[:num_results] # 调用计算文档得分的函数，取前num_results个文档
        for doc_id, score in results: # 遍历所有结果中的每个文档ID和得分
            print('Document:', self.docs[doc_id]) # 打印文档名
            print('Score:', score) # 打印得分
            print(words_counter[doc_id])
            # with open(os.path.join(self.path, self.docs[doc_id]), 'r', encoding='utf-8') as f: # 打开文档
            #     print('Content:', f.readline().strip()) # 打印文档内容的第一行
            print('---' * 10) # 打印分割线



rm = RetrievalModel('DouLuoDaLu_seg') # 创建一个RetrievalModel对象，传入文件路径

#test

