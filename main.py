import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sqlite3 as sql



#------------- Veritanı işlemleri -----------------------------

baglanti = sql.connect("menuSecim.db")
islem = baglanti.cursor()
baglanti.commit()
table = islem.execute("CREATE TABLE IF NOT EXISTS menu(pizzaTuru TEXT,sos TEXT,urunAciklamasi TEXT,odenecekTutar INT)")
baglanti.commit()

baglantiPayment = sql.connect("payment.db")
islemPayment = baglantiPayment.cursor()
baglantiPayment.commit()
tablePayment = islemPayment.execute("CREATE TABLE IF NOT EXISTS payment(isim TEXT,soyisim TEXT,tc_no INT,cart_no INT,cart_password INT)")
baglantiPayment.commit()

#-------------------------------------------------------------

class Menu(QDialog):
    
    def __init__(self):
        super(Menu, self).__init__()
        loadUi("menu.ui", self)
        self.fiyatSorgula.clicked.connect(self.fiyatSorgulaFunction)
        self.odemeSayfasi.clicked.connect(self.goToPaymentPage)

    def fiyatSorgulaFunction(self):
        self.lastTable.clear()
        self.lastTable.setHorizontalHeaderLabels(("Pizza Türü","Sos","Ürün Açıklaması","Ödenecek Tutar"))
        self.lastTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        pizzaTuru = self.pTuru.currentText()
        sos = self.sTuru.currentText()
        self.fiyat = 0
        global aciklama
        if pizzaTuru == "Sade Pizza - 20 TL":
            if sos == "Soğan - 2 TL":
                fiyat = 22
                aciklama = "Bol Soğanlı Sade Pizza"
            elif sos == "Mısır - 3 TL":
                fiyat = 23
                aciklama = "Bol Mısırlı Sade Pizza"
            elif sos == "Zeytin - 5 TL":
                fiyat = 25
                aciklama = "Bol Zeytinli Sade Pizza"
            elif sos == "Keçi Peyniri - 8 TL":
                fiyat = 28
                aciklama = "Bol Keçi Peynirli Sade Pizza"
            elif sos == "Mantar - 12 TL":
                fiyat = 32
                aciklama = "Bol Mantarlı Sade Pizza"
            elif sos == "Et - 15 TL":
                fiyat = 35
                aciklama =  "Bol Etli Sade Pizza"
        elif pizzaTuru == "Klasik Pizza - 25 TL":
            if sos == "Soğan - 2 TL":
                fiyat = 27
                aciklama = "Bol Soğanlı Klasik Pizza"
            elif sos == "Mısır - 3 TL":
                fiyat = 28
                aciklama = "Bol Mısırlı Klasik Pizza"
            elif sos == "Zeytin - 5 TL":
                fiyat = 30
                aciklama = "Bol Zeytinli Klasik Pizza"
            elif sos == "Keçi Peyniri - 8 TL":
                fiyat = 33
                aciklama = "Bol Keçi Peynirli Klasik Pizza"
            elif sos == "Mantar - 12 TL":
                fiyat = 37
                aciklama = "Bol Mantarlı Klasik Pizza"
            elif sos == "Et - 15 TL":
                fiyat = 40
                aciklama =  "Bol Etli Klasik Pizza"
        elif pizzaTuru == "Margarita Pizza - 30 TL":
            if sos == "Soğan - 2 TL":
                fiyat = 32
                aciklama = "Bol Soğanlı Margarita Pizza"
            elif sos == "Mısır - 3 TL":
                fiyat = 33
                aciklama = "Bol Mısırlı Margarita Pizza"
            elif sos == "Zeytin - 5 TL":
                fiyat = 35
                aciklama = "Bol Zeytinli Margarita Pizza"
            elif sos == "Keçi Peyniri - 8 TL":
                fiyat = 38
                aciklama = "Bol Keçi Peynirli Margarita Pizza"
            elif sos == "Mantar - 12 TL":
                fiyat = 42
                aciklama = "Bol Mantarlı Margarita Pizza"
            elif sos == "Et - 15 TL":
                fiyat = 45
                aciklama =  "Bol Etli Margarita Pizza"
        elif pizzaTuru == "Türk Pizza - 40 TL":
            if sos == "Soğan - 2 TL":
                fiyat = 42
                aciklama = "Bol Soğanlı Türk Pizza"
            elif sos == "Mısır - 3 TL":
                fiyat = 43
                aciklama = "Bol Mısırlı Türk Pizza"
            elif sos == "Zeytin - 5 TL":
                fiyat = 45
                aciklama = "Bol Zeytinli Türk Pizza"
            elif sos == "Keçi Peyniri - 8 TL":
                fiyat = 48
                aciklama = "Bol Keçi Peynirli Türk Pizza"
            elif sos == "Mantar - 12 TL":
                fiyat = 52
                aciklama = "Bol Mantarlı Türk Pizza"
            elif sos == "Et - 15 TL":
                fiyat = 55
                aciklama = "Bol Etli Türk Pizza" 
        try:
            ekle = "insert into menu(pizzaTuru,sos,urunAciklamasi,odenecekTutar) values (?,?,?,?)"
            islem.execute(ekle, (pizzaTuru, sos, aciklama, fiyat))
            baglanti.commit()
            sorgu = "SELECT * FROM menu"
            islem.execute(sorgu)
            for indexSatir,kayitNumamrasi in enumerate(islem):
                for indexSutun,kayitSutun in enumerate(kayitNumamrasi):
                    self.lastTable.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSutun)))
        except Exception as error:
            print("Hata: ", error)
        else:
            pass
    def goToPaymentPage(self):
        paymentpage = PaymentPage()
        widget.addWidget(paymentpage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class PaymentPage(QDialog):
    def __init__(self):
        super(PaymentPage, self).__init__()
        loadUi("payment.ui", self)
        self.ode.clicked.connect(self.paymentPageFunction)
        self.cart_password.setEchoMode(QLineEdit.Password)

    def paymentPageFunction(self):
        isim = self.isim.text()
        soyisim = self.soyisim.text()
        tc_no = self.tc_no.text()
        cart_no = self.cart_no.text()
        cart_password =  self.cart_password.text()
        try:
            ekle = "insert into payment(isim,soyisim,tc_no,cart_no,cart_password) values (?,?,?,?,?)"
            islemPayment.execute(ekle, (isim, soyisim, tc_no, cart_no, cart_password))
            baglantiPayment.commit()
            
        except:
            pass


app = QApplication(sys.argv)
mainwindow = Menu()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(825)
widget.setFixedHeight(375)
widget.show()
app.exec_()