# This is a sample Python script.

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press F9 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QHeaderView, QMessageBox, QPushButton
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt5.QtGui import QTextDocument, QTextCursor
from PyQt5.QtPrintSupport import QPrinter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Connexion à la base de données
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('database.db')
        if not self.db.open():
            QMessageBox.critical(None, "Erreur de connexion", "Impossible de se connecter à la base de données.")
            sys.exit(1)

        # Création de la table si elle n'existe pas
        query = QSqlQuery()
        query.exec_(
            "CREATE TABLE IF NOT EXISTS tableau (id INTEGER PRIMARY KEY AUTOINCREMENT, numero_suivi INTEGER UNIQUE, numero_dossier TEXT)")

        # Modèle de données pour la vue
        self.model = QSqlQueryModel()
        self.model.setQuery('SELECT * FROM tableau')
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setCentralWidget(self.view)

        # Bouton pour générer le PDF
        self.btn_pdf = QPushButton('Générer le PDF')
        self.btn_pdf.clicked.connect(self.generate_pdf)
        self.view.setCornerWidget(0, 2, self.btn_pdf)


    def generate_pdf(self):
        # Récupération des données
        query = QSqlQuery('SELECT numero_suivi, numero_dossier FROM tableau ORDER BY id')
        data = []
        while query.next():
            data.append((query.value(0), query.value(1)))

        # Création du document
        doc = QTextDocument()
        cursor = QTextCursor(doc)
        cursor.insertText('Numéro de suivi\tNuméro de dossier\n')
        for row in data:
            cursor.insertText(f'{row[0]}\t\t{row[1]}\n')

        # Impression ou sauvegarde du PDF
        printer = QPrinter()
        if printer.isValid():
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName('tableau.pdf')
            doc.print_(printer)
            QMessageBox.information(None, "Succès", "Le fichier PDF a été généré avec succès.")
        else:
            QMessageBox.critical(None, "Erreur", "Impossible d'initialiser l'imprimante.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
