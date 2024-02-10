from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import MySQLdb
from PyQt5.uic import loadUiType
import datetime

ui,_ = loadUiType('library.ui')

# WORK IN PROGRESS
# login,_ = loadUiType('login.ui')



# TODO
# 1. Fix UI (50%)
# 2. Add basic functionality (40%)
# 3. Add entry to rent book (Done)

# WORK IN PROGRESS
# class Login(QWidget , login):
#     def __init__(self):
#         QWidget.__init__(self)
#         self.setupUi(self)
#         self.pushButton.clicked.connect(self.Handel_Login)
#         style = open('themes/darkorange.css' , 'r')
#         style = style.read()
#         self.setStyleSheet(style)

    # WORK IN PROGRESS SOON
    # def Handel_Login(self):
    #     self.db = MySQLdb.connect(host='localhost' , user='root' , password ='' , db='library')
    #     self.cur = self.db.cursor()

    #     username = self.lineEdit.text()
    #     password = self.lineEdit_2.text()

    #     sql = ''' SELECT * FROM users'''

    #     self.cur.execute(sql)
    #     data = self.cur.fetchall()
    #     for row in data  :
    #         if username == row[1] and password == row[3]:
    #             self.windowMain = MainApp()
    #             self.close()
    #             self.windowMain.show()

    #         else:
    #             self.label.setText('Tolong masukkan kata sandi yang benar!')




class MainApp(QMainWindow , ui):
    def __init__(self):
        # INISIALISASI APLIKASI PADA WINDOW UTAMA
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Function_Btns()
        self.Dark_Blue_Theme()
        self.Show_All_Members()
        self.Show_All_Books()
        self.Show_Rent_Data()

        # Hide tab nav, and only show from button nav
        # MENGHIDE TAMPILAN PADA WIDGET TAB DAN MENGGANTINYA DENGAN BUTTON
        self.tabWidget.setTabVisible(0, False)
        self.tabWidget.setTabVisible(1, False)
        self.tabWidget.setTabVisible(2, False)
        self.tabWidget.setTabVisible(3, False)
        self.tabWidget.setTabVisible(4, False)

    # MENGAITKAN WIDGET BUTTON DENGAN FUNGSI-FUNGSI YANG SUDAH DIBUAT
    def Handle_Function_Btns(self):
        self.pushButton.clicked.connect(self.Menu_Rent)
        self.pushButton_2.clicked.connect(self.Menu_List_Books)
        self.pushButton_26.clicked.connect(self.Menu_List_Members)
        self.pushButton_7.clicked.connect(self.Add_New_Book)
        self.pushButton_22.clicked.connect(self.Add_New_Member)
        self.pushButton_6.clicked.connect(self.Add_Entry_Rents)

    ########################################
    ######### Main Navigation Menu #################
    def Menu_Rent(self):
        self.tabWidget.setCurrentIndex(0)

    def Menu_List_Books(self):
        self.tabWidget.setCurrentIndex(1)

    def Menu_List_Members(self):
        self.tabWidget.setCurrentIndex(2)

    ########################################
    ######### Rent Book Functionality #################
    def Add_Entry_Rents(self):
        book_Code = self.lineEdit.text()
        member_Code = self.lineEdit_29.text()
        status = self.comboBox.currentText()
        days_Rent = self.comboBox_2.currentIndex() + 1
        todayDate = datetime.date.today()
        toDate = todayDate + datetime.timedelta(days=days_Rent)
        
        print(todayDate)
        print(toDate)

        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            INSERT INTO data_peminjaman (kode_buku, kode_anggota, status , rentang_hari, mulai_pinjam, selesai_pinjam)
            VALUES (%s , %s , %s, %s , %s , %s)
        ''' , (book_Code ,member_Code, status , days_Rent , todayDate  , toDate))

        self.db.commit()
        self.statusBar().showMessage('Data peminjaman baru telah ditambahnkan!')

        self.Show_Rent_Data()

    def Show_Rent_Data(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' 
            SELECT kode_buku, kode_anggota, status, rentang_hari, mulai_pinjam, selesai_pinjam FROM data_peminjaman
        ''')

        dataPeminjaman = self.cur.fetchall()

        self.cur.execute(f'SELECT nama_buku FROM data_buku WHERE id_buku = "{dataPeminjaman[0][0]}"')
        dataBuku = self.cur.fetchall()

        self.cur.execute(f'SELECT nama_anggota FROM anggota WHERE id = "{dataPeminjaman[0][1]}"')
        dataAnggota = self.cur.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row , form in enumerate(dataPeminjaman):
            self.cur.execute(f'SELECT nama_buku FROM data_buku WHERE id_buku = "{dataPeminjaman[row][0]}"')
            dataBuku = self.cur.fetchall()

            self.cur.execute(f'SELECT nama_anggota FROM anggota WHERE id = "{dataPeminjaman[row][1]}"')
            dataAnggota = self.cur.fetchall()

            for column , item in enumerate(form):
                self.tableWidget.setItem(row , column , QTableWidgetItem(str(item)))

                # change to book name from id
                if (column == 0):
                    self.tableWidget.setItem(row , column , QTableWidgetItem(dataBuku[0][0]))
                    
                # change to member name from id
                if (column == 1):
                    self.tableWidget.setItem(row , column , QTableWidgetItem(dataAnggota[0][0]))
                column += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)



    # Books Functionality
    def Show_All_Books(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT * FROM data_buku''')
        data = self.cur.fetchall()

        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_5.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_5.rowCount()
            self.tableWidget_5.insertRow(row_position)

        self.db.close()


    def Add_New_Book(self):

        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='' , db='library')
        self.cur = self.db.cursor()

        book_Code = self.lineEdit_3.text()
        bookTitle = self.lineEdit_2.text()
        bookCategory = self.comboBox_3.currentText().lower()
        bookAuthor = self.lineEdit_30.text()
        bookPublisher = self.lineEdit_31.text()

        self.cur.execute('''
            INSERT INTO data_buku (id_buku, nama_buku, kategori, penulis, penerbit)
            VALUES (%s , %s , %s , %s , %s)
        ''' ,(book_Code  , bookTitle , bookCategory , bookAuthor, bookPublisher))

        self.db.commit()
        self.statusBar().showMessage('Buku baru ditambahkan!')

        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.comboBox_3.setCurrentIndex(0)
        self.lineEdit_30.setText('')
        self.lineEdit_31.setText('')
        self.Show_All_Books()

    ########################################
    ######### Members Library #################
    def Show_All_Members(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT * FROM anggota ''')
        data = self.cur.fetchall()

        # print(data)
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_6.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_6.rowCount()
            self.tableWidget_6.insertRow(row_position)

        self.db.close()


    def Add_New_Member(self):
        memberId = self.lineEdit_22.text()
        self.lineEdit_22.setText("")


        memberName = self.lineEdit_23.text()
        memberNIK = self.lineEdit_24.text()

        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            INSERT INTO anggota (id, nama_anggota, NIK)
            VALUES (%s , %s , %s)
        ''' , (memberId , memberName , memberNIK))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('Anggota baru telah ditambahkan!')
        self.Show_All_Members()
        
    # def Login(self):
    #     self.db = MySQLdb.connect(host='localhost' , user='root' , password='' , db='library')
    #     self.cur = self.db.cursor()
        
    #     username = self.lineEdit_14.text()
    #     password = self.lineEdit_13.text()
        
    #     sql = '''SELECT * FROM users'''
        
    #     self.cur.execute(sql)
    #     data = self.cur.fetchall()
    #     for row in data :
    #         if username == row[1] and password == row[3] :
    #             print('user match')
    #             self.statusBar().showMessage('Valid Username & Password')
    #             self.groupbox_4.setEnabled(True)
                
    #             self.lineEdit_17.settext(row[1])
    #             self.lineEdit_15.settext(row[2])
    #             self.lineEdit_16.settext(row[3])

   ########################################
    #########  UI Themes #################
    def Dark_Blue_Theme(self):
        style = open('themes/darkblue.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()



if __name__ == '__main__':
    main()