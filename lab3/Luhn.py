import nltk
import string
import heapq

# nltk.download('punkt')
# nltk.download('stopwords')

class TextSummarizer:
    def __init__(self, top_n_words=5, distance=3, number_sentences=1):
        self.top_n_words = top_n_words
        self.distance = distance
        self.number_sentences = number_sentences
        # 加载英语停用词列表
        self.stopwords = nltk.corpus.stopwords.words('english')
        self.stopwords = self.stopwords + ['cnn','new','Caption','Photos','Hide']

    def preprocessing(self,text):
        # 将文本转换为小写
        formatted_text = text.lower()
        tokens = []
        # 分词并过滤停用词和标点符号
        for token in nltk.word_tokenize(formatted_text):
            tokens.append(token)
        tokens = [word for word in tokens if word not in self.stopwords and word not in string.punctuation]
        # 过滤数字
        formatted_text = ' '.join([str(element) for element in tokens if not element.isdigit()])
        return formatted_text

    def calculate_sentence_score(self, sentences, important_words):
        notes = []
        indice_sentence = 0
        # 对每个句子进行处理
        for sentence in [nltk.word_tokenize(sentence.lower()) for sentence in sentences]:
            indice_word = []
            # 获取句子中重要单词的索引位置
            for word in important_words:
                try:
                    indice_word.append(sentence.index(word))
                except ValueError:
                    pass

            indice_word.sort()

            if len(indice_word) == 0:
                continue

            list_groups = []
            group = [indice_word[0]]
            i = 1
            # 根据距离将索引位置分组
            while i < len(indice_word):
                if indice_word[i] - indice_word[i - 1] < self.distance:
                    group.append(indice_word[i])
                else:
                    list_groups.append(group[:])
                    group = [indice_word[i]]
                i += 1
            list_groups.append(group)

            high_grade_group = 0
            # 计算每个分组的得分
            for g in list_groups:
                important_words_in_the_group = len(g)
                total_word_in_group = g[-1] - g[0] + 1

                note = 1.0 * important_words_in_the_group ** 2 / total_word_in_group

                if note > high_grade_group:
                    high_grade_group = note

            notes.append((high_grade_group, indice_sentence))
            indice_sentence += 1

        return notes
    
    def summarize(self,text):
        original_sentences = [sentence for sentence in nltk.sent_tokenize(text)]
        # 预处理句子
        formatted_sentences = [self.preprocessing(original_sentence) for original_sentence in original_sentences]
        words = [word for sentence in formatted_sentences for word in nltk.word_tokenize(sentence)]
        frequence = nltk.FreqDist(words)
        # 获取频率最高的单词作为重要单词
        top_n_words = [word[0] for word in frequence.most_common(self.top_n_words)]
        # 计算句子得分
        notes_sentences = self.calculate_sentence_score(formatted_sentences, top_n_words)
        # 选取得分最高的句子作为摘要
        best_sentences = heapq.nlargest(self.number_sentences, notes_sentences)
        # 获取摘要的原始句子
        best_sentences = [original_sentences[i] for (note, i) in best_sentences]
        return best_sentences[0]



# summarizer = TextSummarizer(top_n_words=5, distance=2, number_sentences=1)
# original_text = "docs/A 4th dose of Covid-19 vaccine will be needed, Pfizer's CEO says, but the company is working on a shot to handle all variants - CNN.txt"
# # 读取文件内容并解码为UTF-8编码
# original_text = open(original_text, 'rb').read().decode(encoding='utf-8')
# # 使用正则表达式将多个连续空白字符替换为单个空格
# original_text = re.sub(r'\s+', ' ', original_text)
# # 调用summarize函数生成摘要
# best_sentence = summarizer.summarize(original_text)
# print(best_sentence)
