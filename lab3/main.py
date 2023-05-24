import spacy

nlp = spacy.load("en_core_web_sm")
def process_document(doc_text):
    doc = nlp(doc_text)

    # 构建NER结构
    ner_structure = []
    for ent in doc.ents:
        ner_structure.append({
            "text": ent.text,
            "label": ent.label_,
            "start_char": ent.start_char,
            "end_char": ent.end_char
        })
    return ner_structure

# 遍历每个文档进行处理
for doc_path in document_paths:
    with open(doc_path, "r") as f:
        doc_text = f.read()

    ner_structure = process_document(doc_text)

    # 将NER结构保存到文件或数据库中
    save_ner_structure(ner_structure)
