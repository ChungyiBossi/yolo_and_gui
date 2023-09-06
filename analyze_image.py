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
    canvas = tk.Canvas(parent_object, width=700, height=400, bg='#fff')
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

def openfile_and_process(raw_canvas, cooked_canvas, textbox):
    # openfile
    img_path = filedialog.askopenfilename(filetypes=[('png', '*.png'),('jpg', '*.jpg'),('gif', '*.gif')])  # 指定開啟檔案格式
    img = Image.open(img_path)           # 依照圖片路徑取得圖片檔
    show_image(img, raw_canvas)
    # process
    numpy_img = np.array(img)
    detection_result = object_detector.object_detect(numpy_img)
    annotated_image = object_detector.visualize(numpy_img, detection_result)
    show_image(Image.fromarray(annotated_image), cooked_canvas)
    # print result
    # 整理辨識結果到text box
    results = list()
    for result in detection_result.detections:
        category = result.categories[0]
        category_name = category.category_name
        probability = round(category.score, 2)
        result_text = category_name + ' (' + str(probability) + ')'
        results.append(result_text)
    result_for_text_box = "\n".join(results)
    textbox.delete(1.0,'end')
    textbox.insert(tk.END, result_for_text_box)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Process Image')
    root.geometry('1600x900')

    # 創造兩個子視窗 raw/cooked image_frame, 用left frame 包起來
    left_frame = tk.Frame(root)
    left_frame.pack(side='left')
    raw_image_frame = tk.Frame(left_frame, width=800, height=450)
    raw_image_frame.pack(padx=10, pady=10)
    cooked_image_frame = tk.Frame(left_frame, width=800, height=450)
    cooked_image_frame.pack(padx=10, pady=10)
    # 掛上畫布
    raw_canvas = create_canvas_with_scroll(raw_image_frame)
    cooked_canvas = create_canvas_with_scroll(cooked_image_frame)
    
    right_frame = tk.Frame(root)
    right_frame.pack(side='right')
    # 創造一個顯示結果的文字框, 包在right frame 之下
    result_text = tk.Text(right_frame, width=800, font=('Arial',20,'bold'),)
    result_text.insert(tk.END, "這裡是空白的")
    result_text.pack(padx=10, pady=10, anchor='nw')
    # result_text.pack(padx=10, pady=10)
    # 上傳圖檔按鈕, 包在 right frame
    button = tk.Button(
        right_frame, 
        text='Open Image and Process', 
        font=('Arial',15,'bold'),
        command=lambda :openfile_and_process(raw_canvas, cooked_canvas, result_text)
    )
    button.pack(padx=10, pady=10, side='left')
    
    

    root.mainloop()