import os
import sqlite3


class database:
    """
       Klasa `database` odpowiada za zarządzanie bazą danych produktów.

       Metody:
       - __init__(): Konstruktor klasy, tworzy bazę danych, jeśli nie istnieje.
       - createDatabase(): Tworzy tabelę Produkt i wstawia przykładowe dane.
       - add(): Dodaje nowy produkt do bazy danych.
       - update(): Aktualizuje informacje o produkcie w bazie danych.
       - delete(): Usuwa produkt z bazy danych.
       - search(): Wyszukuje produkty w bazie danych.

       Atrybuty:
       Brak.

       """
    def __init__(self):
        """
        Konstruktor klasy, tworzy bazę danych, jeśli nie istnieje.

        Argumenty:
        Brak.

        Zwraca:
        None.

        """
        database_file = 'baza.db'
        if not os.path.isfile(database_file):
            self.createDatabase()

    def createDatabase(self):
        """
        Tworzy tabelę Produkt w bazie danych i wstawia przykładowe dane.

        Argumenty:
        Brak.

        Zwraca:
        None.

        """
        connection = sqlite3.connect('baza.db')
        cursor = connection.cursor()
        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS Produkt (
            Id integer NOT NULL CONSTRAINT Produkt_pk PRIMARY KEY ASC,
            Nazwa varchar(100) NOT NULL,
            Opis text,
            Cena double,
            Miara_Ilosci varchar(50),
            Ilosc double
            );
            """
        )
        cursor.execute('INSERT INTO Produkt VALUES(NULL, ?, ?, ?, ?, ?);',('Mleko','Mleko w kartonie bez laktozy',2.4,'1 l',3))
        cursor.execute('INSERT INTO Produkt VALUES(NULL, ?, ?, ?, ?, ?);',('Mleko kokosowe','Mleko kokosowe w kartonie bez laktozy',3.4,'1 l',65))
        connection.commit()
        connection.close()

    @staticmethod
    def add(Id=None,Nazwa=None,Opis=None,Cena=None,Miara_Ilosci=None,Ilosc=None):
        """
        Dodaje nowy produkt do bazy danych.

        Argumenty:
        - Id (int): Identyfikator produktu. Jeśli None, zostanie automatycznie wygenerowany.
        - Nazwa (str): Nazwa produktu.
        - Opis (str): Opis produktu.
        - Cena (float): Cena produktu.
        - Miara_Ilosci (str): Jednostka miary ilości produktu.
        - Ilosc (float): Dostępna ilość produktu.

         Zwraca:
         - 'Ok' (str): Dodanie produktu powiodło się.
         - 'Not' (str): Nieprawidłowa wartość ilości produktu.

        """
        if Ilosc is not None and Ilosc < 0:
            return 'Not'
        connection = sqlite3.connect('baza.db')
        cursor = connection.cursor()
        query = "SELECT Ilosc FROM Produkt WHERE (Id = ? OR (Nazwa = ? AND Opis = ? AND Cena = ? AND Miara_Ilosci = ?)) AND Ilosc > 0"
        cursor.execute(query, (Id,Nazwa,Opis,Cena,Miara_Ilosci))
        result = cursor.fetchone()
        if result:
            poZmianie = result[0] + Ilosc
            query = "UPDATE Produkt SET Ilosc = ? WHERE Id = ?"
            cursor.execute(query, (poZmianie, Id))
            connection.commit()
            connection.close()
            return 'Ok'
        query = "SELECT Ilosc FROM Produkt WHERE Id = ?"
        cursor.execute(query, (Id,))
        result = cursor.fetchone()
        if result:
            query = "UPDATE Produkt SET Ilosc = ? WHERE Id = ?"
            cursor.execute(query, (Ilosc, Id))
            connection.commit()
            connection.close()
            return 'Ok'
        if Nazwa is None:
            return 'Not1'
        if Ilosc is None:
            Ilosc = 0
        product_data = (Nazwa, Opis, Cena, Miara_Ilosci, Ilosc)
        query = "INSERT INTO Produkt (Nazwa, Opis, Cena, Miara_Ilosci, Ilosc) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, product_data)
        connection.commit()
        connection.close()
        return 'Ok'



    @staticmethod
    def update(Id, Nazwa=None, Opis=None, Cena=None, Miara_Ilosci=None, Ilosc=None):
        """
                Aktualizuje informacje o produkcie w bazie danych.

                Argumenty:
                - Id (int): Identyfikator produktu.
                - Nazwa (str): Nowa nazwa produktu. Jeśli None, nazwa nie zostanie zmieniona.
                - Opis (str): Nowy opis produktu. Jeśli None, opis nie zostanie zmieniony.
                - Cena (float): Nowa cena produktu. Jeśli None, cena nie zostanie zmieniona.
                - Miara_Ilosci (str): Nowa jednostka miary ilości produktu. Jeśli None, jednostka miary ilości nie zostanie zmieniona.
                - Ilosc (float): Nowa dostępna ilość produktu. Jeśli None, ilość nie zostanie zmieniona.

                Zwraca:
                - 'Ok' (str): Aktualizacja produktu powiodła się.
                - 'Not1' (str): Nieprawidłowa wartość ilości produktu.
                - 'Not2' (str): Brak identyfikatora produktu.

                """
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
        if Ilosc is not None:
            update_values.append("Ilosc = {}".format(Ilosc))
        update_query = "UPDATE Produkt SET " + ", ".join(update_values) + " WHERE Id = {}".format(Id)

        cursor.execute(update_query)
        conn.commit()
        conn.close()
        return 'Ok'

    @staticmethod
    def delete(Id):
        """
               Usuwa produkt z bazy danych.

               Argumenty:
               - Id (int): Identyfikator produktu.

               Zwraca:
               - 'Ok' (str): Usunięcie produktu powiodło się.
               - 'Not' (str): Brak identyfikatora produktu.

               """
        if Id is None:
            print("ID cannot be null.")
            return 'Not'

        conn = sqlite3.connect('baza.db')
        cursor = conn.cursor()

        delete_query_produkt = "DELETE FROM Produkt WHERE Id = {}".format(Id)
        cursor.execute(delete_query_produkt)

        conn.commit()
        conn.close()
        return 'Ok'

    @staticmethod
    def search(keyword=None, sort_by=None, include_zero=False):
        """
                Wyszukuje produkty w bazie danych.

                Argumenty:
                - keyword (str): Słowo kluczowe do wyszukania. Jeśli None, zostaną zwrócone wszystkie produkty.
                - sort_by (str): Pole, według którego mają zostać posortowane wyniki. Jeśli None, wyniki nie będą sortowane.
                - include_zero (bool): Określa, czy wyniki powinny zawierać produkty o ilości równej zero.

                Zwraca:
                - results (list): Lista wyników zawierających krotki (Id, Nazwa, Opis, Cena, Ilosc, Miara_Ilosci).

                """
        conn = sqlite3.connect('baza.db')
        cursor = conn.cursor()

        query = "SELECT Id, Nazwa, Opis, Cena, Miara_Ilosci, Ilosc FROM Produkt "


        if keyword is not None and keyword != '':
            query += " WHERE Produkt.Id LIKE '%{}%' OR Produkt.Nazwa LIKE '%{}%'".format(keyword, keyword)

        if sort_by is not None and sort_by != '':
            query += " ORDER BY {} DESC".format(sort_by)

        cursor.execute(query)
        rows = cursor.fetchall()

        results = []
        for row in rows:
            Id, Nazwa, Opis, Cena, Miara_Ilosci, Ilosc = row
            if include_zero and Ilosc == 0:
                continue
            results.append((Id, Nazwa, Opis, Cena, Ilosc, Miara_Ilosci))

        conn.close()
        return results



