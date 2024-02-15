import requests
import os

from businesscard_ocr import businesscard_ocr

def ChatGPT_prediction(filepath):
    # 辨識文本
    texts = businesscard_ocr(filepath)

    # 讀取API密鑰環境變數
    api_key = os.getenv('My_API')

    prompt = f"{texts}，按照Name,Job Title,Company Name,Address,Phone,Email,Link為我分類，嚴格審查Company Name，若無不要回傳"

    # 使用request模組串接API
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        },
        json = {
            'model': 'gpt-3.5-turbo', # 模型
            'messages' : [{"role": "user", "content": prompt}]
        })

    #使用json解析
    json = response.json()
    # print("\n" + json['choices'][0]['message']['content'])
    card_info = json['choices'][0]['message']['content']

    return card_info

if __name__ == "__main__":
    card_info = ChatGPT_prediction(r"E:\ner_model\bussiness_card\card1.png")
    print(card_info)