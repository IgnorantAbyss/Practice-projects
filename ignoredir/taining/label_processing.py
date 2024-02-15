import re
import pickle
import numpy as np
from tensorflow.keras.models import load_model


from text_preprocessing import text_preprocessing

def email_link_preprocessing(texts):

    card_info = {'Email': [], 'Link': []}
    texts = texts.split("\n")
    newtexts = [i.strip() for i in texts if len(i) != 0]

    for text in newtexts:
        # 匹配電子郵件地址
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            card_info['Email'].append(text)
        # 匹配網址
        elif re.search(r'(http[s]?://)?[www\.]?[A-Za-z0-9.-]+\.[A-Za-z]{2,}', text):
            card_info['Link'].append(text)

    newtexts = [text for text in newtexts if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)]
    newtexts = [text for text in newtexts if not re.search(r'(http[s]?://)?[www\.]?[A-Za-z0-9.-]+\.[A-Za-z]{2,}', text)]

    return card_info, newtexts



def label_prediction(texts, model_name):
    # 加載 label_encoder
    with open('label_encoder.pkl', 'rb') as file:
        label_encoder = pickle.load(file)

    # 先處理Email & Link
    card_info = {'Email': [], 'Link': []}
    texts = texts.split("\n")
    newtexts = [i.strip() for i in texts if len(i) != 0]

    for text in newtexts:
        # 匹配電子郵件地址
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            card_info['Email'].append(text)
        # 匹配網址
        elif re.search(r'(http[s]?://)?[www\.]?[A-Za-z0-9.-]+\.[A-Za-z]{2,}', text):
            card_info['Link'].append(text)

    # 若有符合Email & Link則剔除
    newtexts = [text for text in newtexts if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)]
    newtexts = [text for text in newtexts if not re.search(r'(http[s]?://)?[www\.]?[A-Za-z0-9.-]+\.[A-Za-z]{2,}', text)]

    # 文本預處理
    pad_data = text_preprocessing(newtexts)

    # 載入模型
    model = load_model(model_name)

    # 進行預測
    predictions = model.predict(pad_data)

    # 將預測結果轉換為標籤
    predicted_labels = label_encoder.inverse_transform(np.argmax(predictions, axis=1))

    # 輸出預測結果
    for i, text in enumerate(newtexts):
        if predicted_labels[i] not in card_info:
            card_info[str(predicted_labels[i])] = [text]
        else:
            card_info[str(predicted_labels[i])].append(text)

    return card_info


    
# if "__main__" == __name__:
#     texts = """MICHAL JOHNS
#     Solution Manager
#     COMPANY LOGO
#     SLOGANGOESHERE
#     +000 12345 6789
#     +000 12345 6789
#     urname@email.com
#     urwebsitename.com
#     Street Address Here
#     Singapore, 2222"""

#     card_info, newtexts = email_link_preprocessing(texts)

#     print(card_info)
#     print(newtexts)