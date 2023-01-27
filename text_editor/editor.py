import webbrowser
from tkinter import (Frame, Menu, Text, Scrollbar,
                     filedialog, messagebox, Tk)


class TextEditor(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.up_menu()

    def up_menu(self) -> None:
        """ Basic widgets. """
        self.master.title("Simply text editor")
        main_menu = Menu(self)
        self.master.config(menu=main_menu)
        file_menu = Menu(main_menu, tearoff=0)
        file_menu_correction = Menu(main_menu, tearoff=0)
        mouse_menu = Menu(main_menu, tearoff=0)
        file_menu_data = Menu(main_menu, tearoff=0)
        file_menu.add_command(label="New file", command=self.new_file,
                              accelerator="Ctrl+N")
        file_menu.add_command(label="Open file",
                              command=self.select_and_open_file,
                              accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_file,
                              accelerator="Ctrl+S")
        file_menu.add_command(label="Save as", command=self.save_as_file,
                              accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_from_editor,
                              accelerator="Ctrl+Q")
        file_menu_correction.add_command(label="Cut", command=self.cut_text,
                                         accelerator="Ctrl+X")
        file_menu_correction.add_command(label="Copy", command=self.copy_text,
                                         accelerator="Ctrl+C")
        file_menu_correction.add_separator()
        file_menu_correction.add_command(label="Paste",
                                         command=self.paste_text,
                                         accelerator="Ctrl+V")
        file_menu_correction.add_command(label="Select text",
                                         command=self.select_text,
                                         accelerator="Ctrl+A")
        file_menu_data.add_command(label="Github", command=self.url)
        file_menu_data.add_command(label="Data", command=self.data)

        mouse_menu.add_command(label="Save", command=self.save_file)
        mouse_menu.add_command(label="Save as", command=self.save_as_file)
        mouse_menu.add_separator()
        mouse_menu.add_command(label="Select text", command=self.select_text)
        mouse_menu.add_command(label="Cut", command=self.cut_text)
        mouse_menu.add_command(label="Copy", command=self.copy_text)
        mouse_menu.add_command(label="Paste", command=self.paste_text)

        def mouse_popup(event):
            try:
                mouse_menu.tk_popup(event.x_root, event.y_root)
            finally:
                mouse_menu.grab_release()

        self.bind_all("<Button-3>", mouse_popup)

        main_menu.add_cascade(label="File", menu=file_menu)
        main_menu.add_cascade(label="Сorrection", menu=file_menu_correction)
        main_menu.add_cascade(label="Data", menu=file_menu_data)

        txtFrame = Frame(self.master)
        txtFrame.pack(side="bottom", fill="both", expand=True)
        self.txt_notes = Text(master=txtFrame, wrap="word")
        scrollbar = Scrollbar(master=txtFrame, command=self.txt_notes.yview)
        self.txt_notes['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side="right", fill="y")
        self.txt_notes.pack(side="bottom", fill="both", expand=True)

        def key_non_shift(event):
            keys_code = {
                (79, 32): self.select_and_open_file,
                (78, 57): self.new_file,
                (83, 39): self.save_file,
                (65, 38): self.select_text,
                (81, 24): self.exit_from_editor,
            }
            for key_coder, key_func in keys_code.items():
                if event.keycode in key_coder:
                    key_func()

        self.bind_all("<Control-KeyPress>", key_non_shift)

        def keypress_with_shift(event):
            if event.keycode == 83 or event.keycode == 115:
                self.save_as_file()

        self.bind_all("<Control-Shift-KeyPress>", keypress_with_shift)

        self.filetypes = (
            ('Text files', '.txt'),
            ('All files', '.*')
        )

        self.index_first = 0.0
        self.last_index = 0.0
        self.filepath_open = None

    def exit_from_editor(self) -> None:
        """ Exiting the application. """
        self.master.title("Simply text editor - closing")
        self.master.destroy()

    def info(self):
        """ For the function 'askyesno'. """
        title = "Save"
        massage = "Save the file?"
        return messagebox.askyesno(title, massage)

    def select_and_open_file(self) -> None:
        """ Selecting and opening a file. """
        self.filepath_open = (filedialog.askopenfilename
                              (filetypes=self.filetypes, defaultextension=''))
        self.master.title(f"Simply text editor - {self.filepath_open}")
        if self.filepath_open:
            with open(self.filepath_open, "r") as outFile:
                self.txt_notes.delete("1.0", "end-1c")
                self.txt_notes.insert("1.0", outFile.read())
                outFile.close()

    def local(self) -> None:
        """ To reset the variable. """
        return None

    def new_file(self) -> None:
        """ Creating a new text field. """
        if self.filepath_open:
            flag = self.info()
            if flag:
                self.save_file()
                self.txt_notes.delete("1.0", "end-1c")
                self.filepath_open = None
            else:
                self.txt_notes.delete("1.0", "end-1c")
                self.filepath_open = None
        else:
            flag = self.info()
            if flag:
                self.save_as_file()
            self.txt_notes.delete("1.0", "end-1c")
        self.master.title("Simply text editor - New")

    def save_as_file(self) -> None:
        """ The 'save as...' function. """
        self.filepath_open = (filedialog.asksaveasfilename
                              (filetypes=self.filetypes,
                               defaultextension='initialfile'))
        if self.filepath_open:
            self.master.title(f"Simply text editor - {self.filepath_open}")
            with open(self.filepath_open, "w") as inFile:
                inFile.write(self.txt_notes.get("1.0", "end-1c"))
                inFile.close()

    def save_file(self) -> None:
        """ The 'save' function. """
        if self.filepath_open:
            self.master.title(f"Simply text editor - {self.filepath_open}")
            with open(self.filepath_open, "w") as outInfile:
                outInfile.write(self.txt_notes.get("1.0", "end-1c"))
                outInfile.close()
        else:
            self.save_as_file()

    def func_for_copy_cut(self) -> bool:
        """ General function for copying and cutting. """
        self.clipboard_append('')
        self.clipboard_clear()
        self.clipboard_append(self.txt_notes.selection_get())
        self.update()
        self.index_first = self.txt_notes.index("sel.first")
        self.index_last = self.txt_notes.index("sel.last")
        self.txt_notes.selection_clear()

    def cut_text(self) -> None:
        """ Cut text. """
        self.func_for_copy_cut()
        self.txt_notes.delete(self.index_first, self.index_last)

    def copy_text(self) -> None:
        """ Copy text. """
        self.func_for_copy_cut()

    def paste_text(self):
        """ Paste text. """
        index_cursor = self.txt_notes.index('insert')
        self.txt_notes.insert(index_cursor, self.clipboard_get())

    def select_text(self) -> None:
        """ Select text. """
        self.txt_notes.tag_add("sel", "1.0", "end-1c")

    def data(self) -> None:
        """ Information. """
        msg = ('This is a simple text editor designed '
               'to work on texts that do not require any '
               'specific processing. It was created for '
               'educational purposes. Completely written in '
               'python3 using the tkinter library. '
               'Perhaps it will be finalized over time. '
               'The project can be used and refined by '
               'other people, both for educational and '
               'practical purposes.')
        messagebox.showinfo("Information", msg)

    def url(self) -> None:
        """ For git url. """
        webbrowser.open("https://github.com/romanpittchai/text-editor")


def main():
    root = Tk()
    TextEditor(root).pack()
    root.mainloop()


if __name__ == "__main__":
    main()
