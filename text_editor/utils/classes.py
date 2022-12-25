import tkinter as tk
from tkinter import Tk, Frame, Menu, Text, Scrollbar ,filedialog, ttk, messagebox
from tkinter.messagebox import showinfo


class TextEditor(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.master.title("Simply text editor")
        main_menu = Menu(self.master)
        self.master.config(menu=main_menu)
        file_menu = Menu(main_menu, tearoff=0)
        file_menu.add_command(label="New file", command=self.new_file)
        file_menu.add_command(label="Open file", command=self.select_and_open_file)
        file_menu.add_command(label="Close file", command=self.close_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save as", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit)
        main_menu.add_cascade(label="File", menu=file_menu)
    

    def exit(self):
        self.quit()


class TextNotes(TextEditor):
    def __init__(self):
        super().__init__()
        
        self.txt()

    def txt(self):
        txtFrame = Frame(self.master)
        txtFrame.pack(side = "bottom", fill="both", expand=True)
        global txt_notes
        txt_notes = Text(master=txtFrame, wrap="word")
        scrollbar = Scrollbar(master=txtFrame, command=txt_notes.yview)
        txt_notes['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side="right", fill="y")
        txt_notes.pack(side = "bottom", fill="both", expand=True)


    def info(self):
        title="Save"
        massage="Save the file?"
        return messagebox.askyesno(title, massage)



    def select_and_open_file(self):
        """ need text. docstring"""
        global filetypes
        filetypes = (
            ('Text files', '*.txt'),
            ('All files', '*.*')
        )
        global filepath_open
        filepath_open = filedialog.askopenfilename(filetypes=filetypes)
        if filepath_open:
            with open(filepath_open, "r") as outFile:
                text = outFile.read()
                txt_notes.delete("1.0", "end-1c")
                txt_notes.insert("1.0", text)
                outFile.close()
        else:
            return

    def new_file(self):
        """ need text. docstring. """
        txt_notes.delete("0.0", "end-1c")


    def local(self, filepath_open):
        """ need text. docstring"""
        filepath_open = None
        return filepath_open

    def close_file(self):
        """ need text. docstring"""
        global filepath_open
        if filepath_open:
            title="Save"
            massage="Save the file?"
            flag = self.info()
            if flag:
                self.save_file()
                txt_notes.delete("0.0", "end-1c")
                filepath_open = self.local(filepath_open)
        else:
            return
       


    def save_as_file(self):
        """ need text. docstring"""
        filepath = filedialog.asksaveasfilename(filetypes=filetypes)
        if filepath != "":
            text = txt_notes.get("1.0", "end-1c")
            with open(filepath, "w") as inFile:
                inFile.write(text)
                inFile.close()
        else:
            return
                
    
    def save_file(self):
        """ need text. docstring"""
        text = txt_notes.get("0.0", "end-1c")
        with open(filepath_open, "w") as outInfile:
            outInfile.write(text)
            outInfile.close()