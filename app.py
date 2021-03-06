import sys
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from ui.main_design import *
from ui.add_product_design import *


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
        
        self.button_add_product.clicked.connect(self.event_button_add_product_clicked)

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
                is_active INTEGER NOT NULL,
                ave_per_month REAL,
                high INTEGER,
                low INTEGER
            )
        """ 
        query = QSqlQuery()  
        query.exec(sql)
        query.exec("insert into product values(1, '11', 'Amoxyl', 'Amoxycilin', '25mg', 'cardio', 'tablet', 2.43, 1.34, 1, 4.6, 7, 3)")


    def populateUiTableProduct(self):
        self.table_product.clearContents()
        self.table_product.setRowCount(0)
        query = QSqlQuery()
        bOk = query.exec("SELECT * FROM product ORDER BY brand, generic")
        if bOk:
            while query.next():
                row = self.table_product.rowCount()
                self.table_product.insertRow(row)
                for col in range(1, 13):
                    if col == 9:
                        value = query.value(col)
                        if value == 0:
                            value = "No"
                        else:
                            value = "Yes"
                        twi = QTableWidgetItem(value)
                    else:
                        twi = QTableWidgetItem(str(query.value(col)))
                    self.table_product.setItem(row, col-1, twi)
        else:
            QMessageBox.critical(self, "Database Error", query.lastError().text())

    def event_button_add_product_clicked(self):
        dlgAddProduct = DlgAddProduct()
        dlgAddProduct.button_submit_product.clicked.connect(dlgAddProduct.event_button_submit_clicked)
        dlgAddProduct.show()
        dlgAddProduct.exec()
        self.populateUiTableProduct()


class DlgAddProduct(QDialog, Ui_add_product_dialog):
    def __init__(self):
        super(DlgAddProduct, self).__init__()
        self.setupUi(self)
        
        self.button_cancel.clicked.connect(self.close)

    def event_button_submit_clicked(self):
        self.validate_product_data()
        query = QSqlQuery()
        query.prepare("INSERT into product (code, brand, generic, size, class, type, price, cost, is_active, ave_per_month, high, low) VALUES(:code, :brand, :generic, :size, :class, :type, :price, :cost, :is_active, :ave_per_month, :high, :low)")
        query.bindValue(":code", self.value_code_product.text())
        query.bindValue(":brand", self.value_brand_product.text())
        query.bindValue(":generic", self.value_generic_product.text())
        query.bindValue(":size", self.value_size_product.text())
        query.bindValue(":class", self.value_class_product.currentText())
        query.bindValue(":type", self.value_type_product.currentText())
        query.bindValue(":price", self.value_price_product.text())
        query.bindValue(":cost", self.value_cost_product.text())
        query.bindValue(":is_active", self.value_is_active_product.checkState())
        query.bindValue(":ave_per_month", 0)
        query.bindValue(":high", 0)
        query.bindValue(":low", 0)
        bOk = query.exec()
        if bOk:
            QMessageBox.information(self, "Successfully added", "Product was added successfully")
            self.close()
        else:
            QMessageBox.warning(self, "Database Error", query.lastError().text())
        

    def validate_product_data(self):
        print("Data being validated for product")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec_())