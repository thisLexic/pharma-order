import sys
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from ui.design import *


class DlgMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(DlgMain, self).__init__()
        self.setupUi(self)

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("data/app.db")
        if db.open():
            if "product" not in db.tables():
                self.createTableProduct()
            self.populateUiTableProduct()
        else:
            QMessageBox.critical(self, "Database Error", "Could not connect to the database")
    
    def createTableProduct(self):
        sql = """
            CREATE TABLE IF NOT EXISTS product (
                product_id INTEGER PRIMARY KEY,
                code TEXT NOT NULL UNIQUE,
                brand TEXT NOT NULL,
                generic TEXT,
                size TEXT NOT NULL,
                class TEXT NOT NULL,
                type TEXT NOT NULL,
                price REAL NOT NULL,
                cost REAL NOT NULL,
                ave_per_month REAL,
                high INTEGER,
                low INTEGER
            )
        """ 
        query = QSqlQuery()  
        query.exec(sql)
        query.exec("insert into product values(1, '11', 'Amoxyl', 'Amoxycilin', '25mg', 'cardio', 'tablet', 2.43, 1.34, 4.6, 7, 3)")
        query.exec("insert into product values(2, '20', 'Right Med', 'Amlodipin, '100mg', 'cardio', 'capsule', 64.30, 38.34, 104, 203, 58)")

    def populateUiTableProduct(self):
        query = QSqlQuery()
        bOk = query.exec("SELECT * FROM product ORDER BY brand, generic")
        if bOk:
            while query.next():
                row = self.table_product.rowCount()
                self.table_product.insertRow(row)
                for col in range(1, 12):
                    twi = QTableWidgetItem(str(query.value(col)))
                    self.table_product.setItem(row, col-1, twi)
        else:
            QMessageBox.critical(self, "Database Error", query.lastError().text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec_())