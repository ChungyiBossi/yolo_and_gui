import tkinter as tk
from tkinter.constants import *
from PIL import Image, ImageTk

# create windows
windows = tk.Tk()
windows.title('Image Sampe')
windows.geometry('400x400')

# load image
img = Image.open('cat.jpg')

# resize image
print(f"Original image:{img.width}x{img.height}")
if img.height <= img.width:
    img =img.resize((300, int(img.height * (300/img.width))))
else:
    img =img.resize((int(img.width * (300/img.height)), 300))

print(f"Modify image:{img.width}x{img.height}")
tk_img = ImageTk.PhotoImage(img)
canvas = tk.Canvas(windows, width=400, height=400)
canvas.create_image(0, 0, anchor='nw', image=tk_img)   # 在 Canvas 中放入圖片
canvas.pack(anchor=CENTER)

windows.mainloop()