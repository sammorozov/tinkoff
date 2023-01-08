import tkinter as tk
import re


# функция, определяющее расттояние Левенштейна для двух строк


def levenstein(str_1, str_2):
    n, m = len(str_1), len(str_2)
    if n > m:
        str_1, str_2 = str_2, str_1
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if str_1[j - 1] != str_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


# функция убирающая пропуски в коде

def spaces(string):
    string = str(string)

    text = ''

    text += string.replace('\n', '').replace(' ', '').replace('    ', '')
    text = text.lower()

    return text


# функция убирающая комментарии в коде

def comments(string):
    string = str(string)

    if string[0] == '#':
        return ''

    elif string.find('#') != -1 and (string.find('"""') == -1 and string.find("'''") == -1):
        return string[:string.find('#')]
    else:
        return string


# функция убирающая многострочные комментарии в коде

def many_string_comm(text):
    text = str(text)

    a = text.find('"""')
    old_text = text[:a]
    new_text = text[a + 3:]

    res_text = old_text + new_text[new_text.find('"""') + 3:]

    return res_text


def many_string_comm2(text):
    text = str(text)
    a = text.find("'''")
    old_text = text[:a]
    new_text = text[a + 3:]
    res_text = old_text + new_text[new_text.find("'''") + 3:]
    text = res_text

    return text


# функция убирающая комментарии в коде комбинированная

def clear_com(text):
    new_text = text
    f = text.count('"""')
    s = text.count("'''")
    for i in range(f // 2):
        new_text = many_string_comm(new_text)
    new_text2 = new_text
    for i in range(s // 2):
        new_text2 = many_string_comm2(new_text2)

    return new_text2


# функция переводящая код в текст


def transform_into_string(file):
    text = ''
    with open(file, 'r', encoding='utf8') as f:
        for line in f:
            text += comments(line)

    return text


# функция убирающая частые слова + использование регулярок


def replaces(text):
    replace = ['import', 'from', 'def', 'class', 'return', 'while']
    short = ['i', 'f', 'd', 'c', 'r', 'w']
    for i in range(len(replace)):
        text = text.replace(replace[i], short[i])

    R2 = re.findall(r'__\w{2}__', text)
    R3 = re.findall(r'__\w{3}__', text)
    R4 = re.findall(r'__\w{4}__', text)
    R5 = re.findall(r'__\w{5}__', text)

    for i in range(len(R2)):
        text = text.replace(R2[i], f'{i}')

    for i in range(len(R3)):
        text = text.replace(R3[i], f'{i}')

    for i in range(len(R4)):
        text = text.replace(R4[i], f'{i}')

    for i in range(len(R5)):
        text = text.replace(R5[i], f'{i}')

    return text


# функция обрабатывающая два файла


def compare(input1):
    input1 = str(input1)
    scores = []
    file1 = input1.split()[0]
    file2 = input1.split()[1]
    transformfile1 = replaces(clear_com(spaces(transform_into_string(file1))))
    transformfile2 = replaces(clear_com(spaces(transform_into_string(file2))))

    score = 1 - levenstein(transformfile1, transformfile2) / max(len(transformfile1), len(transformfile2))

    scores += [str(round(score, 5))]  # получение score

    return scores


# обратная связь оконного интерфейса
# на вход два файла input.txt и scores.txt
def get_text():
    test = input1.get()
    test = str(test)
    scores = []

    finput = test.split()[0]
    fotput = test.split()[1]

    with open(finput, 'r', encoding='utf8') as ff:
        for line in ff:
            scores += compare(line)

    print(scores)
    root2 = tk.Tk()
    root2.title('Сравнение на плагиат кодов Python')
    root2.geometry("400x400")
    tk.Label(root, text='результаты').grid(row=1, column=0)
    k = 0
    for i in range(len(scores)):
        tk.Label(root2, text=f'{i + 1} пара ' + ' Результат:  ' + str(scores[i])).grid(row=2 + i, column=0)
        k = i
    tk.Label(root2, text='результаты сохранены в' + str(fotput)).grid(row=3 + k, column=0)
    output = fotput
    with open(output, 'w', encoding='utf8') as outf:
        for score in scores:
            outf.write(score)
            outf.write('\n')

    root2.mainloop()
    return 0


# Реализация окнного интерфейса

root = tk.Tk()
root.title('Сравнение на плагиат кодов Python')
root.geometry("400x200")

tk.Label(root, text='input.txt').grid(row=1, column=0)
tk.Label(root, text='Скопируйте и вставьте входной файл input.txt').grid(row=0, column=1)

input1 = tk.Entry()
input1.grid(row=1, column=1)
tk.Button(root, text='Check', command=get_text).grid(row=2, column=0)

root.mainloop()
