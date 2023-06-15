import os
import tkinter
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from tkinter import messagebox

from database import database


class GUI:
    def __init__(self):

        self.main_window = tk.Tk()
        self.main_window.title("MAGAZYN")

        self.top_frame = tk.Frame(self.main_window)
        self.top_frame.pack(side="top")

        self.buttomRaport = tk.Button(self.top_frame, text='Stwórz raport', command=self.createRaport)
        self.buttomRaport.pack(side='left')

        self.separator_lineFirst = tk.Frame(self.top_frame, width=2, bd=1, relief=tk.SUNKEN)
        self.separator_lineFirst.pack(side='left', padx=5, pady=5, fill='y')

        self.text = tk.Text(self.top_frame,insertbackground='blue')
        self.text.pack(side='left',pady=10)
        self.text.config(width=10, height=1)
        self.buttomSearch = tk.Button(self.top_frame,text='Szukaj',command=self.call_method)
        self.buttomSearch.pack(side='left')

        self.separator_lineFirst = tk.Frame(self.top_frame, width=2, bd=1, relief=tk.SUNKEN)
        self.separator_lineFirst.pack(side='left', padx=5, pady=5, fill='y')

        self.bottom_label = tk.Label(self.top_frame, text="OrderBy: ")
        self.bottom_label.pack(side='left')


        self.attribute_var = tk.StringVar()
        self.attribute_checkbuttons = []
        attributes = ["ID", "Nazwa", "Opis", "Ocena", "Ilość", "Miara"]
        for attribute in attributes:
            checkbutton = tk.Checkbutton(self.top_frame, text=attribute, variable=self.attribute_var, onvalue=attribute,
                                         offvalue="")
            checkbutton.pack(anchor="w",side='left')
            self.attribute_checkbuttons.append(checkbutton)

        self.separator_line = tk.Frame(self.top_frame, width=2, bd=1, relief=tk.SUNKEN)
        self.separator_line.pack(side='left', padx=5, pady=5, fill='y')
        self.magazine_var = tk.BooleanVar()
        self.magazine_button = tk.Checkbutton(self.top_frame, text="Must be in magazine", variable=self.magazine_var)
        self.magazine_button.pack(anchor="w",fill="both")

        self.separator1 = tk.Frame(self.main_window, height=5, bd=1, relief=tk.SUNKEN)
        self.separator1.pack(fill="x")

        self.middle_frame = tk.Frame(self.main_window)
        self.middle_frame.pack(expand=True, fill="both")
        self.search()

        #self.listbox = tk.Listbox(self.middle_frame)
        #self.listbox.pack(expand=True, fill="both")

        self.separator2 = tk.Frame(self.main_window, height=2, bd=1, relief=tk.SUNKEN)
        self.separator2.pack(fill="x")

        self.bottom_frame = tk.Frame(self.main_window)
        self.bottom_frame.pack(side="bottom")

        column_names = ["ID", "Nazwa", "Opis", "Ocena", "Ilość", "Miara"]

        for i, name in enumerate(column_names):
            label = tk.Label(self.bottom_frame, text=name)
            label.grid(row=0, column=i, padx=5, pady=5)

        record_values = ["1", "Jakis Product", "Jakis Opis", "JakasOcena", "JakasIlosc", "JakasMiara"]

        self.entry_fields = []
        for i, value in enumerate(record_values):
            entry = tk.Entry(self.bottom_frame)
            entry.insert(tk.END, value)
            entry.grid(row=1, column=i, padx=5, pady=5)
            self.entry_fields.append(entry)

        button_frame = tk.Frame(self.bottom_frame)
        button_frame.grid(row=1, column=len(column_names), padx=5, pady=5, rowspan=2)

        button_dodaj = tk.Button(button_frame, text="Dodaj",command=self.add)
        button_dodaj.pack(fill="x", side='left')

        button_usun = tk.Button(button_frame, text="Usuń",command=self.delete)
        button_usun.pack(fill="x", side='left')

        button_zaktualizuj = tk.Button(button_frame, text="Zaktualizuj",command=self.update)
        button_zaktualizuj.pack(fill="x",side='left')

        self.main_window.mainloop()

    def submit_values(self, entry_fields):
        values = [entry.get() for entry in entry_fields]
        print(values)

    def call_method(self,event=None):
        text_input = self.text.get("1.0", "end-1c")  # Retrieve text from the text field
        print(text_input)  # Call the method with the text input
        #self.text.delete("1.0", "end")
        self.search()


    def update_list(self):
        # Clear the existing items in the listbox
        self.listbox.delete(0, tk.END)

        # Add new items to the listbox
        items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
        for item in items:
            self.listbox.insert(tk.END, item)


    def add(self):
            data = []
            for entry in self.entry_fields:
                value = entry.get()
                if(value==""):
                    value=None
                data.append(value)

            #Błędy
            try:
                if data[0] is not None:
                    data[0] = int(data[0])
            except ValueError:
                tkinter.messagebox.showinfo('Error', 'ID must be an integer')
                return
            try:
                if data[4] is not None:
                    data[4] = float(data[4])
            except ValueError:
                tkinter.messagebox.showinfo('Error', 'Ilość must be a float')
                return
            try:
                if data[3] is not None:
                  data[3] = (data[3])
            except ValueError:
                tkinter.messagebox.showinfo('Error', 'Ocena must be a float')
                return

            resoult = database.add(data[0],data[1],data[2],data[3],data[5],data[4])
            if resoult == 'Not':
                tkinter.messagebox.showinfo('Error', 'Ilość nie może być poniżej zera')
            if resoult == 'Not1':
                tkinter.messagebox.showinfo('Error', 'Przy nowych produktach wymagana jest nazwa')
            self.search()


    def delete(self):
        data = []
        for entry in self.entry_fields:
            value = entry.get()
            if (value == ""):
                value = None
            data.append(value)
        resoult = database.delete(data[0])
        if resoult == 'Not':
            tkinter.messagebox.showinfo('Error', 'Id cannot by null')
        self.search()


    def update(self):
        data = []
        for entry in self.entry_fields:
            value = entry.get()
            if (value == ""):
                value = None
            data.append(value)
        resoult = database.update(int(data[0]),data[1],data[2],float(data[3]),data[5],int(data[4]))
        if resoult == 'Not1':
            tkinter.messagebox.showinfo('Error', 'Ilość nie może być poniżej zera')
        if resoult == 'Not2':
            tkinter.messagebox.showinfo('Error', 'Id cannot by null')
        self.search()

    def search(self):
        text_input = self.text.get("1.0", "end-1c")
        selected_option = self.attribute_var.get()
        inMagazine = self.magazine_var.get()
        resoult = database.search(keyword=text_input, sort_by=selected_option, include_zero=inMagazine)

        for widget in self.middle_frame.winfo_children():
            if isinstance(widget, ttk.Scrollbar):
                widget.destroy()

        for widget in self.middle_frame.winfo_children():
            if isinstance(widget, ttk.Treeview):
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

        self.tree.bind("<Double-1>", self.on_tree_double_click)

    def on_tree_double_click(self, event):
        selected_item = self.tree.selection()[0]

        values = self.tree.item(selected_item, "values")

        for i, value in enumerate(values):
            self.entry_fields[i].delete(0, tk.END)
            self.entry_fields[i].insert(tk.END, value)

    def createRaport(self):
        data_list = database.search()
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H-%M-%S")
        report_name = f"Raport_{current_date}_{current_time}.txt"
        report_folder = "raporty"

        if not os.path.exists(report_folder):
            os.makedirs(report_folder)

        file_path = os.path.join(report_folder, report_name)

        with open(file_path, "w") as file:
            for item in data_list:
                file.write(str(item) + "\n")
        tkinter.messagebox.showinfo('Raport', 'Raport zapisany w forderze raoporty')

# metoda createDatabase tworząca bazę danych
# metoda addValuesToDatabase dodająca podstawowe wartości
# metoda serch zwracająca listę danych wraz z mozliwością szukania po nazwa lub id oraz order by
# metoda init króra sprawdza czy bazadanych istnieje i może wyłować create
# metoda modyfikujProdukt zmienia informacje o produkcie
# metoda usunProdukt usuwa produkt