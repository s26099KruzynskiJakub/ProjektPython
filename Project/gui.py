import tkinter
import tkinter as tk
from tkinter import ttk

from database import database


class GUI:
    def __init__(self):

        self.main_window = tk.Tk()
        self.main_window.title("MAGAZYN")

        self.top_frame = tk.Frame(self.main_window)
        self.top_frame.pack(side="top")

        # Button to select value (Name or ID)
        self.text = tk.Text(self.top_frame,insertbackground='blue')
        self.text.pack(side='left',pady=10)
        self.text.config(width=10, height=1)

        # Separator Line
        self.separator_lineFirst = tk.Frame(self.top_frame, width=2, bd=1, relief=tk.SUNKEN)
        self.separator_lineFirst.pack(side='left', padx=5, pady=5, fill='y')

        self.bottom_label = tk.Label(self.top_frame, text="OrderBy: ")
        self.bottom_label.pack(side='left')

        # Checkbuttons for advanced search attributes
        self.attribute_var = tk.StringVar()
        self.attribute_checkbuttons = []
        attributes = ["ID", "Nazwa", "Opis", "Ocena", "Ilość", "Miara"]
        for attribute in attributes:
            checkbutton = tk.Checkbutton(self.top_frame, text=attribute, variable=self.attribute_var, onvalue=attribute,
                                         offvalue="")
            checkbutton.pack(anchor="w",side='left')
            self.attribute_checkbuttons.append(checkbutton)

         # Separator Line
        self.separator_line = tk.Frame(self.top_frame, width=2, bd=1, relief=tk.SUNKEN)
        self.separator_line.pack(side='left', padx=5, pady=5, fill='y')
        self.magazine_var = tk.BooleanVar()
        self.magazine_button = tk.Checkbutton(self.top_frame, text="Must be in magazine", variable=self.magazine_var)
        self.magazine_button.pack(anchor="w",fill="both")  # Align to the left

        # Separator Line
        self.separator1 = tk.Frame(self.main_window, height=5, bd=1, relief=tk.SUNKEN)
        self.separator1.pack(fill="x")

        # Middle Frame
        self.middle_frame = tk.Frame(self.main_window)
        self.middle_frame.pack(expand=True, fill="both")
        self.search()

        #self.listbox = tk.Listbox(self.middle_frame)
        #self.listbox.pack(expand=True, fill="both")

        # Separator Line
        self.separator2 = tk.Frame(self.main_window, height=2, bd=1, relief=tk.SUNKEN)
        self.separator2.pack(fill="x")

        # Bottom Frame
        self.bottom_frame = tk.Frame(self.main_window)
        self.bottom_frame.pack(side="bottom")
        self.bottom_label = tk.Label(self.bottom_frame, text="Bottom Frame")
        self.bottom_label.pack()

        # Adjust weight to make the middle frame bigger
        self.main_window.grid_rowconfigure(2, weight=1)



        self.text.bind("<Return>", self.call_method)
        tk.mainloop()

    def call_method(self,event=None):
        text_input = self.text.get("1.0", "end-1c")  # Retrieve text from the text field
        print(text_input)  # Call the method with the text input
        self.text.delete("1.0", "end")
        self.search()

    def update_list(self):
        # Clear the existing items in the listbox
        self.listbox.delete(0, tk.END)

        # Add new items to the listbox
        items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
        for item in items:
            self.listbox.insert(tk.END, item)


    def add(self):
        #pobieranie wartości
        resoult = database.add(1,'Nazwa','Opis','Cena','Miara_ilosci','Ilosc')
        if resoult == 'Not':
            tkinter.messagebox.showinfo('Error', 'Ilość nie może być poniżej zera')


    def delete(self):
        #pobieranie watoście id
        resoult = database.delete(1)
        if resoult == 'Not':
            tkinter.messagebox.showinfo('Error', 'Id cannot by null')


    def update(self):
        # pobieranie wartości
        resoult = database.update(1, 'Nazwa', 'Opis', 'Cena', 'Miara_ilosci', 'Ilosc')
        if resoult == 'Not1':
            tkinter.messagebox.showinfo('Error', 'Ilość nie może być poniżej zera')
        if resoult == 'Not2':
            tkinter.messagebox.showinfo('Error', 'Id cannot by null')

    def search(self):
        text_input = self.text.get("1.0", "end-1c")
        selected_option = self.attribute_var.get()
        inMagazine = self.magazine_var.get()
        resoult = database.search(keyword=text_input, sort_by=selected_option, include_zero=inMagazine)

        for widget in self.middle_frame.winfo_children():
            widget.destroy()

        self.tree = ttk.Treeview(self.middle_frame, columns=("Id", "Nazwa", "Opis", "Cena", "Miara_Ilosci", "Ilosc"))

        self.tree.heading("Id", text="ID")
        self.tree.heading("Nazwa", text="Nazwa")
        self.tree.heading("Opis", text="Opis")
        self.tree.heading("Cena", text="Cena")
        self.tree.heading("Miara_Ilosci", text="Miara Ilości")
        self.tree.heading("Ilosc", text="Ilość")

        for item in resoult:
            self.tree.insert("", tk.END, values=item)

        scrollbar = ttk.Scrollbar(self.middle_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.pack(fill=tk.BOTH, expand=True)




# Create an instance of the GUI class
gui = GUI()

# metoda createDatabase tworząca bazę danych
# metoda addValuesToDatabase dodająca podstawowe wartości
# metoda serch zwracająca listę danych wraz z mozliwością szukania po nazwa lub id oraz order by
# metoda init króra sprawdza czy bazadanych istnieje i może wyłować create
# metoda modyfikujProdukt zmienia informacje o produkcie
# metoda usunProdukt usuwa produkt