import tkinter as tk

class GUI:
    def __init__(self):
        self.main_window = tk.Tk()

        # Top Frame
        self.top_frame = tk.Frame(self.main_window)
        self.main_window.title("MAGAZYN")
        self.top_frame.pack(side="top")
        self.top_label = tk.Label(self.top_frame, text="Top Frame")
        self.top_label.pack()

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

        tk.mainloop()

# Create an instance of the GUI class
gui = GUI()

# metoda createDatabase tworząca bazę danych
# metoda addValuesToDatabase dodająca podstawowe wartości
# metoda serch zwracająca listę danych wraz z mozliwością szukania po nazwa lub id oraz order by
# metoda init króra sprawdza czy bazadanych istnieje i może wyłować create
# metoda modyfikujProdukt zmienia informacje o produkcie
# metoda usunProdukt usuwa produkt