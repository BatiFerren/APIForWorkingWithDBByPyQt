import csv
import sqlite3
import datetime
from mydesign import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
import sys
from PyQt5.QtWidgets import QTableWidgetItem


def connect_db(name_db):
    connect = sqlite3.connect(name_db)
    return connect


"""def create_table(name_table, connect):
    cur = connect.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS ''' + name_table + ''' (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Device_type text, Operator text, Time text, Success int)'''
    cur.execute(sql)
    connect.commit


def read_csv_and_write_to_db(file_obj, con):
    with open(file_obj, newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        if header != None:
            for row in reader:
                cur = con.cursor()
                cur.execute("INSERT INTO tests_results (Device_type, Operator, Time, Success) VALUES(?, ?, ?, ?);", row)
                con.commit()"""


def show_all_tests():
    main_connect = connect_db('tests.db')
    main_cursor = main_connect.cursor()
    all_select_sql = '''SELECT * FROM tests_results'''
    show_all_list = main_cursor.execute(all_select_sql).fetchall()
    main_cursor.close()
    main_connect.close()
    return show_all_list


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_3.clicked.connect(self.btnClickedShowAll)
        self.ui.pushButton.clicked.connect(self.btnClickedAdd)
        self.ui.pushButton_2.clicked.connect(self.btnClickedRemoveTest)
        self.ui.pushButton_4.clicked.connect(self.btnClickedShowStatistics)


    def btnClickedShowStatistics(self):
        operator = self.ui.lineEdit_2.text()
        if operator == '':
            error = "Enter the name of operator"
        else:
            main_connect = connect_db('tests.db')
            main_cursor = main_connect.cursor()
            all_select_sql = '''SELECT Device_type, COUNT(*) as All_tests FROM tests_results WHERE Operator = \'''' + operator + '''\' GROUP BY Device_type'''
            success_select_sql = '''SELECT Device_type, COUNT(*) as Success_tests FROM tests_results WHERE Operator = \'''' + operator + '''\' AND Success = 1 GROUP BY Device_type'''
            unsuccess_select_sql = '''SELECT Device_type, COUNT(*) as Unsuccess_tests FROM tests_results WHERE Operator = \'''' + operator + '''\' AND Success = 0 GROUP BY Device_type'''
            statistics_list = main_cursor.execute(all_select_sql).fetchall()

            dev_type_list = []
            all_tests_list = []
            success_tests_list = []
            unsuccess_tests_list = []
            for item in statistics_list:
                dev_type_list.append(item[0])
                all_tests_list.append(item[1])
            success_list = main_cursor.execute(success_select_sql).fetchall()
            for item in success_list:
                success_tests_list.append(item[1])
            unsuccess_list = main_cursor.execute(unsuccess_select_sql).fetchall()
            for item in unsuccess_list:
                unsuccess_tests_list.append(item[1])
            result_list = []
            for i in range(0, len(statistics_list) - 1):
                result_list.append(
                    (dev_type_list[i], all_tests_list[i], success_tests_list[i], unsuccess_tests_list[i]))
            main_cursor.close()
            main_connect.close()
            self.ui.label_6.setText(operator)

            row = 0
            for line in result_list:
                col = 0
                for cell_data in line:
                    col += 1
                row += 1
            self.ui.tableWidget.setRowCount(row)
            self.ui.tableWidget.setColumnCount(col)
            header_list = ['Device type', 'All tests', 'Success tests', 'Unsuccess tests']
            self.ui.tableWidget.setHorizontalHeaderLabels(header_list)

            row = 0
            for line in result_list:
                col = 0
                for cell_data in line:
                    cellinfo = QTableWidgetItem(str(cell_data))
                    cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.ui.tableWidget.setItem(row, col, cellinfo)
                    col += 1
                row += 1

        self.ui.lineEdit_2.setText('')
        """if error:
            self.ui.label_7.setText(error)
            self.ui.label_7.setStyleSheet('color: red')"""

    def btnClickedRemoveTest(self):
        delete_id = self.ui.lineEdit_3.text()
        if delete_id:
            main_connect = connect_db('tests.db')
            main_cursor = main_connect.cursor()
            delete_sql = '''DELETE FROM tests_results WHERE id=''' + delete_id
            main_cursor.execute(delete_sql)
            main_connect.commit()
            main_cursor.close()
            main_connect.close()
            self.btnClickedShowAll()
            self.ui.lineEdit_3.setText('')
        else:
            error = "Enter ID of the test to remove"
        """if error:
            self.ui.label_7.setText(error)
            self.ui.label_7.setStyleSheet('color: red')
        else:
            self.ui.label_7.setText('')"""

    def btnClickedAdd(self):
        main_connect = connect_db('tests.db')
        main_cursor = main_connect.cursor()

        insert_list = []
        if (self.ui.lineEdit.text() == '' or self.ui.lineEdit_2.text() == ''):
            error = "Cant add blank fields"
        else:
            insert_list.append(self.ui.lineEdit.text())
            insert_list.append(self.ui.lineEdit_2.text())
            datetime_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_list.append(datetime_now)
            insert_list.append(self.ui.spinBox.text())

            insert_sql = '''INSERT INTO tests_results (Device_type, Operator, Time, Success) VALUES(?, ?, ?, ?);'''
            main_cursor.execute(insert_sql, insert_list)
            main_connect.commit()
            main_cursor.close()
            main_connect.close()
        self.ui.lineEdit_2.setText('')
        self.ui.lineEdit.setText('')
        self.ui.spinBox.setValue(0)
        self.btnClickedShowAll()
        """if error:
            self.ui.label_7.setText(error)
            self.ui.label_7.setStyleSheet('color: red')"""


    def btnClickedShowAll(self):
        show_list = show_all_tests()
        row = 0
        for line in show_list:
            col = 0
            for cell_data in line:
                col += 1
            row += 1
        self.ui.tableWidget_2.setRowCount(row)
        self.ui.tableWidget_2.setColumnCount(col)
        header = ['ID', 'Device type', 'Operator', 'Time', 'Success']
        self.ui.tableWidget_2.setHorizontalHeaderLabels(header)

        row = 0
        for line in show_list:
            col = 0
            for cell_data in line:
                cellinfo = QTableWidgetItem(str(cell_data))
                cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidget_2.setItem(row, col, cellinfo)
                col += 1
            row += 1


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()

    sys.exit(app.exec())
