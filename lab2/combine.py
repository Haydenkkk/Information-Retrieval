import json
import os

json_data_list = []
output_file_path = '../doucments/DouLuo_Json/douluo.json'

for file in os.listdir('../doucments/DouLuo_Json'):
    with open(os.path.join('../doucments/DouLuo_Json', file), 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        json_data_list.append(json_data)
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(json_data_list, output_file, ensure_ascii=False, indent=4)
