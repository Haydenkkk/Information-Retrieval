import json
import os
import re

json_data_list = []
output_file_path = '../doucments/DouLuo_Json/douluo1.json'

def remove_invalid_words(words):
    valid_words = []
    for word in words:
        if not re.match(r'^[\u4e00-\u9fa5]+$', word):
            continue
        valid_words.append(word)
    return valid_words


for file_name in os.listdir('../doucments/DouLuo_Json'):
    with open(os.path.join('../doucments/DouLuo_Json', file_name), 'r', encoding='utf-8') as file:
        if(file_name[0:7] != 'chapter'):
            print(file_name)
            continue
        json_data = json.load(file)
        words = json_data['content_seg']
        valid_words = remove_invalid_words(words)
        json_data["content_seg"] = valid_words
        json_data_list.append(json_data)
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(json_data_list, output_file, ensure_ascii=False, indent=4)
