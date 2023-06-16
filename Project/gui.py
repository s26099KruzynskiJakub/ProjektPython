import os
import tkinter
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from tkinter import messagebox

from database import database


class GUI:
    """
     Ta klasa reprezentuje interfejs graficzny użytkownika do zarządzania magazynem.

     Atrybuty:
         main_window (tkinter.Tk): Główne okno interfejsu graficznego.
         top_frame (tkinter.Frame): Górna ramka zawierająca przyciski i funkcjonalność wyszukiwania.
         middle_frame (tkinter.Frame): Środkowa ramka zawierająca wyniki wyszukiwania.
         bottom_frame (tkinter.Frame): Dolna ramka zawierająca pola wprowadzania do dodawania/aktualizowania rekordów.
         entry_fields (list): Lista pól wprowadzania danych dla aktualizacji rekordów.
         attribute_checkbuttons (list): Lista checkbuttonów do wyboru po czym sortujemy rekordy.
         attribute_var (tkinter.StringVar): Zmienna przechowująca wybrany atrybut sortowania.
         magazine_var (tkinter.BooleanVar): Zmienna przechowująca wybór czy rekordy mają być w bazie danych czy nie(jeżeli ilość =0 rekord nie zostanie zwrócony).

     Metody:
         clearAllValues: Czyści wszystkie pola wprowadzania danych w interfejsie graficznym dotyczącym dodawania, usuwania czy akutalizowania wartośći.
         add: Dodaje nowy rekord do bazy danych na podstawie pól wprowadzania danych.
         throwError: Sprawdza poprawność wprowadzanych danych i wyświetla ewentualne komunikaty o błędach.
         delete: Usuwa rekord z bazy danych na podstawie pól wprowadzania danych.
         update: Aktualizuje rekord w bazie danych na podstawie pól wprowadzania danych.
         search: Wykonuje wyszukiwanie w bazie danych na podstawie wprowadzonego tekstu i wybranych atrybutów.
         on_tree_double_click: Obsługuje zdarzenie podwójnego kliknięcia na element wyniku wyszukiwania.
         createRaport: Tworzy plik raportu z aktualnymi rekordami bazy danych.

     """
    def __init__(self):

        self.main_window = tk.Tk()
        self.main_window.title("MAGAZYN")

        self.top_frame = tk.Frame(self.main_window)
        self.top_frame.pack(side="top")

        self.buttomRaport = tk.Button(self.top_frame, text='Stwórz raport', command=self.createRaport)
        self.buttomRaport.pack(side='left')

        self.separator_lineFirst = tk.Frame(self.top_frame, width=2, bd=1, relief=tk.SUNKEN)
        self.separator_lineFirst.pack(side='left', padx=5, pady=5, fill='y')

        self.text = tk.Text(self.top_frame, insertbackground='blue')
        self.text.pack(side='left', pady=10)
        self.text.config(width=10, height=1)
        self.buttomSearch = tk.Button(self.top_frame, text='Szukaj', command=self.search)
        self.buttomSearch.pack(side='left')

        self.separator_lineFirst = tk.Frame(self.top_frame, width=2, bd=1, relief=tk.SUNKEN)
        self.separator_lineFirst.pack(side='left', padx=5, pady=5, fill='y')

        self.bottom_label = tk.Label(self.top_frame, text="Sortuj po: ")
        self.bottom_label.pack(side='left')

        self.attribute_var = tk.StringVar()
        self.attribute_checkbuttons = []
        attributes = ["ID", "Nazwa", "Opis", "Cena", "Ilość", "Miara"]
        for attribute in attributes:
            checkbutton = tk.Checkbutton(self.top_frame, text=attribute, variable=self.attribute_var, onvalue=attribute,
                                         offvalue="")
            checkbutton.pack(anchor="w", side='left')
            self.attribute_checkbuttons.append(checkbutton)

        self.separator_line = tk.Frame(self.top_frame, width=2, bd=1, relief=tk.SUNKEN)
        self.separator_line.pack(side='left', padx=5, pady=5, fill='y')
        self.magazine_var = tk.BooleanVar()
        self.magazine_button = tk.Checkbutton(self.top_frame, text="Na magazynie", variable=self.magazine_var)
        self.magazine_button.pack(anchor="w", fill="both")

        self.separator1 = tk.Frame(self.main_window, height=5, bd=1, relief=tk.SUNKEN)
        self.separator1.pack(fill="x")

        self.middle_frame = tk.Frame(self.main_window)
        self.middle_frame.pack(expand=True, fill="both")
        self.search()

        self.separator2 = tk.Frame(self.main_window, height=2, bd=1, relief=tk.SUNKEN)
        self.separator2.pack(fill="x")

        self.bottom_frame = tk.Frame(self.main_window)
        self.bottom_frame.pack(side="bottom")

        column_names = ["ID", "Nazwa", "Opis", "Cena", "Ilość", "Miara"]

        for i, name in enumerate(column_names):
            label = tk.Label(self.bottom_frame, text=name)
            label.grid(row=0, column=i, padx=5, pady=5)

        record_values = ["Przykladowe Id", "Jakis Product", "Jakis Opis", "JakasOcena", "JakasIlosc", "JakasMiara"]

        self.entry_fields = []
        for i, value in enumerate(record_values):
            entry = tk.Entry(self.bottom_frame)
            entry.insert(tk.END, value)
            entry.grid(row=1, column=i, padx=5, pady=5)
            self.entry_fields.append(entry)

        button_frame = tk.Frame(self.bottom_frame)
        button_frame.grid(row=1, column=len(column_names), padx=5, pady=5, rowspan=2)

        button_dodaj = tk.Button(button_frame, text="Dodaj", command=self.add)
        button_dodaj.pack(fill="x", side='left')

        button_usun = tk.Button(button_frame, text="Usuń", command=self.delete)
        button_usun.pack(fill="x", side='left')

        button_zaktualizuj = tk.Button(button_frame, text="Zaktualizuj", command=self.update)
        button_zaktualizuj.pack(fill="x", side='left')

        button_wyczysc = tk.Button(button_frame, text="Wyczyść", command=self.clearAllValues)
        button_wyczysc.pack(fill="x", side='left')

        self.main_window.mainloop()

    def clearAllValues(self):
        for entry in self.entry_fields:
            entry.delete(0, tk.END)
    def add(self):
        data = []
        for entry in self.entry_fields:
            value = entry.get()
            if value == "":
                value = None
            data.append(value)

        if self.throwError(data):
            return

        resoult = database.add(data[0], data[1], data[2], data[3], data[5], data[4])
        if resoult == 'Not':
            tkinter.messagebox.showinfo('Error', 'Ilość nie może być poniżej zera')
            return
        if resoult == 'Not1':
            tkinter.messagebox.showinfo('Error', 'Przy nowych produktach wymagana jest nazwa')
            return
        self.search()

        tkinter.messagebox.showinfo('Operacja', 'Operacja się powiodła!')

    def throwError(self, data):
        try:
            if data[0] is not None:
                data[0] = int(data[0])
        except ValueError:
            tkinter.messagebox.showinfo('Error', 'ID must be an integer')
            return True
        try:
            if data[4] is not None:
                data[4] = float(data[4])
        except ValueError:
            tkinter.messagebox.showinfo('Error', 'Ilosc must be a float')
            return True
        try:
            if data[3] is not None:
                data[3] = float(data[3])
        except ValueError:
            tkinter.messagebox.showinfo('Error', 'Ocena must be a float')
            return True
        if data[1] is not None and len(data[1]) > 100:
            tkinter.messagebox.showinfo('Error', 'Nazwa nie może mieć więcej niż 100 znaków')
            return True
        if data[5] is not None and len(data[5]) > 50:
            tkinter.messagebox.showinfo('Error', 'Nazwa nie może mieć więcej niż 50 znaków')
            return True
        return False

    def delete(self):
        data = []
        for entry in self.entry_fields:
            value = entry.get()
            if value == "":
                value = None
            data.append(value)

        if self.throwError(data):
            return

        resoult = database.delete(data[0])
        if resoult == 'Not':
            tkinter.messagebox.showinfo('Error', 'Id cannot by null')
        self.search()
        tkinter.messagebox.showinfo('Operacja', 'Operacja się powiodła!')

    def update(self):
        data = []
        for entry in self.entry_fields:
            value = entry.get()
            if value == "":
                value = None
            data.append(value)

        if self.throwError(data):
            return

        resoult = database.update(data[0], data[1], data[2], data[3], data[5], data[4])
        if resoult == 'Not1':
            tkinter.messagebox.showinfo('Error', 'Ilość nie może być poniżej zera')
        if resoult == 'Not2':
            tkinter.messagebox.showinfo('Error', 'Id cannot by null')
        self.search()
        tkinter.messagebox.showinfo('Operacja', 'Operacja się powiodła!')

    def search(self):
        text_input = self.text.get("1.0", "end-1c")
        selected_option = self.attribute_var.get()
        if selected_option == 'Ilość':
            selected_option = 'Ilosc'
        if selected_option == 'Miara':
            selected_option = 'Miara_Ilosci'
        inMagazine = self.magazine_var.get()
        resoult = database.search(keyword=text_input, sort_by=selected_option, include_zero=inMagazine)

        for widget in self.middle_frame.winfo_children():
            if isinstance(widget, ttk.Scrollbar):
                widget.destroy()

        for widget in self.middle_frame.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.destroy()

        self.tree = ttk.Treeview(self.middle_frame, columns=("Id", "Nazwa", "Opis", "Cena", "Ilosc", "Miara_Ilosci"))

        self.tree.heading("Id", text="ID")
        self.tree.heading("Nazwa", text="Nazwa")
        self.tree.heading("Opis", text="Opis")
        self.tree.heading("Cena", text="Cena")
        self.tree.heading("Ilosc", text="Ilość")
        self.tree.heading("Miara_Ilosci", text="Miara Ilości")

        for item in resoult:
            self.tree.insert("", tk.END, values=item)

        scrollbar = ttk.Scrollbar(self.middle_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<Double-1>", self.on_tree_double_click)

    def on_tree_double_click(self,event):
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
