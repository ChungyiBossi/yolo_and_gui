import tkinter as tk
import numpy as np
import mediapipe as mp
from tkinter import Variable, filedialog
from PIL import Image, ImageTk
from mediapipe_object_detection import MPObjectDetectorWrapper

object_detector = MPObjectDetectorWrapper()
# canvas create
def create_canvas_with_scroll(parent_object):
    # 將 Canvas 掛在 Frame 之下
    canvas = tk.Canvas(parent_object, width=800, height=600, bg='#fff')
    # 新增 Scroll bars
    scrollX = tk.Scrollbar(parent_object, orient='horizontal')
    scrollX.pack(side='bottom', fill='x')
    scrollX.config(command=canvas.xview)

    scrollY = tk.Scrollbar(parent_object, orient='vertical')
    scrollY.pack(side='right', fill='y')
    scrollY.config(command=canvas.yview)

    canvas.config(xscrollcommand=scrollX.set, yscrollcommand=scrollY.set)
    canvas.pack(side='top')
    return canvas


# image process
def show_image(img, canvas):
    w, h = img.size                      # 取得圖片長寬
    tk_img = ImageTk.PhotoImage(img)     # 轉換成 tk 圖片物件
    canvas.delete('all')                 # 清空 Canvas 原本內容
    canvas.config(scrollregion=(0,0,w,h))   # 改變捲動區域
    canvas.create_image(0, 0, anchor='nw', image=tk_img)   # 建立圖片
    canvas.tk_img = tk_img               # 修改屬性更新畫面

def openfile_and_process(raw_canvas, cooked_canvas):
    img_path = filedialog.askopenfilename(filetypes=[('png', '*.png'),('jpg', '*.jpg'),('gif', '*.gif')])  # 指定開啟檔案格式
    img = Image.open(img_path)           # 依照圖片路徑取得圖片檔
    show_image(img, raw_canvas)
    process_and_show(img, cooked_canvas)

def process_and_show(raw_pillow_img, canvas):
    numpy_img = np.array(raw_pillow_img)
    detection_result = object_detector.object_detect(numpy_img)
    annotated_image = object_detector.visualize(numpy_img, detection_result)
    show_image(Image.fromarray(annotated_image), canvas)


if __name__ == '__main__':

    root = tk.Tk()
    root.title('Process Image')
    root.geometry('1600x900')

    button = tk.Button(root, text='Open Image and Process', command=lambda:openfile_and_process(raw_canvas, cooked_canvas))
    button.pack()

    # 創造兩個子視窗 raw/cooked image_frame
    raw_image_frame = tk.Frame(root, width=800, height=800)
    raw_image_frame.pack(side='left')
    cooked_image_frame = tk.Frame(root, width=800, height=800)
    cooked_image_frame.pack(side='right')

    # 掛上畫布
    raw_canvas = create_canvas_with_scroll(raw_image_frame)
    cooked_canvas = create_canvas_with_scroll(cooked_image_frame)

    root.mainloop()