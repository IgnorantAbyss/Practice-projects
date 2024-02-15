import pytesseract
import cv2
import requests
import os
import re
import pickle
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

# 設置Tesseract OCR的可執行文件路徑（根據你的安裝位置）
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 繪製標線
def drawboxes(image,x,y,w,h):
    # image_y = image.shape[0] - (y + h)
                        # 左上      右下            顏色      粗細
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# 圖片辨識、文字提取
def businesscard_ocr(card_path):
    # 開啟要進行OCR的圖像文件
    image = cv2.imread(card_path)
    # 將圖像轉換為灰度
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    new_width = int(image.shape[1] * 2)
    new_height = int(image.shape[0] * 2)
    new_dimensions = (new_width, new_height)

    gray = cv2.resize(gray, new_dimensions, interpolation=cv2.INTER_LINEAR)
    image = cv2.resize(image, new_dimensions, interpolation=cv2.INTER_LINEAR)

    # 使用Tesseract識別文本，並獲取詳細信息
    result = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT, config='--oem 3 --psm 6')

    # 提取信心分數、文本內容和座標信息
    confidences = result['conf']
    texts = result['text']
    lefts = result['left']
    tops = result['top']
    widths = result['width']
    heights = result['height']

    # 設定信心分數臨界值
    confidence_threshold = 70

    # 初始化用於合併同一行文本的變數
    current_line = ""
    current_line_y = None
    square_width = None
    current_line_x = None

    card_text = """"""

    # 遍歷每個識別文本
    for i in range(len(texts)):
        text = texts[i]
        confidence = float(confidences[i])
        x = int(lefts[i])
        y = int(tops[i])
        width = int(widths[i])
        height = int(heights[i])

        # 如果信心分數高於閾值，保留座標和文本
        if confidence >= confidence_threshold and len(text) > 1:
            # 檢查是否屬於同一行文本
            if current_line_y is None:
                # 第一個文本
                current_line = text
                current_line_y = y
                current_line_x = x
                square_width = width
                square_height = height
                right_top_x = x + width
            
            elif abs(y - current_line_y) < (new_height / 50) and abs(x - right_top_x) < (new_width / 10):
                # 在同一行的文本，合併到同一行
                current_line += " " + text
                #判斷文字框位置前後
                if x < current_line_x:
                    # 新文本塊在當前行辨識框的左側，更新起始 x 坐標和寬度
                    square_width += current_line_x - x
                    current_line_x = x
                else:
                    right_top_x = x + width
                
                # 更新辨識框的寬度
                right_edge = max(right_top_x, x + width)
                square_width = right_edge - current_line_x
                
                # 檢查並更新辨識框的高度
                bottom_edge = max(current_line_y + square_height, y + height)
                square_height = bottom_edge - current_line_y

                # 更新辨識框的右邊界
                right_top_x = right_edge
            
            else:
                # 不在同一行，處理之前的同一行文本，然後重新開始新的一行
                drawboxes(image, current_line_x - 3, current_line_y, square_width + 3, square_height)
                # print(f"合併文本: {current_line}")
                # print(f"{current_line}")

                card_text += current_line + "\n"
                current_line = text
                current_line_y = y
                current_line_x = x
                square_width = width
                square_height = height
                right_top_x = x + width

    # 最後一行文本
    if current_line:
        # print(f"合併文本: {current_line}")
        # print(f"{current_line}")
        card_text += current_line
        drawboxes(image, current_line_x - 3, current_line_y, square_width + 3, square_height)


    # 顯示圖像
    cv2.imshow('Image with Text Boxes', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return card_text

# if "__main__" == __name__:
    
#     card_text = businesscard_ocr(r"E:\ner_model\bussiness_card\card1.png")
#     print(card_text)


# 以ChatGPT進行分類
def ChatGPT_prediction(filepath):
    # 辨識文本
    texts = businesscard_ocr(filepath)

    # 讀取API密鑰環境變數
    api_key = os.getenv('My_API')

    prompt = f"{texts}，勿翻譯原文，按照原文順序進行以下欄位分類:姓名,職稱,公司名稱,地址,電話,Email,網址，嚴格審查公司名稱，若無不要回傳"

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

# if __name__ == "__main__":
#     card_info = ChatGPT_prediction(r"E:\ner_model\bussiness_card\card1.png")
#     print(card_info)


# 將Email、網址進行預處理
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


# 讀取tokenizer
with open(r'./encoder_tokenizer/ner_tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# 文本預處理
def text_preprocessing(texts):
    # 將文本轉換為序列
    sequences = tokenizer.texts_to_sequences(texts)

    # 使用 pad_sequences 來確保序列具有相同的長度
    pad_data = pad_sequences(sequences, maxlen=50)

    return pad_data

# 標籤預測
def label_prediction(texts, model_name):
    # 加載 label_encoder
    with open(r'./encoder_tokenizer/label_encoder.pkl', 'rb') as file:
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
