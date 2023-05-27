import numpy as np
from keras.models import load_model
from keras.models import Model
from keras.layers import Input

# max_text_len = 100

model = load_model('model/model.h5')

# 编码器模型
encoder_inputs = model.input[0]
encoder_outputs, state_h, state_c = model.layers[7].output  # 根据模型结构中编码器的位置确定层的索引
encoder_model = Model(inputs=encoder_inputs, outputs=[encoder_outputs, state_h, state_c])

# 解码器模型
latent_dim = 300  # 解码器的隐藏状态维度，需要和训练时设置的值保持一致
decoder_state_input_h = Input(shape=(latent_dim,))
decoder_state_input_c = Input(shape=(latent_dim,))
decoder_hidden_state_input = Input(shape=(max_text_len, latent_dim))
decoder_inputs = model.input[1]
dec_emb_layer = model.layers[3]  # 根据模型结构中嵌入层的位置确定层的索引
dec_emb = dec_emb_layer(decoder_inputs)
decoder_lstm = model.layers[8]  # 根据模型结构中解码器LSTM层的位置确定层的索引
decoder_outputs, state_h2, state_c2 = decoder_lstm(dec_emb, initial_state=[decoder_state_input_h, decoder_state_input_c])
decoder_dense = model.layers[9]  # 根据模型结构中解码器全连接层的位置确定层的索引
decoder_outputs = decoder_dense(decoder_outputs)
decoder_model = Model(inputs=[decoder_inputs] + [decoder_hidden_state_input, decoder_state_input_h, decoder_state_input_c],
                      outputs=[decoder_outputs] + [state_h2, state_c2])

input_seq = ...  # 准备好的输入序列
encoder_outputs, encoder_state_h, encoder_state_c = encoder_model.predict(input_seq)

target_seq = np.zeros((1, 1))
target_seq[0, 0] = target_word_index['sostok']  # 设置目标序列的起始标记

stop_condition = False
decoded_sentence = ''
while not stop_condition:
    output_tokens, decoder_state_h, decoder_state_c = decoder_model.predict([target_seq] + [encoder_outputs, encoder_state_h, encoder_state_c])
    sampled_token_index = np.argmax(output_tokens[0, -1, :])
    sampled_token = reverse_target_word_index[sampled_token_index]
    if sampled_token == 'eostok':
        stop_condition = True
    else:
        decoded_sentence += ' ' + sampled_token
    target_seq = np.zeros((1, 1))
    target_seq[0, 0] = sampled_token_index
    encoder_state_h, encoder_state_c = decoder_state_h, decoder_state_c

print("Generated Sentence:", decoded_sentence)


