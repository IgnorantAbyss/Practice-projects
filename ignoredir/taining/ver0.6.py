import pytesseract
import cv2
import drawboxes

# 設置Tesseract OCR的可執行文件路徑（根據你的安裝位置）
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

pic = "card1.png"

# 開啟要進行OCR的圖像文件
image = cv2.imread(pic)

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
        # elif abs(y - current_line_y) < 10:
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
            drawboxes.drawboxes(image, current_line_x - 3, current_line_y, square_width + 3, square_height)
            # print(f"合併文本: {current_line}")
            print(f"{current_line}")
            current_line = text
            current_line_y = y
            current_line_x = x
            square_width = width
            square_height = height
            right_top_x = x + width

# 最後一行文本
if current_line:
    # print(f"合併文本: {current_line}")
    print(f"{current_line}")
    drawboxes.drawboxes(image, current_line_x - 3, current_line_y, square_width + 3, square_height)


# 顯示圖像
cv2.imshow('Image with Text Boxes', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
