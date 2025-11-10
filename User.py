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
        self.tblUser.clicked.connect(self.tampilDataUserTerpilih)
        self.btnUbah.clicked.connect(self.ubahDataUser)
        self.btnHapus.clicked.connect(self.hapusDataUser)
        self.tblUser.viewport().installEventFilter(self)

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
                self.tblUser.setItem(baris,5,QTableWidgetItem(x[5]))
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

    def tampilDataUserTerpilih(self):
        try:
            items=self.tblUser.selectedItems()
            id_user=items[0].text()
            nama_depan=items[1].text()
            nama_tengah=items[2].text()
            nama_belakang=items[3].text()
            tipe_user=items[4].text()
            username=items[5].text()

            self.editID.setText(id_user)
            self.editNamaDepan.setText(nama_depan)
            self.editNamaTengah.setText(nama_tengah)
            self.editNamaBelakang.setText(nama_belakang)
            self.editUsername.setText(username)
            if tipe_user=="Administrator":
                self.cmbTipeUser.setCurrentIndex(1)
            elif tipe_user=="User":
                self.cmbTipeUser.setCurrentIndex(2)
            else:
                self.cmbTipeUser.setCurrentIndex(0)
        except:
            self.tampilPesan("Terjadi kesalahan pada saat memilih dan menampilkan data user!")
        
    def ubahDataUser(self):
        try:
            id_user=self.editID.displayText()
            nama_depan=self.editNamaDepan.displayText()
            nama_tengah=self.editNamaTengah.displayText()
            nama_belakang=self.editNamaBelakang.displayText()
            tipe_user=self.cmbTipeUser.currentText()
            username=self.editUsername.displayText()

            if id_user!="" and nama_depan!="" and tipe_user!="" and username!="":
                con=pymysql.connect(host="localhost",user="root",password="",database="lombokperpustakaan_db")
                query="UPDATE tbl_user SET nama_depan=%s,nama_tengah=%s,nama_belakang=%s,tipe_user=%s,username=%s WHERE id_user=%s"
                data=(nama_depan,nama_tengah,nama_belakang,tipe_user,username,id_user)
                cursor=con.cursor()
                cursor.execute(query,data)
                con.commit()
                con.close()
                self.tampilPesan("Pembaruan Data User Berhasil")
                self.tampilDataUser()
            else:
                self.tampilPesan("Data user tidak lengkap, silahkan lengkapi data terlebih dahulu")
        except:
            self.tampilPesan("Terjadi kesalahan pada saat memperbarui data")
    def hapusDataUser(self):
        try:
            id_user=self.editID.displayText()
            if id_user!="":
                msgbox=self.tampilJendelaKonfirmasi("Apakah anda yakin ingin menghapus data ini?")
                if msgbox==QMessageBox.Ok:
                    con=pymysql.connect(host="localhost",user="root",password="",database="lombokperpustakaan_db")
                    query="DELETE FROM tbl_user WHERE id_user=%s"
                    data=(id_user,)
                    cursor=con.cursor()
                    cursor.execute(query,data)
                    con.commit()
                    con.close()
                    self.tampilPesan("Data telah terhapus!")
                    self.tampilDataUser()
                    self.hapusText()
            else:
                self.tampilPesan('Data kosong, silahkan pilih data user yang ingin dihapus terlebih dahulu')
        except:
            self.tampilPesan('Terjadi kesalahan pada saat melakukan penghapusan data user')
    def ubahPasswordUser(self,id_user,passwordBaru):
        try:
            if id_user!="" and passwordBaru!="":
                con=pymysql.connect(host="localhost",user="root",password="",database="lombokperpustakaan_db")
                query="UPDATE tbl_user SET password=md5(%s) WHERE id_user=%s"
                data=(passwordBaru,id_user)
                cursor=con.cursor()
                cursor.execute(query,data)
                con.commit()
                con.close()
                self.tampilPesan("Password telah diubah!")
            else:
                self.tampilPesan("Silahkan pilih user yang ingin diubah password terlebih dahulu!")
        except:
            self.tampilPesan("Terjadi kesalahan pada saat mengubah password!")
    def eventFilter(self,source,event):
        try:
            if event.type()==QEvent.ContextMenu and source is self.tblUser.viewport():
                menu=QMenu()
                menu.addAction(QIcon('ICONS/change_password.png'),'Ubah Password')

                if menu.exec_(event.globalPos()):
                    items=self.tblUser.selectedItems()
                    id_user=items[0].text()
                    passwordBaru,ok=QInputDialog.getText(self,'Lombok Perpustakaan','Password Baru', QLineEdit.Password, '')

                    if ok:
                        self.ubahPasswordUser(id_user,passwordBaru)
            return super().eventFilter(source,event)
        except:
            self.tampilPesan('Terjadi kesalahan pada saat membuat kontak menu')
if __name__=="__main__":
    app=QApplication(sys.argv)
    form=User()
    form.show()
    sys.exit(app.exec_())
