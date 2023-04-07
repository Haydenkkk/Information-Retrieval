# 对文件中中文句子进行分词：

import jieba
import os

def cut_file(file_path, save_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == '':
                continue
            seg_list = jieba.cut(line)
            seg_list = ' '.join(seg_list)
            with open(save_path, 'a', encoding='utf-8') as f:
                f.write(seg_list + ' ') 

def cut_sentence(sentence):
    seg_list = jieba.cut(sentence)
    seg_list = ' '.join(seg_list)
    return seg_list

# if __name__ == '__main__':
#     #将HongLouMeng文件夹中每一个文件中的句子分词后写入HongLouMeng_seg文件夹中
#     file_path = 'DouLuoDaLu'
#     save_path = 'DouLuoDaLu_seg'
#     if not os.path.exists(save_path):
#         os.mkdir(save_path)
#     for file in os.listdir(file_path):
#         cut_file(os.path.join(file_path, file), os.path.join(save_path, file))
    
    # print(cut_sentence('林黛玉进贾府'))
    