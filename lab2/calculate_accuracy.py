import json
import random
import os
from main import RetrievalModel

words_num = 20
total_chapters = 0
find_chapters = 0
if (__name__ == '__main__'):
    model = RetrievalModel('../doucments/DouLuo_Json')
    with open('../doucments/DouLuo_Json/douluo.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        total_chapters = len(data)
        print("total_chatpers:", total_chapters)
        for i in range(total_chapters):
            print("\n\n")
            print("search in chapter:", data[i]["headline"])
            words = []
            count = 0
            while(count < words_num):
                word = data[i]["content_seg"][random.randint(4, len(data[i]["content_seg"]) - 1)]
                if(word not in model.stop_words):
                    words.append(word)
                    count = count + 1
            words = str(words)
            print("search words:", words)
            result = model.search(words, 5)
            for res in result:
                if(res["header"] == data[i]["headline"]):
                    find_chapters = find_chapters + 1
                    print("match chapter:", data[i]["headline"])
                    print("url:", data[i]["url"])
                    print("score:", res["score"])
                    break
    print("===============================================")
    print("检索章节数:", total_chapters)
    print("检索匹配章节数:", find_chapters)
    print("检索准确率:", find_chapters / total_chapters * 100, "%")
    print("===============================================")