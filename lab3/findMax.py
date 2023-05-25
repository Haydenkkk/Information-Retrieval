import spacy
import json
import re
from summary import TextSummarizer

# 加载spaCy模型
nlp = spacy.load("en_core_web_sm")

# 打开JSON文件
with open('CNN_Articels_clean.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

summarizer = TextSummarizer(top_n_words=5, distance=2, number_sentences=1)
# 遍历JSON中的每个对象
for obj in data:
    # 获取"Article text"字段的值
    text = obj["Article text"]

    # 使用spaCy处理文本
    doc = nlp(text)

    # 统计实体类型中每个token的出现次数
    # PERSON：人名
    # NORP：民族、宗教或政治团体
    # FAC：建筑物、机构、机场等
    # ORG：组织机构、公司、政府等
    # GPE：地点、国家、城市等
    # LOC：非GPE地点，山脉、湖泊等
    # PRODUCT：产品名称
    # EVENT：事件名称
    # WORK_OF_ART：艺术作品，书籍、歌曲等
    # LAW：法律文件名
    # LANGUAGE：语言名称
    # DATE：日期
    # TIME：时间
    # PERCENT：百分比
    # MONEY：货币金额
    # QUANTITY：数量
    # ORDINAL：顺序词，第一、第二等
    # CARDINAL：基数词，数字
    entity_counts = {
        "PERSON": {}, "NORP": {}, "FAC": {}, "ORG": {}, "GPE": {}, "LOC": {}, "PRODUCT": {},
        "EVENT": {}, "WORK_OF_ART": {}, "LANGUAGE": {}, "DATE": {}, "TIME": {}, "MONEY": {}
    }
    for ent in doc.ents:
        if ent.label_ in entity_counts:
            token_counts = entity_counts[ent.label_]
            token_counts[ent.text] = token_counts.get(ent.text, 0) + 1

    # 获取每个实体类型中出现频率最高的两个token
    top_tokens = {}
    for label, counts in entity_counts.items():
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        top_tokens[label] = {token: count for token, count in sorted_counts[:2] if count > 1}
    text = re.sub(r'\s+', ' ', text)
    obj["Summary"] = summarizer.summarize(text)
    # 将处理结果添加到JSON对象中
    obj["Top Tokens"] = top_tokens
    print(f"已处理: {obj['Headline']}")
    # print(f"Top Tokens: {top_tokens}")
# 将更新后的JSON保存到文件
with open('res.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4)
