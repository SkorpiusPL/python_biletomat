import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QComboBox, QGridLayout, QApplication, QPushButton, QAction, QFileDialog,  QMainWindow, QInputDialog, QFormLayout)
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
        self.skad_s = QLineEdit()
        self.dokad_s= QLineEdit()
        self.kierunek_s = QLineEdit()
        self.wynik = QLineEdit()
        self.wynik.setDisabled(True)
        self.bilet = QComboBox(self)
        for i,v in (('wybierz', ''),('zwykły','zwykły'), ('ulgowy','ulgowy')):
            self.bilet.addItem(i,v)
            
        self.minuty = QComboBox(self)
        for i,v in (('wybierz',""),('20 minut',"20"), ('45 minut',"45"), ('75 minut',"75")):
            self.minuty.addItem(i,v)
        
        self.wynik.setToolTip('Tu będzie wynik tekstu')
        self.dodajBtn = QPushButton("&Dodaj")
        self.czysc = QPushButton("&Czysc")
        
        self.interfejs()

    def interfejs(self):
        tytul = QLabel("DODAJ BILET", self)
        imie = QLabel("Podaj imię: ", self)
        nazwisko = QLabel("Podaj nazwisko: ", self)
        pesel = QLabel("Podaj numer pesel: ", self)
        rodzaj_biletu = QLabel("Rodzaj biletu: ", self)
        ile_minut =  QLabel("Ilu minutowy: ", self)
        skad = QLabel("Przystanek początkowy: ", self) 
        dokad = QLabel("Przystanek końcowy: ", self)
        kierunek = QLabel("Kierunek jazdy: ", self)
        
        ukladT = QGridLayout()
        ukladT.setSpacing(10)
        ukladT.addWidget(tytul, 0, 1)
        ukladT.addWidget(imie, 1, 0)
        ukladT.addWidget(nazwisko, 1,1)
        ukladT.addWidget(pesel, 1,2)
        
        ukladT.addWidget(skad, 3,0)
        ukladT.addWidget(dokad, 3,1)
        ukladT.addWidget(kierunek, 3,2)
        
        ukladT.addWidget(rodzaj_biletu, 5,0)
        ukladT.addWidget(self.bilet, 6,0)
        ukladT.addWidget(ile_minut, 5,1)
        ukladT.addWidget(self.minuty, 6,1)
        ukladT.addWidget(self.imie_s, 2, 0)
        ukladT.addWidget(self.nazwisko_s, 2, 1)
        ukladT.addWidget(self.pesel_s, 2, 2)
        ukladT.addWidget(self.skad_s, 4, 1)
        ukladT.addWidget(self.dokad_s, 4, 2)
        ukladT.addWidget(self.kierunek_s, 4, 0)
        ukladT.addWidget(self.wynik, 10, 0,3,0)
        ukladT.addWidget(self.dodajBtn, 8, 0, 3, 0)
        ukladT.addWidget(self.czysc, 6, 2)

        # przypisanie utworzonego układu do okna
        self.dodajBtn.clicked.connect(self.dzialanie)
        self.czysc.clicked.connect(self.dzialanie)
        
        self.setLayout(ukladT)
        self.setGeometry(150, 100, 330, 300)
        self.setWindowTitle("Automatyczny biletomat- sprzedaż biletu")
        self.show()
        

    def dzialanie(self):
        dzialania = self.sender()
        wartosc = str(dzialania.text())
        im = str(self.imie_s.text())
        in_= str(self.nazwisko_s.text())
        ipes = self.pesel_s.text()
        kier = str(self.kierunek_s.text())
        pp = str(self.skad_s.text())
        pk = str(self.dokad_s.text())
        bil = str(self.bilet.currentData())
        minut = int(self.minuty.currentData())
        
        if wartosc == "&Dodaj":
            
            if im == "":
                self.wynik.setText("Brak danych. Wpisz dane")
            elif in_ == "":
                self.wynik.setText("Brak danych. Wpisz dane")
            elif ipes == "":
                self.wynik.setText("Brak danych. Wpisz dane")
            elif bool(re.match(r'[0-9]{11}$', ipes)) == False:
                self.wynik.setText("Zły fomat numeru Pesel")
            elif kier == "":
                self.wynik.setText("Brak danych. Wpisz dane")
            elif pp == "":
                self.wynik.setText("Brak danych. Wpisz dane")
            elif pk == "":
                self.wynik.setText("Brak danych. Wpisz dane")
            elif str(self.bilet.currentIndex()) == "0":
                self.wynik.setText("Nie wybrałes rodzaju biletu")
            elif str(self.minuty.currentIndex()) == "0":
                self.wynik.setText("Nie wybrałes ilosci minut")
            else:
                obecnie = datetime.datetime.now()
                od = str(obecnie)
                dm = obecnie + datetime.timedelta(minutes=minut)
                wygasanie = str(dm.timestamp())
                dodajminut = str(dm)
                
                data_dodania = od[:10]
                godzina_dodania = od[11:]
                godzina_wygasania = dodajminut[11:]
                
                identyfikator = hashlib.new('sha1')
                identyfikator.update(str(im + in_ + ipes + od).encode('utf-8'))
                identyfikator = identyfikator.hexdigest()
                identyfikator = identyfikator[:10]
                id_klient = hashlib.new('sha1')
                id_klient.update(str(im + in_ + ipes).encode('utf-8'))
                id_klient = id_klient.hexdigest()
                id_klient = id_klient[:5]
                
                #self.wynik.setText(im+" "+in_+" "+ipes+" ->"+kier+" "+pp+" "+pk+" "+bil+" | "+data_dodania+"|"+godzina_dodania+"|"+godzina_wygasania+"|"+wygasanie+" | "+identyfikator+" | "+id_klient)
                
                cursor.execute("INSERT INTO bilety VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?,?)",(im, in_, ipes, bil, data_dodania, pp, pk, kier, godzina_dodania, godzina_wygasania, wygasanie, identyfikator, id_klient))
                self.wynik.setText("Zachowaj identyfikator biletu: "+identyfikator)
                connect.commit()
                cursor.execute("SELECT * FROM klienci WHERE nazwisko=? AND pesel=?",(in_,ipes))
                klienci = cursor.fetchall()
                ilosc = len(klienci)
                
                if ilosc == 1:
                    pass
                else:
                    cursor.execute("INSERT INTO klienci VALUES(NULL,?,?,?,?)",(im, in_, ipes, id_klient))
                    self.imie_s.setText("")
                    self.nazwisko_s.setText("")
                    self.pesel_s.setText("")
                    self.skad_s.setText("")
                    self.dokad_s.setText("")
                    self.kierunek_s.setText("")
                    self.bilet.setCurrentIndex(0)
                    self.minuty.setCurrentIndex(0)
                    self.wynik.setText("Bilet został kupiony. Identyfikator biletu:"+identyfikator+" | Klient został oznaczony numerem:"+id_klient)
                connect.commit()
            
        elif wartosc == "&Czysc":
            self.imie_s.setText("")
            self.nazwisko_s.setText("")
            self.pesel_s.setText("")
            self.skad_s.setText("")
            self.dokad_s.setText("")
            self.kierunek_s.setText("")
            self.bilet.setCurrentIndex(0)
            self.minuty.setCurrentIndex(0)
            self.wynik.setText("Wyczyszczone")
        else:
            pass
            
        
        #self.wynik.setText(wartosc)
            
if __name__ == '__main__':

    app = QApplication(sys.argv)
    okno = Okno()
    sys.exit(app.exec_())
