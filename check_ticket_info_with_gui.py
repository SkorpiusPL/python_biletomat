import sys
from PyQt5.QtWidgets import (QTableWidget, QTableWidgetItem, QWidget, QLabel, QLineEdit, QTextEdit, QComboBox, QGridLayout, QApplication, QPushButton, QAction, QFileDialog,  QMainWindow, QInputDialog, QFormLayout)
from PyQt5.QtCore import *
import sqlite3
import datetime
import hashlib
import re

connect = sqlite3.connect('databases/structure.db')
connect.row_factory = sqlite3.Row
cursor = connect.cursor()


class Okno(QWidget):

    def __init__(self):
        super(Okno, self).__init__()
        self.imie_s = QLineEdit()
        self.imie_s.setFocus()
        self.nazwisko_s = QLineEdit()
        self.idb_s = QLineEdit()
        self.wynik_table = QTableWidget()
        self.wynik = QLineEdit()
        self.wynik.setDisabled(True)
        self.sprawdz = QPushButton("&Sprawdz")
        self.czysc = QPushButton("&Czysc")
        
        self.interfejs()

    def interfejs(self):
        tytul = QLabel("SPRAWDŹ INFORMACJE O BILECIE", self)
        imie = QLabel("Podaj imię: ", self)
        nazwisko = QLabel("Podaj nazwisko: ", self)
        idb = QLabel("Podaj identyfikator biletu: ", self)
        
        ukladT = QGridLayout()
        ukladT.setSpacing(10)
        ukladT.addWidget(tytul, 0, 1)
        ukladT.addWidget(imie, 1, 0)
        ukladT.addWidget(nazwisko, 1,1)
        ukladT.addWidget(idb, 1,2)
        
        ukladT.addWidget(self.imie_s, 2, 0)
        ukladT.addWidget(self.nazwisko_s, 2, 1)
        ukladT.addWidget(self.idb_s, 2, 2)
        ukladT.addWidget(self.wynik, 5, 0,3,0)
        ukladT.addWidget(self.wynik_table, 10, 0,3,0)
        ukladT.addWidget(self.sprawdz, 3, 1)
        ukladT.addWidget(self.czysc, 3, 2)

        # przypisanie utworzonego układu do okna
        self.sprawdz.clicked.connect(self.dzialanie)
        self.czysc.clicked.connect(self.dzialanie)
        
        self.setLayout(ukladT)
        self.setGeometry(150, 100, 330, 300)
        self.setWindowTitle("Automatyczny biletomat- rozklad jazdy na podstawie bilety")
        self.show()
        

    def dzialanie(self):
        dzialania = self.sender()
        wartosc = str(dzialania.text())
        im = str(self.imie_s.text())
        in_= str(self.nazwisko_s.text())
        idb = self.idb_s.text()
        
        if wartosc == "&Sprawdz":
            
            if im == "":
                self.wynik.setText("Brak danych. Wpisz dane")
            elif bool(re.match(r'[A-ZŚŻŹĆŁĄ]{1}[a-zśąęóżźćł]{2,}$', im)) == False:
                self.wynik.setText("Imie zaczyna się od dużej litery")
            elif in_ == "":
                self.wynik.setText("Brak danych. Wpisz dane")
            elif bool(re.match(r'[A-ZŚŻŹĆŁĄ]{1}[a-zśąęóżźćł]{2,}$', in_)) == False:
                self.wynik.setText("Nazwisko zaczyna się od dużej litery")
            elif idb == "":
                self.wynik.setText("Brak danych. Wpisz dane")
            elif bool(re.match(r'[0-9A-Za-z]{10}$', idb)) == False:
                self.wynik.setText("Zły fomat identyfikatora")
            else:
                self.wynik.setText("Wprowadzono poprawne dane. Rozkład jazdy niżej")
                #self.wynik.setText(im+" "+in_+" "+ipes+" ->"+idk)
                
                cursor.execute("SELECT * FROM bilety WHERE imie=? AND nazwisko=? AND id_biletu=?",(im, in_, idb))
                bilety = cursor.fetchall()
                ilosc = len(bilety)
                if ilosc == 1:
                    for bilet in bilety:
                        cursor.execute("SELECT * FROM flota WHERE prz_poczatkowy=? AND prz_koncowy=? AND kierunek=?",(bilet['prz_poczatkowy'], bilet['prz_koncowy'], bilet['kierunek']))
                        flota = cursor.fetchall()
                        self.wynik_table.setRowCount(len(flota))
                        self.wynik_table.setColumnCount(5)
                        self.wynik_table.setHorizontalHeaderLabels(['Numer linii', 'Kierunek jazdy', 'Typ pojazdu', 'Numer strefy', 'Rozkład jazdy'])
                        ile = len(flota)
                        if ile > 0:
                            for i,komunikacja in enumerate(flota):
                                self.wynik_table.setItem(i,0, QTableWidgetItem(komunikacja['nr_linii']))
                                self.wynik_table.setItem(i,1, QTableWidgetItem(komunikacja['kierunek']))
                                self.wynik_table.setItem(i,2, QTableWidgetItem(komunikacja['typ_pojazdu']))
                                self.wynik_table.setItem(i,3, QTableWidgetItem(komunikacja['strefa']))
                                self.wynik_table.setItem(i,4, QTableWidgetItem(komunikacja['rozklad_jazdy']))
                        else:
                            self.wynik.setText("Nie ma pojazdow odpowiadajacych twoim upodobaniom. Sprobuj ponownie.")
                else:
                    self.wynik.setText("Dane są niepoprawne. Sprobuj ponownie.")
                    self.imie_s.setText("")
                    self.nazwisko_s.setText("")
                    self.idb_s.setText("")
                connect.commit()
            
        elif wartosc == "&Czysc":
            self.imie_s.setText("")
            self.nazwisko_s.setText("")
            self.idb_s.setText("")
            self.wynik.setText("Wyczyszczone")
        else:
            pass
            
        
        #self.wynik.setText(wartosc)
            
if __name__ == '__main__':

    app = QApplication(sys.argv)
    okno = Okno()
    sys.exit(app.exec_())
