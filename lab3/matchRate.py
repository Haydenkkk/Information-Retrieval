import spacy
import json
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TokenAnalyzer:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.data = None

    def load_data(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

    def count_list_occurrences(self, obj, lst):
        token_counts = 0
        # 遍历列表中的每个元素
        for token in lst:
            token = token.lower()  # 将关键词转换为小写
            token_counts += self.count_token_occurrences(obj, token)
        return token_counts

    def count_token_occurrences(self, obj, token):
        top_tokens = obj["Top Tokens"]
        # token = token.lower()  # 将关键词转换为小写
        token_counts = 0

        # 遍历 top_tokens 中的每个字段
        for category, sub_tokens in top_tokens.items():
            # 如果该字段是一个字典，则继续查找嵌套的子字段
            if isinstance(sub_tokens, dict):
                for sub_token, count in sub_tokens.items():
                    if sub_token.lower() == token:  # 将子字段的键转换为小写进行比较
                        token_counts += count

        return token_counts

    def extract_keywords(self, sentence):
        doc = self.nlp(sentence)
        keywords = [token.text for token in doc if not token.is_stop and not token.is_punct]
        return keywords

    def calculate_match_rate(self, keywords, summary):
        summary = summary.lower()  # 将摘要转换为小写
        keywords = [keyword.lower() for keyword in keywords]  # 将关键词列表转换为小写

        summary_keywords = self.extract_keywords(summary)
        summary_keywords = ' '.join(summary_keywords)
        # 将关键词组合成一个列表
        sentence_keywords = ' '.join(keywords)
        documents = [sentence_keywords, summary_keywords]
        # 创建一个TF-IDF向量化器
        vectorizer = TfidfVectorizer()
        # 将关键词转换为TF-IDF特征向量
        tfidf_matrix = vectorizer.fit_transform(documents)
        # 计算余弦相似度
        similarity_matrix = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
        # 提取相似度值
        match_rate = similarity_matrix[0][0]
        return match_rate

    def get_results(self, query):
        if not self.data:
            raise ValueError("Data not loaded. Please load the data using 'load_data' method.")
        
        keywords = self.extract_keywords(query)
        print(keywords)
        
        # 创建一个列表来保存结果
        results = []
        
        # 遍历数据，找到最token_counts > 0 的  token_counts 的 obj
        top_objs = []
        for obj in self.data:
            token_counts = self.count_list_occurrences(obj, keywords)
            if token_counts > 0:
                top_objs.append((obj, token_counts))
        
        # 根据 token_counts 进行排序，获取最大的 50 个对象
        sorted_objs = sorted(top_objs, key=lambda x: x[1], reverse=True)[:50]

        # 计算匹配率权重
        max_token_counts = max([count for _, count in sorted_objs])
        weights = [math.exp(token_counts / max_token_counts) for _, token_counts in sorted_objs]
        total_weight = sum(weights)
        normalized_weights = [weight / total_weight for weight in weights]

        # 对最大的 50 个对象进行 calculate_match_rate 并添加到结果列表
        for (obj, token_counts), weight in zip(sorted_objs, normalized_weights):
            match_rate = self.calculate_match_rate(keywords, obj['Summary'])
            # 综合考虑 match_rate 和 token_counts 权重，并确保最终的 matchRate 不超过 100%
            match_rate = min(1.0, match_rate*weight*100) if match_rate > 0 else min(1.0, weight*4.5)
            
            result = {
                'title': obj["Second headline"],
                'summary': obj['Summary'],
                'matchRate': "{:.2%}".format(match_rate),
                'url': obj['Url']
            }
            results.append(result)
        
        # 根据 matchRate 进行排序，获取前三个结果
        sorted_results = sorted(results, key=lambda x: float(x['matchRate'].rstrip('%')), reverse=True)[:3]
        
        return sorted_results


