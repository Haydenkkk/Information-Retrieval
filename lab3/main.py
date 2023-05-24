import spacy
from spacy import displacy
import csv
import json
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
# 构建相对目录下的文件路径
relative_path = '../doucments'
file_path = os.path.join(current_directory, relative_path,'CNN_Articels_clean.csv')
my_json = {}
with open(file_path, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Use one of the CSV column names as a key
        key = row['Index']
        my_json[key] = row 

json_file = os.path.join(current_directory, relative_path,'CNN_Articels_clean.json') 
with open(json_file,'w') as fobj:
    fobj.write(json.dumps(my_json, indent=2))





nlp = spacy.load("en_core_web_sm")
text = 'Russian Defence Minister Sergei Shoigu has promised a "harsh response" to cross-border incursions from Ukraine.His comments came after Moscow said it had defeated an attack in the Belgorod region.However, regional governor Vyacheslav Gladkov said there had been a "large number" of drone attacks overnight.Ukraine denies involvement in the raid - and two Russian paramilitary groups opposed to Russian President Vladimir Putin say they were behind it.Attackers entered Russian territory from Ukraine on Monday.Reporting to defence ministry officials on the incursion, Mr Shoigu said "more than 70 Ukrainian nationalists" had been killed and the rest pushed back into Ukraine."We will continue to respond to such actions by Ukrainian militants promptly and extremely harshly," he said.The two Russian paramilitary groups - the Russian Volunteer Corps (RDK) and Liberty of Russia Legion (LSR) denied that they had sustained any casualties, and said a Russian motorised rifle company had been destroyed.The casualty claims by the warring sides have not been independently verified.Russia also says that Western military vehicles were used in the incursion.It posted pictures of destroyed US vehicles apparently at the scene of the fighting but some Ukrainian military experts and bloggers have suggested they could have been staged.The US said it was sceptical that reports of US-supplied weapons being used in the incursion were true and did not "encourage or enable strikes inside of Russia".But Kremlin spokesman Dmitry Peskov said the vehicles were evidence of growing Western military involvement in Ukraine."It is no secret for us that more and more equipment is being delivered to Ukraine'
doc = nlp(text)
def process_document(doc_text):
    doc = nlp(doc_text)
    # 构建NER结构
    ner_structure = []
    for ent in doc.ents:
        print(ent.text, ent.label_)
        ner_structure.append({
            "text": ent.text,
            "label": ent.label_,
            "start_char": ent.start_char,
            "end_char": ent.end_char
        })
    return ner_structure

# 遍历每个文档进行处理
# for doc_path in document_paths:
#     with open(doc_path, "r") as f:
#         doc_text = f.read()

#     ner_structure = process_document(doc_text)

#     # 将NER结构保存到文件或数据库中
#     save_ner_structure(ner_structure)
# process_document("Binary weights for the part-of-speech tagger, dependency parser and named entity recognizer to predict those annotations in context.")
# print(process_document(text))
# displacy.serve(doc, style="ent")