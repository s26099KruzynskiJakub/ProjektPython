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
    def add(Id,Nazwa=None,Opis=None,Cena=None,Miara_Ilosci=None,Ilosc=None):
        if Ilosc is not None and Ilosc <0:
            return 'Not'
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
            connection.close()
            return 'Ok'
        query = "SELECT Ilosc FROM Magazyn WHERE Produkt_Id = ?"
        cursor.execute(query, (Id,))
        result = cursor.fetchone()
        if result:
            query = "UPDATE Magazyn SET Ilosc = ? WHERE Produkt_Id = ?"
            cursor.execute(query, (Ilosc, Id))
            connection.commit()
            connection.close()
            return 'Ok'
        product_data = (Nazwa, Opis, Cena, Miara_Ilosci)
        query = "INSERT INTO Produkt (Nazwa, Opis, Cena, Miara_Ilosci) VALUES (?, ?, ?, ?)"
        cursor.execute(query, product_data)
        product_id = cursor.lastrowid
        magazyn_data = (product_id, Ilosc)
        query = "INSERT INTO Magazyn (Produkt_Id, Ilosc) VALUES (?, ?)"
        cursor.execute(query, magazyn_data)
        connection.commit()
        connection.close()
        return 'Ok'

    @staticmethod
    def update(Id, Nazwa=None, Opis=None, Cena=None, Miara_Ilosci=None, Ilosc=None):
        if Ilosc is not None and Ilosc < 0:
            return 'Not1'
        if Id is None:
            return 'Not2'
        conn = sqlite3.connect('baza.db')
        cursor = conn.cursor()

        update_values = []
        if Nazwa is not None:
            update_values.append("Nazwa = '{}'".format(Nazwa))
        if Opis is not None:
            update_values.append("Opis = '{}'".format(Opis))
        if Cena is not None:
            update_values.append("Cena = {}".format(Cena))
        if Miara_Ilosci is not None:
            update_values.append("Miara_Ilosci = '{}'".format(Miara_Ilosci))

        update_query = "UPDATE Produkt SET " + ", ".join(update_values) + " WHERE Id = {}".format(Id)

        if Ilosc is not None:
            update_query_magazyn = "UPDATE Magazyn SET Ilosc = {} WHERE Produkt_Id = {}".format(Ilosc, Id)
            cursor.execute(update_query_magazyn)

        cursor.execute(update_query)
        conn.commit()
        conn.close()
        return 'Ok'

    @staticmethod
    def delete(Id):
        if Id is None:
            print("ID cannot be null.")
            return 'Not'

        conn = sqlite3.connect('baza.db')
        cursor = conn.cursor()

        delete_query_produkt = "DELETE FROM Produkt WHERE Id = {}".format(Id)
        cursor.execute(delete_query_produkt)

        delete_query_magazyn = "DELETE FROM Magazyn WHERE Produkt_Id = {}".format(Id)
        cursor.execute(delete_query_magazyn)
        conn.commit()
        conn.close()
        return 'Ok'

    @staticmethod
    def search(keyword=None, sort_by=None, include_zero=False):
        conn = sqlite3.connect('baza.db')
        cursor = conn.cursor()

        query = "SELECT Produkt.Id, Produkt.Nazwa, Produkt.Opis, Produkt.Cena, Produkt.Miara_Ilosci, Magazyn.Ilosc " \
                "FROM Produkt " \
                "LEFT JOIN Magazyn ON Produkt.Id = Magazyn.Produkt_Id"

        if keyword is not None:
            query += " WHERE Produkt.Id LIKE '%{}%' OR Produkt.Nazwa LIKE '%{}%'".format(keyword, keyword)

        if sort_by is not None and sort_by != '':
            query += " ORDER BY {}".format(sort_by)

        cursor.execute(query)
        rows = cursor.fetchall()

        results = []
        for row in rows:
            Id, Nazwa, Opis, Cena, Miara_Ilosci, Ilosc = row
            if not include_zero and Ilosc == 0:
                continue
            results.append((Id, Nazwa, Opis, Cena, Miara_Ilosci, Ilosc))

        conn.close()
        return results



