import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QFileDialog, QMessageBox, QLabel, QInputDialog

from module import businesscard_ocr
from module import label_prediction
from module import ChatGPT_prediction

# 使用的自定義模型
model = 'ner_model.h5'

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_file_path = ""
        self.texts = []

        # 布局
        layout = QVBoxLayout(self)

        # 文件導入欄位
        self.file_path_edit = QLineEdit(self)
        self.file_path_button = QPushButton('選擇文件', self)
        self.file_path_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.file_path_edit)
        layout.addWidget(self.file_path_button)

        # 文本辨識按鈕
        self.my_ocr_button = QPushButton('使用自訂OCR辨識圖片', self)
        self.my_ocr_button.clicked.connect(self.my_ocr)
        layout.addWidget(self.my_ocr_button)

        # 文字框
        self.text_box = QTextEdit(self)
        layout.addWidget(self.text_box)

        # 名片辨識按鈕
        self.my_model_predict_button = QPushButton('自訂模型分類', self)
        self.my_model_predict_button.clicked.connect(self.my_model_predict)
        layout.addWidget(self.my_model_predict_button)

        self.ChatGPT_predict_button = QPushButton('ChatGPT分類(需要API key)', self)
        self.ChatGPT_predict_button.clicked.connect(self.ChatGPT_predict)
        layout.addWidget(self.ChatGPT_predict_button)

        # 設置窗口
        self.setLayout(layout)
        self.setWindowTitle('名片辨識')

    # 文本錯誤彈出窗口
    def path_error_dialog(self):
        # 創建一個消息框
        dialog = QMessageBox(self)

        # 設置消息框的一些屬性
        dialog.setWindowTitle("路徑錯誤")
        dialog.setText("請先選擇路徑")

        # 添加標準按鈕
        dialog.setStandardButtons(QMessageBox.Ok)

        # 顯示對話框
        dialog.exec()


    def input_apikey(self):
        api_key, ok_pressed = QInputDialog.getText(self, "輸入API key", "請輸入API key:")
        if ok_pressed:

            os.environ['My_API'] = api_key
            

    def text_error_dialog(self):
        dialog = QMessageBox(self)

        dialog.setWindowTitle("文本錯誤")
        dialog.setText("請先辨識文本")

        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.exec()


    # 打開文件選擇對話框
    def open_file_dialog(self):
        filepath, filetype = QFileDialog.getOpenFileName(self)
        if filepath:
            # 設定路徑
            self.selected_file_path = filepath
            # 設定路徑文字框
            self.file_path_edit.setText(filepath)
                    
    def my_ocr(self):
        self.text_box.setText("") 
        if len(self.selected_file_path) != 0:
            text = businesscard_ocr(self.selected_file_path)
            self.text_box.append(text + "\n")
            self.texts = text
        else:
            self.path_error_dialog()

    def my_model_predict(self):
        if self.texts != []:
            card_info = label_prediction(self.texts, model)
            self.text_box.append("名片實體分類")
            if 'PERSON' in card_info and card_info['PERSON']:
                self.text_box.append(f"姓名: {str(card_info['PERSON'][0])}")
            if 'ORG' in card_info and card_info['ORG']:
                self.text_box.append(f"公司: {str(card_info['ORG'][0])}")
            if 'POSITION' in card_info and card_info['POSITION']:
                self.text_box.append(f"職稱: {str(card_info['POSITION'][0])}")
            if 'PHONE' in card_info and card_info['PHONE']:
                self.text_box.append(f"電話: {str(card_info['PHONE'][0])}")
            if 'ADDRESS' in card_info and card_info['ADDRESS']:
                self.text_box.append(f"地址: {str(card_info['ADDRESS'][0])}")
            if 'Email' in card_info and card_info['Email']:
                self.text_box.append(f"信箱: {str(card_info['Email'][0])}")
            if 'Link' in card_info and card_info['Link']:
                self.text_box.append(f"網址: {str(card_info['Link'][0])}\n")
        else:
            self.text_error_dialog()

    def ChatGPT_predict(self):
        if 'My_API' not in os.environ:  
            # 如果 My_API 不存在，則執行 input_apikey 函數以設置 API 金鑰
            self.input_apikey()
        if len(self.selected_file_path) != 0:
            try:
                card_info = ChatGPT_prediction(self.selected_file_path)
            except KeyError:
                # 如果發生 KeyError，將錯誤顯示
                self.text_box.append(f"API錯誤，您輸入的API為{os.environ.get('My_API', '未設置')} \n")
                # API錯誤，進行重置
                os.environ.pop('My_API', None)
            self.text_box.append("ChatGPT名片實體分類\n" + card_info + "\n")
        else:
            self.text_error_dialog()

# 創建應用程序和主窗口
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()

# 運行應用程序
sys.exit(app.exec())