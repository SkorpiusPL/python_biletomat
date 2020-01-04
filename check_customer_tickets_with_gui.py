import sys
from PyQt5.QtWidgets import (QTableWidget,QTableWidgetItem,QWidget, QLabel, QLineEdit, QTextEdit, QComboBox, QGridLayout, QApplication, QPushButton, QAction, QFileDialog,  QMainWindow, QInputDialog, QFormLayout)
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
        self.pesel_s = QLineEdit()
        self.idk_s = QLineEdit()
        self.wynik_table = QTableWidget()
        self.wynik = QLineEdit()
        self.wynik.setDisabled(True)
        self.wynik.setToolTip('Tu będzie wynik tekstu')
        self.login = QPushButton("&Zaloguj")
        self.czysc = QPushButton("&Czysc")
        
        self.interfejs()

    def interfejs(self):
        tytul = QLabel("SPRAWDŹ INFORMACJE O BILETACH", self)
        imie = QLabel("Podaj imię: ", self)
        nazwisko = QLabel("Podaj nazwisko: ", self)
        pesel = QLabel("Podaj numer pesel: ", self)
        identyfikator_k = QLabel("Identyfikator klienta: ", self)
        
        ukladT = QGridLayout()
        ukladT.setSpacing(10)
        ukladT.addWidget(tytul, 0, 1)
        ukladT.addWidget(imie, 1, 0)
        ukladT.addWidget(nazwisko, 1,1)
        ukladT.addWidget(pesel, 1,2)
        
        ukladT.addWidget(identyfikator_k, 3,0)
        
        ukladT.addWidget(self.idk_s, 5,0)
        ukladT.addWidget(self.imie_s, 2, 0)
        ukladT.addWidget(self.nazwisko_s, 2, 1)
        ukladT.addWidget(self.pesel_s, 2, 2)
        ukladT.addWidget(self.wynik, 6, 0,3,0)
        ukladT.addWidget(self.wynik_table, 10,0,3,3)
        ukladT.addWidget(self.login, 5, 1)
        ukladT.addWidget(self.czysc, 5, 2)

        # przypisanie utworzonego układu do okna
        self.login.clicked.connect(self.dzialanie)
        self.czysc.clicked.connect(self.dzialanie)
        
        self.setLayout(ukladT)
        self.setGeometry(150, 100, 330, 300)
        self.setWindowTitle("Automatyczny biletomat- wyswietlenie informacji o biletach zakupionych przez klienta")
        self.show()
        

    def dzialanie(self):
        dzialania = self.sender()
        wartosc = str(dzialania.text())
        im = str(self.imie_s.text())
        in_= str(self.nazwisko_s.text())
        ipes = self.pesel_s.text()
        idk = str(self.idk_s.text())
        
        if wartosc == "&Zaloguj":
            
            if im == "":
                self.wynik.setText("Brak danych. Wpisz dane")
            elif bool(re.match(r'[A-ZŚŻŹĆŁĄ]{1}[a-zśąęóżźćł]{2,}$', im)) == False:
                self.wynik.setText("Imie zaczyna się od dużej litery")
            elif in_ == "":
                self.wynik.setText("Brak danych. Wpisz dane")
            elif bool(re.match(r'[A-ZŚŻŹĆŁĄ]{1}[a-zśąęóżźćł]{2,}$', in_)) == False:
                self.wynik.setText("Nazwisko zaczyna się od dużej litery")
            elif ipes == "":
                self.wynik.setText("Brak danych. Wpisz dane")
            elif bool(re.match(r'[0-9]{11}$', ipes)) == False:
                self.wynik.setText("Zły fomat numeru Pesel")
            elif bool(re.match(r'[0-9A-Za-z]{5}$', idk)) == False:
                self.wynik.setText("Zły format identyfikatora")
            elif idk == "":
                self.wynik.setText("Wpisz identyfikator klienta")
            else:
                obecnie = datetime.datetime.now()
                now_timestamp = obecnie.timestamp()
                self.wynik.setText("Wprowadzono poprawne dane. Lista biletow niżej")
                #self.wynik.setText(im+" "+in_+" "+ipes+" ->"+idk)
                
                cursor.execute("SELECT * FROM klienci WHERE imie=? AND nazwisko=? AND pesel=? AND id_klient=?",(im, in_, ipes, idk))
                klienci = cursor.fetchall()
                ilosc = len(klienci)
                if ilosc == 1:
                    cursor.execute("SELECT * FROM bilety WHERE imie=? AND nazwisko=? AND id_klienta=?",(im, in_, idk))
                    bilety = cursor.fetchall()
                    self.wynik_table.setRowCount(len(bilety))
                    self.wynik_table.setColumnCount(6)
                    self.wynik_table.setHorizontalHeaderLabels(['Identyfikator biletu', 'Data zakupu', 'Kierunek jazdy', 'Przystanek początkowy', 'Przystanek końcowy', 'Status biletu'])
                    for i,bilet in enumerate(bilety):
                        self.wynik_table.setItem(i,0, QTableWidgetItem(bilet['id_biletu']))
                        self.wynik_table.setItem(i,1, QTableWidgetItem(bilet['data_zakupu']))
                        self.wynik_table.setItem(i,2, QTableWidgetItem(bilet['kierunek']))
                        self.wynik_table.setItem(i,3, QTableWidgetItem(bilet['prz_poczatkowy']))
                        self.wynik_table.setItem(i,4, QTableWidgetItem(bilet['prz_koncowy']))
                        if float(float(bilet['czas_wygasniecia_dump']) - now_timestamp) > 0:
                            self.wynik_table.setItem(i,5, QTableWidgetItem("Aktywny"))
                        else:
                            self.wynik_table.setItem(i,5, QTableWidgetItem("Nieaktywny"))
                        

                else:
                    self.wynik.setText("Dane są niepoprawne. Sprobuj ponownie.")
                    self.imie_s.setText("")
                    self.nazwisko_s.setText("")
                    self.pesel_s.setText("")
                    self.idk_s.setText("")
                connect.commit()
            
        elif wartosc == "&Czysc":
            self.imie_s.setText("")
            self.nazwisko_s.setText("")
            self.pesel_s.setText("")
            self.idk_s.setText("")
            self.wynik.setText("Wyczyszczone")
        else:
            pass
            
        
        #self.wynik.setText(wartosc)
            
if __name__ == '__main__':

    app = QApplication(sys.argv)
    okno = Okno()
    sys.exit(app.exec_())
