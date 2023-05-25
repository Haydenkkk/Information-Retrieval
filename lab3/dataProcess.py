import json
import re
json_file = 'CNN_Articels_clean.json'

# 从JSON文件中获取文章文本
def getTxt(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    cnt = 0
    # 遍历每个JSON对象
    for item in data:
        headline = item['Headline']
        article_text = item['Article text']
        
        # 清理文件名中的无效字符
        cleaned_headline = re.sub(r'[<>:"/\\|?*]', '', headline)
        
        # 判断文章文本是否为空
        if article_text:
            # 将文章文本保存到文件
            with open(f'docs/{cleaned_headline}.txt', 'wb') as article_file:
                article_file.write(article_text.encode('utf-8'))
                cnt+=1
            print(f"已将文章文本保存为文件: {cleaned_headline}.txt")
        else:
            print(f"文章文本为空，跳过保存文件: {cleaned_headline}")