import tkinter as tk
from tkinter.constants import *

window = tk.Tk()
window.title('GUI') # 標題
window.geometry('380x400') # 視窗大小
window.resizable(False, False) # 是否能夠更改視窗 x, y 大小
# window.iconbitmap('icon.ico')


# button
btn_1 = tk.Button(text='button 1')
btn_1.pack(side='bottom', pady=5)

# checkbox with event
def checkbutton_event():
    print("Checkbtn checked!")

def checkbutton_event(button):
    print(f"Checkbtn: {button['text']} checked: {window.getvar(button['variable'])}") # 必須得從TK母物件拿


checkbtn_1 = tk.Checkbutton(text="這是啟用的勾選框",state="active", command=checkbutton_event)
checkbtn_1.pack(side='bottom')
checkbtn_2 = tk.Checkbutton(text="這是禁用的勾選框",state="disabled")
checkbtn_2.pack(side='bottom')

is_checkbtn_3_checked = tk.IntVar()
checkbtn_3 = tk.Checkbutton(text="這是預設勾選的框",state="active", variable=is_checkbtn_3_checked, command=lambda:checkbutton_event(checkbtn_3))
checkbtn_3.pack(side='bottom')
checkbtn_3.select()


window.mainloop()