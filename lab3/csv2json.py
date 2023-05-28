import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    # 读取CSV文件
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_data = csv.DictReader(csv_file)
        
        # 转换为JSON格式
        json_data = json.dumps([row for row in csv_data], indent=4)
        
        # 将JSON数据写入文件
        with open(json_file_path, 'w') as json_file:
            json_file.write(json_data)

# 示例用法
csv_file_path = 'data/CNN_Articels_clean_2.csv'  # CSV文件路径
json_file_path = 'CNN_Articels_clean_2.json'  # 输出的JSON文件路径

csv_to_json(csv_file_path, json_file_path)
