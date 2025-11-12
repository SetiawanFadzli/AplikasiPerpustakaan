import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMdiArea
from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMdiSubWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi
from User import *

class FormUtama(QMainWindow):
    def __init__(self, tipe_user):
        QMainWindow.__init__(self)
        loadUi('form_utama.ui',self)

        #membuat area MDI
        self.mdi=QMdiArea()
        self.setCentralWidget(self.mdi)

        #membuat menubar
        self.menubar=QMenuBar()
        administrator=self.menubar.addMenu('Administrator')
        data=self.menubar.addMenu('Data')
        transaksi=self.menubar.addMenu('Transaksi')
        statistik=self.menubar.addMenu('Statistik')
        user=self.menubar.addMenu('User')

        #membuat sub menu
        data_pengguna=QAction(QIcon('ICONS/account.png'),'Data Pengguna', self)
        administrator.addAction(data_pengguna)

        data_anggota=QAction(QIcon('ICONS/member.png'),'Data Anggota',self)
        data_buku=QAction(QIcon('ICONS/book.png'),'Data Buku',self)
        data.addAction(data_anggota)
        data.addAction(data_buku)

        transaksi_peminjaman=QAction(QIcon('ICONS/loan_transaction.png'),'Transaksi Peminjaman',self)
        transaksi.addAction(transaksi_peminjaman)

        statistik_anggota=QAction(QIcon('ICONS/member_stat.png'),'Statistik Anggota',self)
        statistik_buku=QAction(QIcon('ICONS/book_stat.png'),'Statistik Buku',self)
        statistik_peminjaman=QAction(QIcon('ICONS/loan_stat.png'),'Statistik Peminjaman',self)
        statistik.addAction(statistik_anggota)
        statistik.addAction(statistik_buku)
        statistik.addAction(statistik_peminjaman)

        logout=QAction(QIcon('ICONS/logout.png'),'Logout',self)
        exitapp=QAction(QIcon('ICONS/exit.png'),'Exit',self)
        user.addAction(logout)
        user.addAction(exitapp)

        self.setMenuBar(self.menubar)
        
        logout.triggered.connect(self.logoutuser)
        exitapp.triggered.connect(self.exitApp)
        data_pengguna.triggered.connect(self.tampilFormDataUser)
        
        if tipe_user=="User":
            data_pengguna.setEnabled(False)
            data_buku.setEnabled(False)
            data_anggota.setEnabled(False)

    #fungsi menampilkan ktak pesan
    def tampilDialogKonfirmasi(self,pesan):
        msgbox=QMessageBox()
        msgbox.setWindowTitle('Applikasi Perpustakaan')
        msgbox.setIcon(QMessageBox.Question)
        msgbox.setText(pesan)
        msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        return msgbox.exec()

    #fungsi logout
    def logoutuser(self):
        dialog_konfirmasi=self.tampilDialogKonfirmasi('Apakah anda yakin untuk logout?')
        if dialog_konfirmasi==QMessageBox.Ok:
            widget=self.parentWidget()
            widget.setCurrentIndex(widget.currentIndex()-1)
            widget.showNormal()

    #fungsi keluar dari aplikasi
    def exitApp(self):
        dialog_konfirmasi=self.tampilDialogKonfirmasi('Apakah anda yakin untuk keluar')
        if dialog_konfirmasi==QMessageBox.Ok:
            self.parentWidget().close()

    def tampilFormDataUser(self):
        form_data_user=User()
        sub_form=QMdiSubWindow()
        sub_form.setWidget(form_data_user)
        sub_form.setFixedSize(881,464)
        self.mdi.addSubWindow(sub_form)
        sub_form.show()
        
if __name__=="__main__":
    app=QApplication(sys.argv)
    form=FormUtama("Administrator")
    form.show()
    sys.exit(app.exec_())
