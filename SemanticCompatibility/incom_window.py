from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy, QAbstractScrollArea
from PyQt5.QtGui import QFont

class IncompatibilitiesWindow(QMainWindow):
    def __init__(self, incompatibilities):
        super().__init__()

        self.setWindowTitle('Невідповідності')
        self.setGeometry(100, 100, 1000, 400)  # Adjust the width to accommodate the content

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        self.populate_table(incompatibilities)

    def populate_table(self, incompatibilities):
        self.table_widget.setRowCount(len(incompatibilities))
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(['Data Type | Тип даних', 'Element Name | Назва елементу'])

        for row, incompatibility in enumerate(incompatibilities):
            item1 = QTableWidgetItem(incompatibility['data_type'])
            item2 = QTableWidgetItem(incompatibility['element_name'])
            
            # Set a larger font for the table items
            font = QFont()
            font.setPointSize(16)  # Adjust the font size as needed
            item1.setFont(font)
            item2.setFont(font)
            
            self.table_widget.setItem(row, 0, item1)
            self.table_widget.setItem(row, 1, item2)
        
        # Adjust the column width to fit the content
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
