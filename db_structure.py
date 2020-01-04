import sqlite3
connect = sqlite3.connect('databases/structure.db')
connect.row_factory = sqlite3.Row
cursor = connect.cursor()

cursor.executescript("""
                     DROP TABLE IF EXISTS bilety;
                     DROP TABLE IF EXISTS klienci;
                     DROP TABLE IF EXISTS flota;
                     """)
connect.commit()
cursor.executescript("""
                     CREATE TABLE IF NOT EXISTS bilety (id INTEGER NOT NULL PRIMARY KEY,
                                                        imie varchar(250) NOT NULL,
                                                        nazwisko varchar(250) NOT NULL,
                                                        pesel INT(11) NOT NULL,
                                                        typ_biletu varchar(250) NOT NULL,
                                                        data_zakupu varchar(250) NOT NULL,
                                                        prz_poczatkowy varchar(250) NOT NULL,
                                                        prz_koncowy varchar(250) NOT NULL,
                                                        kierunek varchar(250) NOT NULL,
                                                        czas_zakupu varchar(250) NOT NULL,
                                                        czas_wygasniecia varchar(250) NOT NULL,
                                                        czas_wygasniecia_dump varchar(250) NOT NULL,
                                                        id_biletu VARCHAR(250) NOT NULL,
                                                        id_klienta VARCHAR(250) NOT NULL);
                     CREATE TABLE IF NOT EXISTS klienci (id INTEGER NOT NULL PRIMARY KEY UNIQUE,
                                                         imie varchar(250) NOT NULL,
                                                         nazwisko varchar(250) NOT NULL,
                                                         pesel int(11) NOT NULL,
                                                         id_klient varchar(250) NOT NULL);
                     CREATE TABLE IF NOT EXISTS flota (id INTEGER NOT NULL PRIMARY KEY,
                                                       kierunek VARCHAR(250) NOT NULL,
                                                       prz_poczatkowy VARCHAR(250) NOT NULL,
                                                       prz_koncowy VARCHAR(250) NOT NULL,
                                                       nr_lini INT NOT NULL,
                                                       typ_pojazdu VARCHAR(250) NOT NULL,
                                                       rozklad_jazdy VARCHAR(250) NOT NULL,
                                                       strefa INT NOT NULL);
                     """)
connect.commit()

flota = (
            ("Bronowice", "Babie lato","Bronowice wiadukt","501","autobus","10:10|11:12|13:38","1"),
            ("Bronowice", "Knapczyka","Bronowice wiadukt","17","autobus","07:12|08:36|12:50","1"),
            ("Bronowice Małe", "Solskiego","Teatr Bagatela","168","autobus","06:20|13:55|17:30","1"),
            ("Azory", "Budryka","Azory pętla","173","autobus","04:05|10:39|15:23","1"),
            ("Manie", "Babie lato","Bronowice wiadukt","601","tramwaj","00:15|02:18|04:24","1")
        )

cursor.executemany('INSERT INTO flota VALUES(NULL,?,?,?,?,?,?,?)', flota)
connect.commit()