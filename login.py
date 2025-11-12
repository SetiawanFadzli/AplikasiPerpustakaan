import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import pymysql
import matplotlib.image as mpimg
from form_utama import *

class login(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('form_login.ui',self)

        img=mpimg.imread('ICONS/library_logo.png')
        self.widgetLogo.canvas.axis1.imshow(img)
        self.widgetLogo.canvas.axis1.axis('off')

        self.btnLogin.clicked.connect(self.userLogin)
        self.btnCancel.clicked.connect(self.userCancel)

    def tampilPesan(self, pesan):
        msgbox=QMessageBox()
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setWindowTitle('Applikasi Perpustakaan')
        msgbox.setText(pesan)
        msgbox.exec()

    def hapusText(self):
        self.editUsername.setText('')
        self.editPassword.setText('')

    def userLogin(self):
        try:
            username=self.editUsername.displayText()
            password=self.editPassword.text()

            if username!="" and password!="":
                con=pymysql.connect(host="localhost",user="root",password="",database="lombokperpustakaan_db")

                query="SELECT * FROM tbl_user WHERE username=%s AND password=md5(%s)"
                data=(username,password)
                cursor=con.cursor()
                cursor.execute(query,data)
                data_user=cursor.fetchall()

                if len(data_user)==1:
                    self.hapusText()
                    tipe_user=data_user[0][4]
                    formutama=FormUtama(tipe_user)
                    widget.addWidget(formutama)
                    widget.showMaximized()
                    widget.setWindowTitle('Aplikasi Perpustakaan')
                    widget.setWindowIcon(QIcon('ICONS/library_logo.png'))
                    widget.setCurrentIndex(widget.currentIndex()+1)
                else:
                    self.tampilPesan('Login gagal')
            else:
                self.tampilPesan('password dan username tidak boleh kosong')
        except:
            self.tampilPesan('terjadi kesalahan pada saat login')

    def userCancel(self):
        self.close()

if __name__=="__main__":
    app=QApplication(sys.argv)
    form=login()
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(form)
    widget.setMinimumWidth(451)
    widget.setMaximumHeight(216)
    widget.setWindowTitle('Aplikasi Perpustakaan')
    widget.setWindowIcon(QIcon('ICONS/library_logo.png'))
    widget.show()
    sys.exit(app_exec())
