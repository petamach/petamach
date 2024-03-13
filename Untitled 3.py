import sqlite3
from sqlite3 import Error
import os


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        return sqlite3.connect(db_file)
    except Error as e:
        print(e)


def create_tables(conn):
    sql_code = """
    DROP TABLE IF EXISTS Obedy;
    DROP TABLE IF EXISTS Rozvrh_Obedu;
    DROP TABLE IF EXISTS Restaurace;
    DROP TABLE IF EXISTS Recenze;
    """
    c = conn.cursor()
    c.executescript(sql_code)

    
    sql_code = """
    CREATE TABLE IF NOT EXISTS Obedy (
        ObedID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nazev VARCHAR(255) NOT NULL,
        Alergeny VARCHAR(255),
        Vege VARCHAR(50),
        Cena INTEGER
    );
    """
    c.execute(sql_code)

    
    sql_code = """
    CREATE TABLE IF NOT EXISTS Rozvrh_Obedu (
        Datum DATE NOT NULL,
        IDObed INTEGER NOT NULL,
        FOREIGN KEY (IDObed) REFERENCES Obedy(ObedID)
    );
    """
    c.execute(sql_code)

    sql_code = """
    CREATE TABLE IF NOT EXISTS Restaurace (
        RestauraceID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nazev VARCHAR(255) NOT NULL,
        Adresa VARCHAR(255),
        Telefon VARCHAR(20)
    );
    """
    c.execute(sql_code)

    
    sql_code = """
    CREATE TABLE IF NOT EXISTS Recenze (
        RecenzeID INTEGER PRIMARY KEY AUTOINCREMENT,
        Hodnoceni INTEGER NOT NULL,
        Komentar TEXT,
        RestauraceID INTEGER NOT NULL,
        FOREIGN KEY (RestauraceID) REFERENCES Restaurace(RestauraceID)
    );
    """
    c.execute(sql_code)

    conn.commit()


def insert_data(conn):
    sql_code = """
    INSERT INTO Obedy (Nazev, Alergeny, Vege, Cena)
    VALUES ("Kuře na paprice", "1", 0, 156),
           ("Gulaš", "4", 0, 112),
           ("Falafel", "1,4", 1, 92),
           ("Kuskus", "1,4", 1, 192),
           ("Bulgur pšenice", "1,4", 1, 115);
    """
    c = conn.cursor()
    c.executescript(sql_code)

    
    with open("jidla.txt", "r") as f:
        for line in f.readlines():
            datum, obed_id = line.strip().split(",")
            sql_code = f"""
            INSERT INTO Rozvrh_Obedu (Datum, IDObed)
            VALUES ("{datum}", {obed_id});
            """
            c.execute(sql_code)

    sql_code = """
    INSERT INTO Restaurace (Nazev, Adresa, Telefon)
    VALUES ("U draka", "Dlouhá 123, Praha 1", "222111222"),
           ("Indická restaurace", "Národní 34, Brno", "555444333");
    """
    c.executescript(sql_code)

    sql_code = """
    INSERT INTO Recenze (Hodnoceni, Komentar, RestauraceID)
    VALUES (5, "Výborné jídlo, rychlá obsluha", 1),
           (4, "Trochu delší čekání, ale chuťově super", 2);
    """  

    c.executescript(sql_code)
    conn.commit()


def select_data(conn):

    
    sql_code = "SELECT * FROM Obedy;"
    c = conn.cursor()
    cursor = c.execute(sql_code)
    print("Všechny obědy:")
    for row in cursor.fetchall():
        print(row)

    sql_code = """
    SELECT o.Nazev, ro.Datum
    FROM Rozvrh_Obedu ro
    JOIN Obedy o ON ro.IDObed = o.ObedID
    WHERE ro.Datum >= date('now');
    """
    c = conn.cursor()
    cursor = c.execute(sql_code)
    print("\nObědy od dnešního data:")
    for row in cursor.fetchall():
        print(row)

    sql_code = "SELECT * FROM Restaurace WHERE Telefon LIKE '%222%';"
    c = conn.cursor()
    cursor = c.execute(sql_code)
    print("\nRestaurace s telefonním číslem obsahujícím '222':")
    for row in cursor.fetchall():
        print(row)

    sql_code = "SELECT * FROM Recenze WHERE Hodnoceni = 5 ORDER BY RestauraceID DESC;"
    c = conn.cursor()
    cursor = c.execute(sql_code)
    print("\nRecenze s hodnocením 5 seřazené podle RestauraceID sestupně:")
    for row in cursor.fetchall():
        print(row)


def update_data(conn):

    sql_code = "UPDATE Obedy SET Cena = Cena + 20 WHERE Vege = 1;"
    c = conn.cursor()
    c.execute(sql_code)
    conn.commit()
    print("\nCena vegetariánských obědů navýšena o 20 Kč.")

    sql_code = """
    UPDATE Restaurace
    SET Adresa = 'Národní třída 34, Brno'
    WHERE RestauraceID = 2;
    """
    c = conn.cursor()
    c.execute(sql_code)
    conn.commit()
    print("\nAdresa Indické restaurace změněna.")


def delete_data(conn):

    sql_code = "DELETE FROM Rozvrh_Obedu WHERE Datum < date('now','-7 day');" 
    c = conn.cursor()
    c.execute(sql_code)
    conn.commit()
    print("\nSmazány záznamy v Rozvrh_Obedu starší než 7 dní.")

   
    sql_code = "DELETE FROM Restaurace WHERE RestauraceID = 1;"
    c = conn.cursor()
    c.execute(sql_code)
    conn.commit()
    print("\nRestaurace 'U draka' smazána.")


if __name__ == "__main__":
    if not os.path.exists(r"C:\sqlite\db"):
        os.makedirs(r"C:\sqlite\db")
    conn = create_connection(r"C:\sqlite\db\pythonsqlite.db")

    create_tables(conn)
    insert_data(conn)

    # select_data(conn)
    # update_data(conn)
    # delete_data(conn)

    conn.close()
    
    
    