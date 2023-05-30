import os
import math
from collections import defaultdict
from cut import cut_sentence
import json

class RetrievalModel2: 
    def __init__(self, path):
        self.path = path 
        self.index = defaultdict(dict)
        self.doc_length = {} # doc_length 用于存储每个文档的长度
        self.total_length = 0 # 所有文档总长度 所有文件长度之和是指所有文件中所有词的长度之和？
        self.docs = [] # docs 用于存储所有文档文件名
        self.stop_words = set() # stop_words 用于存储停用词表
        self.load_stop_words() # 载入停用词表
        # self.build_index() # 建立倒排索引
        # self.build_index_with_json() # 建立倒排索引 using json files
        self.build_index_with_1json() # 建立倒排索引 using 1 json file
        self.compute_lengths() # 计算每个文档的长度


    def load_stop_words(self): # 载入停用词表
        file_path = os.path.join(os.path.dirname(__file__), 'stop_words.txt')
        with open(file_path, 'r', encoding='utf-8') as f: 
            for line in f: 
                self.stop_words.add(line.strip())

    def build_index_with_json(self): # 建立倒排索引
        for doc_id, file in enumerate(os.listdir(self.path)): # enumrate()函数用于将一个可遍历的数据对象组合为一个索引序列，同时列出数据和数据下标
            self.docs.append(file) 
            with open(os.path.join(self.path, file), 'r', encoding='utf-8') as f:
                data = json.load(f)
                tokens = data["content_seg"]
                for token in tokens: 
                    if token not in self.stop_words:
                        self.index[token][doc_id] = self.index[token].get(doc_id, 0) + 1

    def build_index_with_1json(self): # 建立倒排索引
        with open(os.path.join(self.path, 'douluo.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)
            for doc_id in range(len(data)):
                self.docs.append(data[doc_id]["headline"])
                tokens = data[doc_id]["content_seg"]
                for token in tokens: 
                    if token not in self.stop_words:
                        self.index[token][doc_id] = self.index[token].get(doc_id, 0) + 1

    # {'word': docname{doc_id: freq, doc_id: freq, ...}, ...}
    def build_index(self): # 建立倒排索引
        for doc_id, file in enumerate(os.listdir(self.path)): # enumrate()函数用于将一个可遍历的数据对象组合为一个索引序列，同时列出数据和数据下标
            self.docs.append(file) 
            with open(os.path.join(self.path, file), 'r', encoding='utf-8') as f:
                for line in f: 
                    tokens = line.strip().split()
                    for token in tokens: 
                        if token not in self.stop_words:
                            self.index[token][doc_id] = self.index[token].get(doc_id, 0) + 1

    def compute_lengths(self): # 计算文档长度
        for doc_id in range(len(self.docs)):
            length = 0 
            for term, freq in self.index.items(): # get (term, {doc_id: freq, doc_id: freq, ...})
                tf = freq.get(doc_id, 0) # term frequency
                idf = math.log(len(self.docs) / len(self.index[term])) # 计算单词的逆文档频率 = log(文档总数 / 包含该单词的文档数)
                if tf > 0:
                    length += ((1 + math.log(tf)) * idf * (1 + math.log(tf)) * idf) # 该文档长度为文档中所有单词频率对数之和  加1避免tf为1时tf_weight为0
            self.doc_length[doc_id] = math.sqrt(length) 
            self.total_length += length # 将文档长度加到所有文档总长度上

    def calculate_query_vector(self, query): # 计算查询向量
        query_vector = defaultdict(int)
        for term in query.strip().split():
            if term not in self.stop_words:
                query_vector[term] += 1
        length = math.sqrt(sum(map(lambda x: x*x, query_vector.values()))) # 计算查询向量的长度(模)  map()返回一个迭代器
        for term, freq in query_vector.items():
            query_vector[term] = freq / length # 单词的出现次数 / length = 单词的权重
        return query_vector # 返回查询向量

    def calculate_score(self, query, words_counter): # 计算文档得分
        query_vector = self.calculate_query_vector(query) # 得到查询向量
        scores = defaultdict(float)
        for term, freq in query_vector.items(): # (term, term_freq_in_query)
            if term in self.index:
                idf = math.log(len(self.docs) / len(self.index[term])) # 计算单词的逆文档频率 = log(文档总数 / 包含该单词的文档数)
                for doc_id, tf in self.index[term].items(): # (doc_id, term_freq_in_doc)
                    words_counter[doc_id][term] = tf # 记录每个文档中每个单词出线次数
                    tf_weight = 1 + math.log(tf) # 单词在文档中的权重 = 1 + log(单词频率)
                    scores[doc_id] += freq * tf_weight * idf / self.doc_length[doc_id] # 文档得分 = 查询向量中单词权重 * 文档中单词权重 * 逆文档频率 / 文档长度
        # for doc_id, score in scores.items():
            # scores[doc_id] *= self.total_length # 文档得分 = 文档得分 * 所有文档总长度
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True) # 对第二个元素排序
        return sorted_scores

    def search(self, query, num_results=5): # 查询
        query = cut_sentence(query) # 对查询分词
        words_counter = defaultdict(dict)
        print('匹配分词:', query)
        results = self.calculate_score(query, words_counter)[:num_results] # num_results个文档

        with open(os.path.join(self.path, 'douluo.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)
            ret = []
            for doc_id, score in results:
                record = {'title': [], 'url': [], 'matchRate': []}
                print(f.name)
                record['title'] = data[doc_id]["headline"]
                record['url'] = data[doc_id]["url"]
                record['matchRate'] = score
                ret.append(record)
                print('Document:', self.docs[doc_id])
                print('Score:', score)
                print(words_counter[doc_id])
            # with open(os.path.join(self.path, self.docs[doc_id]), 'r', encoding='utf-8') as f: # 打开文档
            #     print('Content:', f.readline().strip()) # 打印文档内容的第一行
                print('---' * 20)
        return ret

