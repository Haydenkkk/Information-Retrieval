import json

def count_token_occurrences(obj, token):
    top_tokens = obj["Top Tokens"]
    token_counts = 0
    
    # 遍历 top_tokens 中的每个字段
    for category, sub_tokens in top_tokens.items():
        # 如果该字段是一个字典，则继续查找嵌套的子字段
        if isinstance(sub_tokens, dict):
            token_counts += sub_tokens.get(token, 0)
    
    return token_counts

def count_list_occurrences(obj, lst):
    token_counts = 0
    
    # 遍历列表中的每个元素
    for token in lst:
        token_counts += count_token_occurrences(obj, token)
    
    return token_counts


tokens = ['Russia', 'country', 'Europe', 'Asia']
with open('res.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
for obj in data:
    token_counts = count_list_occurrences(obj, tokens)
    if token_counts > 0:
            # print("标题：", obj['Title'])
            print("摘要：", obj['Summary'])