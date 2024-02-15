import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

with open(r'ner_tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

def text_preprocessing(texts):
    # 將文本轉換為序列
    sequences = tokenizer.texts_to_sequences(texts)

    # 使用 pad_sequences 來確保序列具有相同的長度
    pad_data = pad_sequences(sequences, maxlen=50)

    return pad_data
