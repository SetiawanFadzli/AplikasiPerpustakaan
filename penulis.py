import sys
from PyQt5.QtWidgets import QDialog
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

class Penulis(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        loadUi('form_penulis.ui',self)
        self.setWindowTitle('Lombok Perpustakaan')
        self.setWindowIcon(QIcon('ICONS/library_logo.png'))
        self.tampilDataPenulis()
        self.btnSimpan.clicked.connect(self.simpanDataPenulis)
        self.tblPenulis.clicked.connect(self.tampilDataPenulisTerpilih)
        self.btnUbah.clicked.connect(self.ubahDataPenulis)
        self.btnHapus.clicked.connect(self.hapusDataPenulis)
        self.btnCari.clicked.connect(self.cariDataPenulis)
        

    def tampilPesan(self,pesan):
        msgbox=QMessageBox()
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setWindowTitle('Lombok Perpustakaan')
        msgbox.setText(pesan)
        msgbox.exec()

    def tampilJendelaKonfirmasi(self,pesan):
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

    def tampilDataPenulis(self):
        try:
            con=pymysql.connect(host="localhost",user="root",password="",database="lombokperpustakaan_db")
            query="select * from tbl_penulis"
            cursor=con.cursor()
            cursor.execute(query)
            data=cursor.fetchall()
            con.close()
            n_data=len(data)
            self.tblPenulis.setRowCount(n_data)
            baris=0
            for x in data:
                self.tblPenulis.setItem(baris,0,QTableWidgetItem(x[0]))
                self.tblPenulis.setItem(baris,1,QTableWidgetItem(x[1]))
                self.tblPenulis.setItem(baris,2,QTableWidgetItem(x[2]))
                self.tblPenulis.setItem(baris,3,QTableWidgetItem(x[3]))
                baris=baris+1
        except:
            self.tampilPesan('Terjadi kesalahan pada saat menampilkan data penulis')

    def simpanDataPenulis(self):
        try:
            id_penulis=self.editID.displayText()
            nama_depan=self.editNamaDepan.displayText()
            nama_tengah=self.editNamaTengah.displayText()
            nama_belakang=self.editNamaBelakang.displayText()

            if id_penulis!="" and nama_depan!="":
                con=pymysql.connect(host="localhost",user="root",password="",database="lombokperpustakaan_db")
              

                query="INSERT INTO tbl_penulis (id_penulis,nama_depan,nama_tengah,nama_belakang) VALUES(%s,%s,%s,%s)"
                data=(id_penulis,nama_depan,nama_tengah,nama_belakang)
                cursor=con.cursor()
                cursor.execute(query,data)
                con.commit()
                con.close()
                self.hapusText()
                self.tampilDataPenulis()
            else:
                self.tampilPesan('Data penulis tidak boleh kosong, silahkan lengkapi terlebih dahulu')
        except:
            self.tampilPesan('Terjadi kesalahan pada saat menyimpan user')

    def tampilDataPenulisTerpilih(self):
        try:
            items=self.tblPenulis.selectedItems()
            id_penulis=items[0].text()
            nama_depan=items[1].text()
            nama_tengah=items[2].text()
            nama_belakang=items[3].text()

            self.editID.setText(id_penulis)
            self.editNamaDepan.setText(nama_depan)
            self.editNamaTengah.setText(nama_tengah)
            self.editNamaBelakang.setText(nama_belakang)
        except:
            self.tampilPesan("Terjadi kesalahan pada saat memilih dan menampilkan data")

    def ubahDataPenulis(self):
        try:
            id_penulis=self.editID.displayText()
            nama_depan=self.editNamaDepan.displayText()
            nama_tengah=self.editNamaTengah.displayText()
            nama_belakang=self.editNamaBelakang.displayText()

            if id_penulis!="" and nama_depan!="":
                con=pymysql.connect(host="localhost",user="root",password="",database="lombokperpustakaan_db")
                query="UPDATE tbl_penulis SET nama_depan=%s,nama_tengah=%s,nama_belakang=%s WHERE id_penulis=%s"
                data=(nama_depan,nama_tengah,nama_belakang,id_penulis)
                cursor=con.cursor()
                cursor.execute(query,data)
                con.commit()
                con.close()
                self.tampilPesan("Pembaruan Data User Berhasil")
                self.tampilDataPenulis()
            else:
                self.tampilPesan("Data user tidak lengkap, silahkan lengkapi data terlebih dahulu")
        except:
            self.tampilPesan("Terjadi kesalahan pada saat memperbarui data")

    def hapusDataPenulis(self):
        try:
            id_penulis=self.editID.displayText()

            if id_penulis!="":
                msgbox=self.tampilJendelaKonfirmasi("Apakah anda yakin ingin menghapus data ini?")

                if msgbox==QMessageBox.Ok:
                    con=pymysql.connect(host="localhost",user="root",password="",database="lombokperpustakaan_db")
                    query="DELETE FROM tbl_penulis WHERE id_penulis=%s"
                    data=(id_penulis,)
                    cursor=con.cursor()
                    cursor.execute(query,data)
                    con.commit()
                    con.close()
                    self.tampilPesan("Data Telah Terhapus!")
                    self.tampilDataPenulis()
                    self.hapusText()
            else:
                self.tampilPesan("Data kosong, silahkan pilih data penulis terlebih dahulu")
        except:
            self.tampilPesan("Terjadi Kesalahan pada saat melakukan penghapusan data")

    def cariDataPenulis(self):
        try:
            kata_kunci=self.editCari.displayText()
            con=pymysql.connect(host="localhost",user="root",password="",database="lombokperpustakaan_db")
            query="SELECT * FROM tbl_penulis WHERE id_penulis LIKE '%" + kata_kunci + "%' OR nama_depan LIKE '%" + kata_kunci + "%'"
            cursor=con.cursor()
            cursor.execute(query)
            data=cursor.fetchall()
            con.close()
            n_data=len(data)
            self.tblPenulis.setRowCount(n_data)
            baris=0

            for x in data:
                self.tblPenulis.setItem(baris,0,QTableWidgetItem(x[0]))
                self.tblPenulis.setItem(baris,1,QTableWidgetItem(x[1]))
                self.tblPenulis.setItem(baris,2,QTableWidgetItem(x[2]))
                self.tblPenulis.setItem(baris,3,QTableWidgetItem(x[3]))

                baris=baris+1
        except:
            self.tampilPesan("Terjadi kesalahan pada saat pencarian data")

if __name__=="__main__":
    app=QApplication(sys.argv)
    form=Penulis()
    form.exec()
    sys.exit(app.exec_())
