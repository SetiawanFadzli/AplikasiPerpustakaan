import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import pymysql

class Anggota(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('form_anggota.ui',self)
        self.setWindowTitle('Lombok Perpustakaan')
        self.setWindowIcon(QIcon('ICONS/library_logo.png'))
        self.tampilDataAnggota()
        self.btnSimpan.clicked.connect(self.simpanDataAnggota)
        self.tblAnggota.clicked.connect(self.tampilDataAnggotaTerpilih)
        self.btnUbah.clicked.connect(self.ubahDataAnggota)
        self.btnHapus.clicked.connect(self.hapusDataAnggota)
        self.btnCari.clicked.connect(self.cariDataAnggota)

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

    def tampilDataAnggota(self):
        try:
            con=pymysql.connect(host='localhost',user='root',password='',database='lombokperpustakaan_db')
            query="select * from tbl_anggota"
            cursor=con.cursor()
            cursor.execute(query)
            data=cursor.fetchall()
            con.close()
            n_data=len(data)
            self.tblAnggota.setRowCount(n_data)
            baris=0

            for x in data:
                self.tblAnggota.setItem(baris,0,QTableWidgetItem(x[0]))
                self.tblAnggota.setItem(baris,1,QTableWidgetItem(x[1]))
                self.tblAnggota.setItem(baris,2,QTableWidgetItem(x[2]))
                self.tblAnggota.setItem(baris,3,QTableWidgetItem(x[3]))
                self.tblAnggota.setItem(baris,4,QTableWidgetItem(x[4]))
                self.tblAnggota.setItem(baris,5,QTableWidgetItem(x[5]))
                self.tblAnggota.setItem(baris,6,QTableWidgetItem(x[6]))
                self.tblAnggota.setItem(baris,7,QTableWidgetItem(x[7]))

                baris=baris+1
        except:
            self.tampilPesan('Terjadi kesalahan pada saat menampilkan data anggota')

    def simpanDataAnggota(self):
        try:
            id_anggota=self.editID.displayText()
            nama_depan=self.editNamaDepan.displayText()
            nama_tengah=self.editNamaTengah.displayText()
            nama_belakang=self.editNamaBelakang.displayText()
            jenis_kelamin=self.cmbJenisKelamin.currentText()
            tlp=self.editTlp.displayText()
            alamat=self.editAlamat.displayText()
            email=self.editEmail.displayText()

            if id_anggota!="" and nama_depan!="" and jenis_kelamin !="" and tlp !="" and alamat !="" and email !="":
                con=pymysql.connect(host='localhost',user='root',password='',database='lombokperpustakaan_db')
                query="INSERT INTO tbl_anggota(id_anggota,nama_depan,nama_tengah,nama_belakang,jenis_kelamin,tlp,alamat,email) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                data=(id_anggota,nama_depan,nama_tengah,nama_belakang,jenis_kelamin,tlp,alamat,email)
                cursor=con.cursor()
                cursor.execute(query,data)
                con.commit()
                con.close()
                self.tampilPesan('Data telah tersimpan')
                self.tampilDataAnggota()
            else:
                self.tampilPesan('Data tidak lengkap, silahkan lengkap data terlebih dahulu')
        except:
            self.tampilPesan('Terjadi kesalahan pada saat menyimpan data anggota')

    def tampilDataAnggotaTerpilih(self):
        items=self.tblAnggota.selectedItems()
        id_anggota=items[0].text()
        nama_depan=items[1].text()
        nama_tengah=items[2].text()
        nama_belakang=items[3].text()
        jenis_kelamin=items[4].text()
        tlp=items[5].text()
        alamat=items[6].text()
        email=items[7].text()

        self.editID.setText(id_anggota)
        self.editNamaDepan.setText(nama_depan)
        self.editNamaTengah.setText(nama_tengah)
        self.editNamaBelakang.setText(nama_belakang)
        self.editTlp.setText(tlp)
        self.editAlamat.setText(alamat)
        self.editEmail.setText(email)

        if jenis_kelamin=="Laki-Laki":
            self.cmbJenisKelamin.setCurrentIndex(1)
        elif jenis_kelamin=="Perempuan":
            self.cmbJenisKelamin.setCurrentIndex(2)
        else:
            self.cmbJenisKelamin.setCurrentIndex(0)

    def ubahDataAnggota(self):
        try:
            id_anggota=self.editID.displayText()
            nama_depan=self.editNamaDepan.displayText()
            nama_tengah=self.editNamaTengah.displayText()
            nama_belakang=self.editNamaBelakang.displayText()
            jenisKelamin=self.cmbJenisKelamin.currentText()
            tlp=self.editTlp.displayText()
            alamat=self.editAlamat.displayText()
            email=self.editEmail.displayText()

            if id_anggota!="" and nama_depan !="" and jenisKelamin !="":
##                pass
                con=pymysql.connect(host="localhost",user="root",password="",database="lombokperpustakaan_db")
##                con=pymysql.connect(host='localhost',user='root',password='',database='lombokperpustakaan_db')
                query="UPDATE tbl_anggota SET nama_depan=%s,nama_tengah=%s,nama_belakang=%s,jenis_kelamin=%s,tlp=%s,alamat=%s,email=%s WHERE id_anggota=%s"
                data=(nama_depan,nama_tengah,nama_belakang,jenisKelamin,tlp,alamat,email,id_anggota)
                cursor=con.cursor()
                cursor.execute(query,data)
                con.commit()
                con.close()
                self.tampilPesan("Pembaruan Data Anggota Berhasil")
                self.tampilDataAnggota()
            else:
                self.tampilPesan("Data Anggota tidak lengkap, silahkan lengkapi data terlebih dahulu")
        except:
            self.tampilPesan('Terjadi kesalahan pada saat ubah data')

    def hapusDataAnggota(self):
        try:
            id_anggota=self.editID.displayText()
            if id_anggota!="":
                msgbox=self.tampilJendelaKonfirmasi("Apakah anda yakin ingin menghapus data ini?")

                if msgbox==QMessageBox.Ok:
                    con=pymysql.connect(host="localhost",user="root",password="",database="lombokperpustakaan_db")
                    query="DELETE FROM tbl_anggota WHERE id_anggota=%s"
                    data=(id_anggota,)
                    cursor=con.cursor()
                    cursor.execute(query,data)
                    con.commit()
                    con.close()
                    self.tampilPesan("Data telah terhapus")
                    self.tampilDataAnggota()
            else:
                self.tampilPesan("Data Kosong, Silahkan pilih data anggota yang ingin di hapus")
        except:
            self.tampilPesan("Terjadi Kesalahan Pada Saat Hapus Data")

    def cariDataAnggota(self):
        try:
            kata_kunci=self.editCari.displayText()
            con=pymysql.connect(host="localhost",user="root",password="",database="lombokperpustakaan_db")
            query="SELECT * FROM tbl_anggota WHERE id_anggota LIKE '%" + kata_kunci + "%' OR nama_depan LIKE '%" + kata_kunci + "%'"
            cursor=con.cursor()
            cursor.execute(query)
            data=cursor.fetchall()
            con.close()
            n_data=len(data)
            self.tblAnggota.setRowCount(n_data)
            baris=0

            for x in data:
                self.tblAnggota.setItem(baris,0,QTableWidgetItem(x[0]))
                self.tblAnggota.setItem(baris,1,QTableWidgetItem(x[1]))
                self.tblAnggota.setItem(baris,2,QTableWidgetItem(x[2]))
                self.tblAnggota.setItem(baris,3,QTableWidgetItem(x[3]))
                self.tblAnggota.setItem(baris,4,QTableWidgetItem(x[4]))
                self.tblAnggota.setItem(baris,5,QTableWidgetItem(x[5]))
                self.tblAnggota.setItem(baris,6,QTableWidgetItem(x[6]))
                self.tblAnggota.setItem(baris,7,QTableWidgetItem(x[7]))

                baris=baris+1
        except:
            self.tampilPesan("Terjadi kesalahan pada pencarian data")
        
##if __name__=="__main__":
##    app=QApplication(sys.argv)
##    form=Anggota()
##    form.show()
##    sys.exit(app.exec_())
