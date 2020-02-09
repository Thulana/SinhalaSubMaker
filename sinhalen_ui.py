from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter.ttk import Progressbar
import io
from translate import Translator
import threading
import random
from time import sleep
import sys

LANGUAGE = "si"
fields = 'Sub file', 'Output name',"From Language"

root = Tk()
progress = Progressbar(root, orient=HORIZONTAL, length=500, mode='determinate')
tkvar = StringVar(root)
choices = {'si', 'en', 'ta'}
# on change dropdown value
def change_dropdown(*args):
    global LANGUAGE
    LANGUAGE = tkvar.get()
    print(LANGUAGE)

def makeform(root, fields):
    entries = []

    tkvar.set('si')  # set the default option
    row = Frame(root)
    lab = Label(row, width=15, text="To Language", anchor='w')
    ent = OptionMenu(row, tkvar, *choices)
    row.pack(side=TOP, fill=X, padx=10, pady=8)
    lab.pack(side=LEFT)
    ent.pack(side=RIGHT, expand=YES, fill=X)
    tkvar.trace('w', change_dropdown)

    for field in fields:
        row = Frame(root)
        lab = Label(row, width=15, text=field, anchor='w')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=10, pady=8)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries.append((field, ent))
    return entries


def translate_text(translator,text, target):
    """Translates text into the target language.
    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    ###translate_client = translate.Client()

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    ###result = translate_client.translate(text, target_language=target)

    ###return result['translatedText']

    result = translator.translate(text)
    return result


def convert(root, entries):
    from_lang = 'autodetect'
    file_name = ''
    output = 'sub'
    lang = LANGUAGE
    for entry in entries:
        if entry[0] == fields[0]:
            file_name = entry[1].get()
        elif entry[0] == fields[1]:
            output = entry[1].get()
        elif entry[0] == fields[2]:
            if entry[1].get() != "":
                from_lang = entry[1].get()

    translator = Translator(to_lang=LANGUAGE, from_lang=from_lang)
    print(from_lang,lang)
    try:

        with io.open(output + "_" + lang + ".srt", 'wb') as hi:
                index = 0
                with io.open(file_name, 'r') as file:
                    contents = file.readlines()
                    contents[0] = "1\n"
                    for i in range(len(contents)):
                        if contents[i][0].isdigit():
                            hi.write(contents[i].encode())
                        else:
                            while True:
                                # try:
                                    hi.write((translate_text(translator,contents[i],lang)+ "\n").encode())
                                    break
                                # except:
                                    print('connection error, retrying')
                                    sleep(random.randint(1, 3))
                            index += 1

                        precentage = int((i/len(contents))*100)
                        progress['value'] = precentage
                        root.update_idletasks()

        messagebox.showinfo("Done", " subtitle file created successfully.")
        progress['value'] = 0
        root.update_idletasks()
    except Exception as e:
        messagebox.showerror("Error", "Error occured. Please check inputs and try again.")
        print(e)
        progress['value'] = 0
        root.update_idletasks()

def async_convert(root, entries):
    t = threading.Thread(target=convert, args=(root,entries))
    t.start()


def open_file(root, entries):
    print('file open')
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    output_name = ".".join(filename.split('.')[:-1])
    for entry in entries:
        if entry[0] == fields[0]:
            entry[1].delete(0, END)
            entry[1].insert(0, filename)
        elif entry[0] == fields[1]:
            entry[1].delete(0, END)
            entry[1].insert(0, output_name)


if __name__ == '__main__':
    root.title("Sinhalen Subtitle Maker")
    # root.geometry("500x240")
    w = root.winfo_reqwidth()
    h = root.winfo_reqheight()
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('+%d+%d' % (x, y))
    root.resizable(0, 0)

    # Dictionary with options
    choices = {'si', 'en', 'ta'}
    tkvar.set('si')  # set the default option
    ents = makeform(root, fields)
    btn_row = Frame(root)
    btn_row.pack(side=TOP, fill=X, padx=10, pady=8)
    b1 = Button(btn_row, text='Open File',
                command=lambda: open_file(root, ents))
    b1.pack(side=LEFT, padx=5, pady=5)
    b3 = Button(btn_row, text='Convert', command=lambda: async_convert(root, ents))
    b3.pack(side=LEFT, padx=10, pady=5)
    b2 = Button(btn_row, text='Quit', command=root.quit)
    b2.pack(side=RIGHT, padx=5, pady=5)
    progress.pack(side=BOTTOM, pady=5)

    root.mainloop()
