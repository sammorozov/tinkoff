import tkinter as tk
from script import *
import re

"""
Реализован оконный интерфейс.

пример входного файла input.txt
Скопировать с 11 по 16 строчку включительно, работает долго. ага

files/add_constant.py plagiat1/add_constant.py
files/apply_lambda.py plagiat1/apply_lambda.py
files/test_auto.py plagiat1/test_auto.py
files/forward.py plagiat1/forward.py
files/fourier.py plagiat1/fourier.py
files/generator.py plagiat1/generator.py



"""




def get_text():
    test = input1.get()
    test = str(test)

    data = test.split('\n')
    scores = []
    print(data)
    for d in data:
        scores += compare(d)

    print(scores)
    root2 = tk.Tk()
    root2.title('Сравнение на плагиат кодов Python')
    root2.geometry("400x400")
    tk.Label(root, text='результаты').grid(row=1, column=0)
    for i in range(len(scores)):
        tk.Label(root2, text=f'{i+1} пара ' + ' Результат:  ' + str(scores[i])).grid(row=2+i, column=0)
    root2.mainloop()
    return 0


root = tk.Tk()
root.title('Сравнение на плагиат кодов Python')
root.geometry("400x200")

tk.Label(root, text='input.txt').grid(row=1, column=0)
tk.Label(root, text='Скопируйте и вставьте входной файл input.txt').grid(row=0, column=1)

input1 = tk.Entry()
input1.grid(row=1, column=1)
tk.Button(root, text='Check', command=get_text).grid(row=2, column=0)


root.mainloop()

