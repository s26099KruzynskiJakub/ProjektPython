import os
import sqlite3


class database:
    def __init__(self):
        database_file = 'baza.db'
        if not os.path.isfile(database_file):
            self.createDatabase()

    def createDatabase(self):
        connection = sqlite3.connect('baza.db')
        cursor = connection.cursor()
        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS Produkt (
            Id integer NOT NULL CONSTRAINT Produkt_pk PRIMARY KEY ASC,
            Nazwa varchar(100) NOT NULL,
            Opis text NOT NULL,
            Cena double NOT NULL,
            Miara_Ilosci varchar(50) NOT NULL
            );
            CREATE TABLE Magazyn (
            Produkt_Id integer NOT NULL CONSTRAINT Magazyn_pk PRIMARY KEY,
            Ilosc double NOT NULL,
            CONSTRAINT Produkt_na_magazynie_Produkt FOREIGN KEY (Produkt_Id)
            REFERENCES Produkt (Id)
            );
            """
        )
        cursor.execute('INSERT INTO Produkt VALUES(NULL, ?, ?, ?, ?);',('Mleko','Mleko w kartonie bez laktozy',2.4,'1 l'))
        cursor.execute('INSERT INTO Produkt VALUES(NULL, ?, ?, ?, ?);',('Mleko kokosowe','Mleko kokosowe w kartonie bez laktozy',3.4,'1 l'))

        cursor.execute('INSERT INTO Magazyn VALUES(?,?);',(1,3))
        cursor.execute('INSERT INTO Magazyn VALUES(?,?);',(2,13))

        connection.commit()
        connection.close()

    @staticmethod
    def add(Id,Nazwa,Opis,Cena,Miara_Ilosci,Ilosc):
        connection = sqlite3.connect('baza.db')
        cursor = connection.cursor()
        query = "SELECT Ilosc FROM Magazyn WHERE Produkt_Id = ? AND Ilosc > 0"
        cursor.execute(query, (Id,))
        result = cursor.fetchone()
        if result:
            poZmianie = result[0] + Ilosc
            query = "UPDATE Magazyn SET Ilosc = ? WHERE Produkt_Id = ?"
            cursor.execute(query, (poZmianie, Id))
            connection.commit()
            return 'Ok'
        query = "SELECT Ilosc FROM Magazyn WHERE Produkt_Id = ?"
        cursor.execute(query, (Id,))
        result = cursor.fetchone()
        if result:
            query = "UPDATE Magazyn SET Ilosc = ? WHERE Produkt_Id = ?"
            cursor.execute(query, (Ilosc, Id))
            connection.commit()
            return 'Ok'


        connection.commit()
        connection.close()




MyDatabase = database()

    #metoda addValuesToDatabase dodająca podstawowe wartości
    #metoda serch zwracająca listę danych wraz z mozliwością szukania po nazwa lub id oraz order by
    #metoda init króra sprawdza czy bazadanych istnieje i może wyłować create
    #metoda modyfikujProdukt zmienia informacje o produkcie
    #metoda usunProdukt usuwa produkt
