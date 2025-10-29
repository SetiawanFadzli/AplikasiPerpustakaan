import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QEvent
from PyQt5.uic import loadUi
import pymysql

class User(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('form_user.ui',self)
        self.setWindowTitle('Lombok Perpustakaan')
        self.setWindowIcon(QIcon('ICONS/library_logo.png'))
        self.tampilDataUser()
        self.btnSimpan.clicked.connect(self.simpanDataUser)

    def tampilPesan(self, pesan):
        msgbox=QMessageBox()
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setWindowTitle('Lombok Perpustakaan')
        msgbox.setText(pesan)
        msgbox.exec()

    def tampilJendelaKonfirmasi(self, pesan):
        msgbox=QMessageBox()
        msgbox.setIcon(QMessageBox.Question)
        msgbox.setWindowTitle('Lombok Perpustakaan')
        msgbox.setText(pesan)
        msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        return msgbox.exec()

    def hapusText(self):
        self.editID.setText('')
        self.editNamaDepan.setText('')
        self.editNamaTengah.setText('')
        self.editNamaBelakang.setText('')
        self.editUsername.setText('')
        self.editPassword.setText('')
        self.cmbTipeUser.setCurrentIndex(0)

    def tampilDataUser(self):
        try:
            con=pymysql.connect(host='localhost',user='root',password='',database='lombokperpustakaan_db')
            query="select * from tbl_user"
            cursor=con.cursor()
            cursor.execute(query)
            data=cursor.fetchall()
            con.close()
            n_data=len(data)
            self.tblUser.setRowCount(n_data)
            baris=0
            for x in data:
                self.tblUser.setItem(baris,0,QTableWidgetItem(x[0]))
                self.tblUser.setItem(baris,1,QTableWidgetItem(x[1]))
                self.tblUser.setItem(baris,2,QTableWidgetItem(x[2]))
                self.tblUser.setItem(baris,3,QTableWidgetItem(x[3]))
                self.tblUser.setItem(baris,4,QTableWidgetItem(x[4]))
                baris=baris+1
        except:
            self.tampilPesan('Terjadi kesalahan pada saat menampilkan data user')

    def simpanDataUser(self):
        try:
            id_user=self.editID.displayText()
            nama_depan=self.editNamaDepan.displayText()
            nama_tengah=self.editNamaTengah.displayText()
            nama_belakang=self.editNamaBelakang.displayText()
            tipe_user=self.cmbTipeUser.currentText()
            username=self.editUsername.displayText()
            password=self.editPassword.text()

            if id_user!="" and nama_depan!="" and nama_tengah!="" and nama_belakang!="" and tipe_user!="" and username!="" and password!="":
                con=pymysql.connect(host="localhost",user="root",password="",database="lombokperpustakaan_db")
            
                query="INSERT INTO tbl_user (id_user,nama_depan,nama_tengah,nama_belakang,tipe_user,username,password) VALUES (%s, %s, %s, %s, %s, %s, md5(%s))"
                data=(id_user,nama_depan,nama_tengah,nama_belakang,tipe_user,username,password)
                cursor=con.cursor()
                cursor.execute(query,data)
                con.commit()
                con.close()
                self.hapusText()
                self.tampilDataUser()
            else:
                self.tampilPesan('Data user tidak boleh kosong, silahkan lengkapi data terlebih dahulu')
        except:
            self.tampilPesan('Terjadi kesalahan pada saat menyimpan user')
if __name__=="__main__":
    app=QApplication(sys.argv)
    form=User()
    form.show()
    sys.exit(app.exec_())
