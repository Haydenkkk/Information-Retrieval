import spacy
from spacy import displacy
import os

nlp = spacy.load("en_core_web_sm")

def process_document(doc_text):
    doc = nlp(doc_text)
    # 构建NER结构
    ner_structure = []
    entity_counts = {
                    "PERSON": {}, "NORP":{} , "FAC": {}, "ORG": {}, "GPE": {}, "LOC": {}, "PRODUCT": {},
                    "EVENT": {}, "WORK_OF_ART": {}, "LANGUAGE": {}, "DATE": {}, "TIME": {}, "MONEY": {}
                }
    for ent in doc.ents:
        if ent.label_ in entity_counts:
            entity_counts[ent.label_][ent.text] = entity_counts[ent.label_].get(ent.text, 0) + 1

    top_tokens = {}
    for label, counts in entity_counts.items():
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        top_tokens[label] = sorted_counts[:2]
        
    for ent in doc.ents:
        print(ent.text, ent.label_)
        ner_structure.append({
            "text": ent.text,
            "label": ent.label_,
            "start_char": ent.start_char,
            "end_char": ent.end_char
        })
    return ner_structure

current_folder = os.getcwd()
folder_path = os.path.join(current_folder, "docs")
for file_name in os.listdir(folder_path):
    # 构建文件的完整路径
    file_path = os.path.join(folder_path, file_name)
    # 检查文件是否为普通文件
    if os.path.isfile(file_path):
        # 读取文件内容
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        # 使用spaCy处理文件内容
        ner_structure = process_document(text)


# displacy.serve(doc, style="ent")