import spacy
import json
import re
from Luhn import TextSummarizer
from multiprocessing.dummy import Pool as ThreadPool

# 加载spaCy模型
nlp = spacy.load("en_core_web_sm")
cnt = 0

def process_obj(obj):
    # 获取"Article text"字段的值
    text = obj["Article text"]

    # 使用spaCy处理文本
    doc = nlp(text)

    # 统计实体类型中每个token的出现次数
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
    summary = summarizer.summarize(text)
    if summary == "Failed to generate summary":
        return None

    obj["Summary"] = summary
    # 将处理结果添加到JSON对象中
    obj["Top Tokens"] = top_tokens
    print(f"已处理: {obj['Second headline']}")
    
    return obj

if __name__ == '__main__':
    # 打开JSON文件
    with open('CNN_Articels_clean_2.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    # distance参数：该参数控制着在计算句子得分时，两个重要单词之间允许的最大距离。
    # 较小的距离值将导致较长的重要短语被视为一个连续的组，并在计算得分时得到更高的权重。较大的距离值将使得算法更加宽松，接受较远的重要单词，并降低得分权重。
    # top_n_words参数：该参数决定了在计算句子得分时要考虑的重要单词的数量。
    # 较小的值将仅考虑最频繁出现的几个单词，从而生成较为精炼的摘要。较大的值将考虑更多的重要单词，可能导致生成较长的摘要。
    summarizer = TextSummarizer(top_n_words=3, distance=2, number_sentences=1)

    # 创建线程池
    pool = ThreadPool(processes=12)

    # 使用线程池并行处理每个JSON对象
    processed_data = pool.map(process_obj, data)

    # 关闭线程池
    pool.close()
    pool.join()

    # 过滤掉返回的None值
    processed_data = [obj for obj in processed_data if obj is not None]

    # 将更新后的JSON保存到文件
    # 37915
    with open('res_3.json', 'w', encoding='utf-8') as file:
        json.dump(processed_data, file, indent=4)

    print(f"共处理{len(processed_data)}个对象")
