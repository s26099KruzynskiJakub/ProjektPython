import tkinter as tk

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

        self.listbox = tk.Listbox(self.middle_frame)
        self.listbox.pack(expand=True, fill="both")

        # Separator Line
        self.separator2 = tk.Frame(self.main_window, height=2, bd=1, relief=tk.SUNKEN)
        self.separator2.pack(fill="x")

        # Bottom Frame
        self.bottom_frame = tk.Frame(self.main_window)
        self.bottom_frame.pack(side="bottom")

        # List of column names
        column_names = ["ID", "Nazwa", "Opis", "Ocena", "Ilość", "Miara"]

        # Create labels for column names
        for i, name in enumerate(column_names):
            label = tk.Label(self.bottom_frame, text=name)
            label.grid(row=0, column=i, padx=5, pady=5)

        # List of record values
        record_values = ["1", "Jakis Product", "Jakis Opis", "JakasOcena", "JakasIlosc", "JakasMiara"]

        # Create entry fields for record values
        entry_fields = []
        for i, value in enumerate(record_values):
            entry = tk.Entry(self.bottom_frame)
            entry.insert(tk.END, value)
            entry.grid(row=1, column=i, padx=5, pady=5)
            entry_fields.append(entry)

            # Create buttons
            button_frame = tk.Frame(self.bottom_frame)
            button_frame.grid(row=1, column=len(column_names), padx=5, pady=5, rowspan=2)

            button_dodaj = tk.Button(button_frame, text="Dodaj")
            button_dodaj.pack(fill="x", side='left')

            button_usun = tk.Button(button_frame, text="Usuń")
            button_usun.pack(fill="x", side='left')

            button_zaktualizuj = tk.Button(button_frame, text="Zaktualizuj")
            button_zaktualizuj.pack(fill="x",side='left')

        self.main_window.mainloop()

    def submit_values(self, entry_fields):
        # Retrieve the values from the entry fields
        values = [entry.get() for entry in entry_fields]
        # Do something with the values
        print(values)

    def call_method(self,event=None):
        text_input = self.text.get("1.0", "end-1c")  # Retrieve text from the text field
        print(text_input)  # Call the method with the text input
        self.text.delete("1.0", "end")

    def call_method2(self,event=None):
        text_input = self.text1.get("1.0", "end-1c")  # Retrieve text from the text field
        print(text_input)  # Call the method with the text input
        self.text.delete("1.0", "end")


    def update_list(self):
        # Clear the existing items in the listbox
        self.listbox.delete(0, tk.END)

        # Add new items to the listbox
        items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
        for item in items:
            self.listbox.insert(tk.END, item)


    def add(self):
        return 0

    def delete(self):
        return 0

    def update(self):
        return 0

    def search(self):
        return 0

# Create an instance of the GUI class
gui = GUI()

# metoda createDatabase tworząca bazę danych
# metoda addValuesToDatabase dodająca podstawowe wartości
# metoda serch zwracająca listę danych wraz z mozliwością szukania po nazwa lub id oraz order by
# metoda init króra sprawdza czy bazadanych istnieje i może wyłować create
# metoda modyfikujProdukt zmienia informacje o produkcie
# metoda usunProdukt usuwa produkt