import spacy
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TokenAnalyzer:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.data = None

    def load_data(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

    def count_token_occurrences(self, obj, token):
        top_tokens = obj["Top Tokens"]
        token_counts = 0

        # 遍历 top_tokens 中的每个字段
        for category, sub_tokens in top_tokens.items():
            # 如果该字段是一个字典，则继续查找嵌套的子字段
            if isinstance(sub_tokens, dict):
                token_counts += sub_tokens.get(token, 0)

        return token_counts

    def count_list_occurrences(self, obj, lst):
        token_counts = 0
        # 遍历列表中的每个元素
        for token in lst:
            token_counts += self.count_token_occurrences(obj, token)
        return token_counts

    def extract_keywords(self, sentence):
        doc = self.nlp(sentence)
        keywords = [token.text for token in doc if not token.is_stop and not token.is_punct]
        return keywords

    def calculate_match_rate(self, keywords, summary):
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
        print("关键词：", keywords)

        # 创建一个列表来保存结果
        results = []

        for obj in self.data:
            match_rate = self.calculate_match_rate(keywords, obj['Summary'])
            token_counts = self.count_list_occurrences(obj, keywords)
            if token_counts > 0:
                results.append((obj, token_counts, match_rate))

        # 根据 token_counts 进行排序，获取前十个结果
        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)[:10]

        # 打印结果
        for result in sorted_results:
            obj, token_counts, match_rate = result
            print("Token Counts:", token_counts, end=" \t\t")
            print("Match Rate:", match_rate)
            print(obj["Url"])  # 输出匹配到的对象信息

# 创建 TokenAnalyzer 实例
analyzer = TokenAnalyzer()
# 加载数据
analyzer.load_data('res.json')
# 获取结果
analyzer.get_results("Russia Ukraine")
