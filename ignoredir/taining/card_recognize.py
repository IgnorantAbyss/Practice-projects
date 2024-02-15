from businesscard_ocr import businesscard_ocr
from label_processing import label_prediction

# 圖片文字辨識
texts = businesscard_ocr("card1.png")

model = 'ner_predict_model.h5'
# 實體分類
card_info = label_prediction(texts, model)

# print(card_info)

for key, value in card_info.items():
    print(key)
    print(value)


if 'PERSON' in card_info and card_info['PERSON']:
    print(f"姓名: {card_info['PERSON']}")
if 'ORG' in card_info and card_info['ORG']:
    print(f"公司: {card_info['ORG']}")
if 'POSITION' in card_info and card_info['POSITION']:
    print(f"職稱: {card_info['POSITION']}")
if 'PHONE' in card_info and card_info['PHONE']:
    print(f"電話: {card_info['PHONE']}")
if 'ADDRESS' in card_info and card_info['ADDRESS']:
    print(f"地址: {card_info['ADDRESS']}")
if 'Email' in card_info and card_info['Email']:
    print(f"信箱: {card_info['Email']}")
if 'Link' in card_info and card_info['Link']:
    print(f"網址: {card_info['Link']}")