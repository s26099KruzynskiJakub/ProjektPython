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
        self.middle_label = tk.Label(self.middle_frame, text="Middle Frame")
        self.middle_label.pack()

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



    def select_value(self):
        # Function to handle the button click event
        selected_value = self.value_button.cget("text")
        if selected_value == "Name":
            self.value_button.configure(text="ID")
        else:
            self.value_button.configure(text="Name")

# Create an instance of the GUI class
gui = GUI()

# metoda createDatabase tworząca bazę danych
# metoda addValuesToDatabase dodająca podstawowe wartości
# metoda serch zwracająca listę danych wraz z mozliwością szukania po nazwa lub id oraz order by
# metoda init króra sprawdza czy bazadanych istnieje i może wyłować create
# metoda modyfikujProdukt zmienia informacje o produkcie
# metoda usunProdukt usuwa produkt