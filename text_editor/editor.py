from tkinter import Frame, Menu, Text, Scrollbar, filedialog, messagebox, Tk


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
        file_menu.add_command(label="New file", command=self.new_file)
        file_menu.add_command(label="Open file",
                              command=self.select_and_open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save as", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_from_editor)
        main_menu.add_cascade(label="File", menu=file_menu)

        txtFrame = Frame(self.master)
        txtFrame.pack(side="bottom", fill="both", expand=True)
        global txt_notes
        txt_notes = Text(master=txtFrame, wrap="word")
        scrollbar = Scrollbar(master=txtFrame, command=txt_notes.yview)
        txt_notes['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side="right", fill="y")
        txt_notes.pack(side="bottom", fill="both", expand=True)

    global filetypes
    filetypes = (
        ('Text files', '*.txt'),
        ('All files', '*.*')
    )

    def check_gl_var(self) -> bool:
        """ Verification of the presence of a global variable. """
        if 'filepath_open' in globals():
            return True
        else:
            return False

    def exit_from_editor(self) -> None:
        """ Exiting the application. """
        self.quit()

    def info(self):
        """ For the function 'askyesno'. """
        title = "Save"
        massage = "Save the file?"
        return messagebox.askyesno(title, massage)

    def select_and_open_file(self) -> None:
        """ Selecting and opening a file. """
        global filepath_open
        filepath_open = filedialog.askopenfilename(filetypes=filetypes)
        if filepath_open:
            with open(filepath_open, "r") as outFile:
                text = outFile.read()
                txt_notes.delete("1.0", "end-1c")
                txt_notes.insert("1.0", text)
                outFile.close()

    def local(self, filepath_open) -> None:
        """ To reset the global variable. """
        filepath_open = None
        return filepath_open

    def new_file(self) -> None:
        """ Creating a new text field. """
        gl_check = self.check_gl_var()
        if gl_check:
            global filepath_open
            if filepath_open:
                flag = self.info()
                if flag:
                    self.save_file()
                    txt_notes.delete("1.0", "end-1c")
                    filepath_open = self.local(filepath_open)
                else:
                    txt_notes.delete("1.0", "end-1c")
                    filepath_open = self.local(filepath_open)
        elif not gl_check:
            text = txt_notes.get("1.0", "end-1c")
            if text:
                flag = self.info()
                if flag:
                    self.save_as_file()
                txt_notes.delete("1.0", "end-1c")

    def save_as_file(self) -> None:
        """ The 'save as...' function. """
        text = txt_notes.get("1.0", "end-1c")
        global filepath_open
        if text:
            filepath_open = filedialog.asksaveasfilename(filetypes=filetypes)
            if filepath_open:
                with open(filepath_open, "w") as inFile:
                    inFile.write(text)
                    inFile.close()

    def save_file(self) -> None:
        """ The 'save' function."""
        gl_check = self.check_gl_var()
        if gl_check:
            if filepath_open:
                text = txt_notes.get("1.0", "end-1c")
                with open(filepath_open, "w") as outInfile:
                    outInfile.write(text)
                    outInfile.close()
        elif not gl_check:
            self.save_as_file()


def main():
    root = Tk()
    TextEditor(root).pack()
    root.mainloop()


if __name__ == "__main__":
    main()
