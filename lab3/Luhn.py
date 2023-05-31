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
        self.stopwords = self.stopwords + ['cnn','new','Caption','photos','Hide','s','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','q','r','s','t','u','v','w','x','y','z','``',"'s"]

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
        # 存储每个句子的得分以及句子的索引
        notes = []
        # 句子的索引
        indice_sentence = 0
        # 对每个句子进行处理
        # 首先将每个句子转换为小写，使用nltk库的word_tokenize方法将句子分词为单词列表
        for sentence in [nltk.word_tokenize(sentence.lower()) for sentence in sentences]:
            indice_word = []
            # 获取句子中重要单词的索引位置
            for word in important_words:
                try:
                    indice_word.append(sentence.index(word))
                except ValueError:
                    pass
            # 确保索引位置按升序排列
            indice_word.sort()
            # 句子中没有重要单词，跳过
            if len(indice_word) == 0:
                continue
            # 存储根据距离将索引位置分组后的组
            list_groups = []
            group = [indice_word[0]]
            i = 1
            # 根据距离将索引位置分组
            while i < len(indice_word):
                if indice_word[i] - indice_word[i - 1] < self.distance:
                    # 将当前索引位置添加到group列表中
                    group.append(indice_word[i])
                else:
                    # 将当前的group列表添加到list_groups列表
                    list_groups.append(group[:])
                    # 创建一个新的group列表
                    group = [indice_word[i]]
                i += 1
            # 将最后的group列表添加到list_groups列表
            list_groups.append(group)
            # 存储最高得分的分组得分
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
        try:
            # 获取摘要的原始句子
            best_sentence = original_sentences[best_sentences[0][1]]
        except IndexError:
            # 如果索引错误，表示无法获取摘要句子，返回默认的错误信息
            best_sentence = "Failed to generate summary"
        # print(best_sentence)
        return best_sentence
        # # 获取摘要的原始句子
        # best_sentences = [original_sentences[i] for (note, i) in best_sentences]
        # return best_sentences[0]

# if __name__ == '__main__':
#     text = '''(CNN)Working in a factory or warehouse can mean doing the same task over and over, and that repetition can lead to chronic injury. Now, a battery-powered glove could help workers by taking some of the strain.The \"Ironhand\" glove strengthens the wearer's grip, meaning they don't have to use as much force to perform repetitive manual tasks. Its developer, Bioservo, says it can increase the wearer's hand strength by 20%. The Swedish company describes the system as a \"soft exoskeleton.\" Exoskeletons are an external device that supports and protects the body, typically increasing strength and endurance. Most have a rigid structure, but the Ironhand is soft, like a regular glove.  Photos: The robots running our warehousesRobots are an increasingly familiar presence in warehouses. At the south-east London warehouse run by British online supermarket Ocado, 3,000 robots fulfill shopping orders. When an order is sent to the warehouse, the bots spring to life and head towards the container they require. Scroll through to see more robots that are revolutionizing warehouses.Hide Caption 1 of 8 Photos: The robots running our warehousesIn response to the coronavirus pandemic, MIT collaborated with Ava Robotics and the Greater Boston Food Bank to design a robot that can use UV light to sanitize the floor of a 4,000-square foot warehouse in just 30 minutes. Hide Caption 2 of 8 Photos: The robots running our warehousesSeven-foot \"Model-T\" robots produced by Japanese startup Telexistence have been stacking shelves in two of Tokyo's largest convenience store franchises. Featuring cameras, microphones and sensors, the Model-T uses three \"fingers\" to stock items such as bottled drinks, cans and rice bowls. The robot is controlled by shop staff remotely.Hide Caption 3 of 8 Photos: The robots running our warehousesUS company Boston Dynamics has become known for its advanced work robots. \"Handle\" is made for the warehouse and equipped with an on-board vision system. It can lift boxes weighing over 30 pounds. Hide Caption 4 of 8 Photos: The robots running our warehousesStretch is the latest robot from Boston Dynamics and can work in warehouses and distribution centers. Designed to keep human workers out of harm's way, Stretch's tentacle-like grippers mean it can manipulate boxes. Hide Caption 5 of 8 Photos: The robots running our warehousesAlthough not specifically designed for warehouses, Boston Dynamics' dog-like robot \"Spot\" can lift objects, pick itself up after a fall, open and walk through doors, and even remind people to practice social distancing. Hide Caption 6 of 8 Photos: The robots running our warehousesThis robot is used to plant seeds and check plants at the \"Nordic Harvest\" vertical farm  based in Taastrup, Denmark. The indoor farm is one of the biggest in Europe.Hide Caption 7 of 8 Photos: The robots running our warehousesRobots sort packages at a warehouse run by JD.com -- one of China's largest e-commerce firms, in Wuhan, China, ahead of the annual Singles Day online shopping bonanza, in 2019.Hide Caption 8 of 8Reducing fatigue\"When you have the glove on, it provides strength and reduces the effort needed when lifting objects,\" says Mikael Wester, Bioservo's marketing director. \"It's all in order to reduce fatigue and prevent strain injuries in the long run.\"The Ironhand system was developed with General Motors as a partner.Read MoreThe system consists of a backpack, which houses the power pack, and artificial tendons that connect to the glove. There are sensors on each fingertip which switch on the motor when a user grabs an object. A remote control or app can be used to adjust the strength and sensitivity of the grip.Wester says applications include assembly on the production line in the automotive industry, using tools in construction and lifting heavy objects in warehouses.Each Ironhand system costs around \u20ac6,000 ($7,275). The device also collects data that allows the company to assess the wearer's risk of developing strain injuries.  According to the European Agency for Safety and Health at Work, work-related neck and upper limb disorders are the most common occupational disease in Europe, costing national economies up to 2% of their gross national product.From NASA to General Motors The glove was originally intended for workers in a very different setting to the factory floor. NASA developed an early version of the technology, called \"Robo-Glove,\" to help astronauts grasp objects and carry out work in space. The Ironhand system being used for assembling parts in the automobile industry. Bioservo licensed the design in 2016 and then partnered with auto manufacturer General Motors (GM) to develop the glove for its workers. Why online supermarket Ocado wants to take the human touch out of groceries\"Ergonomics is really the field of trying to fit the jobs to the workers, instead of the workers having to conform and adapt to the job,\" says Stephen Krajcarski, a senior manager with GM's ergonomics team.\"By using tools such as the Ironhand we are really trying to mitigate any potential concerns or physical demands that may eventually cause a medical concern for that individual operator.\"  Krajcarski says GM has helped Bioservo to test and improve the Ironhand by piloting it in a variety of jobs at its manufacturing plants. He says some workers have found it easy to use but adds that it's not suitable for all situations.The Ironhand is just one of the exoskeletons GM is looking into. According to market research firm ABI Research, the exoskeleton market will grow from $392 million in 2020 to $6.8 billion in 2030.\"If you look at exoskeletons, this is just one of the tools that are out there,\" says Krajcarski. \"But this is an exciting technology.\"This story has been updated to correct the cost of the Ironhand system.
    
#     '''
#     text_summarizer = TextSummarizer()
#     print(text_summarizer.summarize(text))
    # print(text_summarizer.summarize(text))