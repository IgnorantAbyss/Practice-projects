import cv2

def drawboxes(image,x,y,w,h):
    # image_y = image.shape[0] - (y + h)
                        # 左上      右下            顏色      粗細
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 顯示圖像
    # cv2.imshow('Image with Text Boxes', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()