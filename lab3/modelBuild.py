from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
# from keras.preprocessing.sequence import pad_sequences

post_pre = pd.read_csv('post_pre.csv')
max_text_len = 1000
max_summary_len = 35

# 划分训练集和验证集
x_tr, x_val, y_tr, y_val = train_test_split(np.array(post_pre['text']), np.array(post_pre['summary']), test_size=0.1,
											random_state=0, shuffle=True)
# print(list(x_tr))
x_tr = [str(x) for x in x_tr]
x_val = [str(x) for x in x_val]
y_tr = [str(x) for x in y_tr]
y_val = [str(x) for x in y_val]
# 为训练数据准备一个标记器
x_tokenizer = Tokenizer()
x_tokenizer.fit_on_texts(list(x_tr))
thresh = 4

cnt = 0
tot_cnt = 0
freq = 0
tot_freq = 0

# 统计词频
for key, value in x_tokenizer.word_counts.items():
	tot_cnt = tot_cnt + 1
	tot_freq = tot_freq + value
	if value < thresh:
		cnt = cnt + 1
		freq = freq + value

print("词汇表中罕见单词的百分比:", (cnt / tot_cnt) * 100)
print("罕见单词的总覆盖率:", (freq / tot_freq) * 100)

# 为训练数据准备一个标记器
x_tokenizer = Tokenizer(num_words=tot_cnt - cnt)
x_tokenizer.fit_on_texts(list(x_tr))

# 将文本序列转换为整数序列（即对所有单词进行独热编码）
x_tr_seq = x_tokenizer.texts_to_sequences(x_tr)
x_val_seq = x_tokenizer.texts_to_sequences(x_val)

# 对序列进行填充，补0到最大长度
x_tr = pad_sequences(x_tr_seq, maxlen=max_text_len, padding='post')
x_val = pad_sequences(x_val_seq, maxlen=max_text_len, padding='post')

# 词汇表大小（+1 用于填充标记）
x_voc = x_tokenizer.num_words + 1

print("X中的词汇表大小 = {}".format(x_voc))

# 为训练数据准备一个标记器
y_tokenizer = Tokenizer()
y_tokenizer.fit_on_texts(list(y_tr))
thresh = 6

cnt = 0
tot_cnt = 0
freq = 0
tot_freq = 0

# 统计词频
for key, value in y_tokenizer.word_counts.items():
	tot_cnt = tot_cnt + 1
	tot_freq = tot_freq + value
	if value < thresh:
		cnt = cnt + 1
		freq = freq + value

print("词汇表中罕见单词的百分比:", (cnt / tot_cnt) * 100)
print("罕见单词的总覆盖率:", (freq / tot_freq) * 100)

# 为训练数据准备一个标记器
y_tokenizer = Tokenizer(num_words=tot_cnt - cnt)
y_tokenizer.fit_on_texts(list(y_tr))

# 将文本序列转换为整数序列（即对文本进行独热编码）
y_tr_seq = y_tokenizer.texts_to_sequences(y_tr)
y_val_seq = y_tokenizer.texts_to_sequences(y_val)

# 对序列进行填充，补0到最大长度
y_tr = pad_sequences(y_tr_seq, maxlen=max_summary_len, padding='post')
y_val = pad_sequences(y_val_seq, maxlen=max_summary_len, padding='post')

# 词汇表大小
y_voc = y_tokenizer.num_words + 1
print("Y中的词汇表大小 = {}".format(y_voc))

ind = []
# 删除长度为2的序列
for i in range(len(y_tr)):
	cnt = 0
	for j in y_tr[i]:
		if j != 0:
			cnt = cnt + 1
	if cnt == 2:
		ind.append(i)

y_tr = np.delete(y_tr, ind, axis=0)
x_tr = np.delete(x_tr, ind, axis=0)

ind = []
# 删除长度为2的序列
for i in range(len(y_val)):
	cnt = 0
	for j in y_val[i]:
		if j != 0:
			cnt = cnt + 1
	if cnt == 2:
		ind.append(i)

y_val = np.delete(y_val, ind, axis=0)
x_val = np.delete(x_val, ind, axis=0)

from keras import backend as K
# import gensim
from numpy import *
import numpy as np
import pandas as pd
import re
# from bs4 import BeautifulSoup
from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords
from keras.layers import Input, LSTM, Embedding, Dense, Concatenate, TimeDistributed
from keras.models import Model
from keras.callbacks import EarlyStopping
import warnings
from matplotlib import pyplot

# 设置显示的最大列宽
pd.set_option("display.max_colwidth", 200)
# 忽略警告信息
warnings.filterwarnings("ignore")

print("Size of vocabulary from the w2v model = {}".format(x_voc))

# 清除之前的模型，释放内存
K.clear_session()

latent_dim = 300
embedding_dim = 200

# 编码器
encoder_inputs = Input(shape=(max_text_len,))
enc_emb = Embedding(x_voc, embedding_dim, trainable=True)(encoder_inputs)
encoder_lstm1 = LSTM(latent_dim, return_sequences=True, return_state=True, dropout=0.4, recurrent_dropout=0.4)
encoder_output1, state_h1, state_c1 = encoder_lstm1(enc_emb)
encoder_lstm2 = LSTM(latent_dim, return_sequences=True, return_state=True, dropout=0.4, recurrent_dropout=0.4)
encoder_output2, state_h2, state_c2 = encoder_lstm2(encoder_output1)
encoder_lstm3 = LSTM(latent_dim, return_state=True, return_sequences=True, dropout=0.4, recurrent_dropout=0.4)
encoder_outputs, state_h, state_c = encoder_lstm3(encoder_output2)

# 解码器
decoder_inputs = Input(shape=(None,))
dec_emb_layer = Embedding(y_voc, embedding_dim, trainable=True)
dec_emb = dec_emb_layer(decoder_inputs)
decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True, dropout=0.4, recurrent_dropout=0.2)
decoder_outputs, decoder_fwd_state, decoder_back_state = decoder_lstm(dec_emb, initial_state=[state_h, state_c])
decoder_dense = TimeDistributed(Dense(y_voc, activation='softmax'))
decoder_outputs = decoder_dense(decoder_outputs)

# 定义模型
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

model.summary()
model.compile(optimizer='rmsprop', loss='sparse_categorical_crossentropy')
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=2)
history = model.fit([x_tr, y_tr[:, :-1]], y_tr.reshape(y_tr.shape[0], y_tr.shape[1], 1)[:, 1:], epochs=10,
                    callbacks=[es], batch_size=512,
                    validation_data=([x_val, y_val[:, :-1]], y_val.reshape(y_val.shape[0], y_val.shape[1], 1)[:, 1:]))
model.save("model/model.h5")

# 绘制损失曲线
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()

reverse_target_word_index = y_tokenizer.index_word
reverse_source_word_index = x_tokenizer.index_word
target_word_index = y_tokenizer.word_index

# 编码器模型
encoder_model = Model(inputs=encoder_inputs, outputs=[encoder_outputs, state_h, state_c])

# 解码器模型
decoder_state_input_h = Input(shape=(latent_dim,))
decoder_state_input_c = Input(shape=(latent_dim,))
decoder_hidden_state_input = Input(shape=(max_text_len, latent_dim))
dec_emb2 = dec_emb_layer(decoder_inputs)
decoder_outputs2, state_h2, state_c2 = decoder_lstm(dec_emb2, initial_state=[decoder_state_input_h, decoder_state_input_c])
decoder_outputs2 = decoder_dense(decoder_outputs2)
decoder_model = Model(
    [decoder_inputs] + [decoder_hidden_state_input, decoder_state_input_h, decoder_state_input_c],
    [decoder_outputs2] + [state_h2, state_c2])

# 解码器函数
def decode_sequence(input_seq):
    e_out, e_h, e_c = encoder_model.predict(input_seq)
    target_seq = np.zeros((1, 1))
    target_seq[0, 0] = target_word_index['sostok']
    stop_condition = False
    decoded_sentence = ''
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict([target_seq] + [e_out, e_h, e_c])
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_token = reverse_target_word_index[sampled_token_index]
        if sampled_token != 'eostok':
            decoded_sentence += ' ' + sampled_token
        if sampled_token == 'eostok' or len(decoded_sentence.split()) >= (max_summary_len-1):
            stop_condition = True
        target_seq = np.zeros((1, 1))
        target_seq[0, 0] = sampled_token_index
        e_h, e_c = h, c
    return decoded_sentence

# 将序列转换为摘要文本
def seq2summary(input_seq):
    newString = ''
    for i in input_seq:
        if (i != 0 and i != target_word_index['sostok']) and i != target_word_index['eostok']:
            newString = newString + reverse_target_word_index[i] + ' '
    return newString

# 将序列转换为原始文本
def seq2text(input_seq):
    newString = ''
    for i in input_seq:
        if i != 0:
            newString = newString + reverse_source_word_index[i] + ' '
    return newString

# 预测和打印结果
for i in range(0, 100):
    print("Review:", seq2text(x_tr[i]))
    print("Original summary:", seq2summary(y_tr[i]))
    print("Predicted summary:", decode_sequence(x_tr[i].reshape(1, max_text_len)))
    print("\n")