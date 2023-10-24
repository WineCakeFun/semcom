from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import*
from PyQt5.QtGui import QFont
import sys, os
from semcom import process, export_incompatibilities_to_file, incompatibilities
from semcom.mongodb import save_incompatibilities_to_mongodb, retrieve_incompatibilities_from_mongodb
from incom_window import*


global __Scenario
global __Domain
incompatibilities_window = None 
app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle('Забезпечення семантичної сумісності')

# Кнопка "Завантажити сценарій"
button_script = QPushButton("Завантажити сценарій")


# Напис біля кнопки "Завантажити сценарій"
label_script = QLabel("...")


# Кнопка "Завантажити онтологію"
button_ontology = QPushButton("Завантажити онтологію")


# Напис біля кнопки "Завантажити онтологію"
label_ontology = QLabel("...")


# Кнопка "Перевірити сумісність"
button_check = QPushButton("Перевірити сумісність")


button_db_save = QPushButton("Зберегти дані про невідповідності")
button_db_save.setDisabled(True)


button_show_incompatibilities = QPushButton("Показати невідповідності")

def on_click_show_incompatibilities():
    global incompatibilities_window
    incomps = retrieve_incompatibilities_from_mongodb()
    incompatibilities_window = IncompatibilitiesWindow(incomps)
    incompatibilities_window.show()


text_check = QTextEdit()
LayoutH1 = QHBoxLayout()
LayoutH2 = QHBoxLayout()
LayoutH3 = QHBoxLayout()

LayoutH1.addWidget(button_script, alignment = Qt.AlignCenter)
LayoutH1.addWidget(label_script, alignment = Qt.AlignCenter)
LayoutH1.addWidget(button_ontology, alignment = Qt.AlignCenter)
LayoutH1.addWidget(label_ontology, alignment = Qt.AlignCenter)
LayoutH2.addWidget(text_check)
LayoutH3.addWidget(button_check, alignment = Qt.AlignCenter)
LayoutH3.addWidget(button_db_save, alignment = Qt.AlignCenter)
LayoutH3.addWidget(button_show_incompatibilities, alignment = Qt.AlignCenter)

LayoutV = QVBoxLayout()
LayoutV.addLayout(LayoutH1)
LayoutV.addLayout(LayoutH2)
LayoutV.addLayout(LayoutH3)

central_widget = QWidget()
central_widget.setLayout(LayoutV)

window.setCentralWidget(central_widget)
# window.setLayout(LayoutV)

def on_click_script(event):
    global __Scenario
    try:
        filename, _ = QFileDialog.getOpenFileName(
            window, "Виберіть сценарій", "", "Сценарій (*.owl *.owx)")
        if filename:
            __Scenario = filename
            # Extract only the filename and extension
            filename_only = os.path.basename(filename)
            label_script.setText(filename_only)
    except:
        pass

def on_click_ontology(event):
    global __Domain
    try:
        filename, _ = QFileDialog.getOpenFileName(
            window, "Виберіть онтологію", "", "Онтологія (*.owl *.owx *.rdf)")
        if filename:
            __Domain = filename
            # Extract only the filename and extension
            filename_only = os.path.basename(filename)
            label_ontology.setText(filename_only)
    except:
        pass



def on_click_check(event):
    text_check.clear()
    incompatibilities.clear()
    global __Scenario
    global __Domain
    try:
        process(__Scenario, __Domain)
        if len(incompatibilities) == 0:
            text_check.append('Семантично сумісно')
        else:
            button_db_save.setEnabled(True)
            text_check.append("Знайдено семантичну несумісність!")
            separator_line = "-" * 50  # Create a separator line of hyphens
            text_check.append(separator_line)
            for incompatibility in incompatibilities:
                text_check.append(f"Тип даних \"'{incompatibility[0]}'\", що використовується в елементі \"'{incompatibility[1]}'\", не знайдено в онтології.")
                text_check.append(separator_line)
            export_incompatibilities_to_file('incompatibilities.txt')
    except:
        QMessageBox.warning(window, "Вибір", "Ви не вибрали файл!")



def on_click_save_icompatibility(event):
    save_incompatibilities_to_mongodb(incompatibilities)
    QMessageBox.information(window, "Збереження", "Успішно!")



# Increase the font size for labels
label_script.setFont(QFont("Times", 20))  # Adjust the size (12) as needed
label_ontology.setFont(QFont("Times", 20))  # Adjust the size (12) as needed

# Increase the font size for QPushButton text
button_script.setFont(QFont("Times", 20))  # Adjust the size (12) as needed
button_ontology.setFont(QFont("Times", 20))  # Adjust the size (12) as needed
button_check.setFont(QFont("Times", 20))  # Adjust the size (12) as needed
button_db_save.setFont(QFont("Times", 20))  # Adjust the size (12) as needed
button_show_incompatibilities.setFont(QFont("Times", 20))  # Adjust the size (12) as needed

# Increase the font size for QTextEdit
text_check.setFont(QFont("Times", 20))  # Adjust the size (12) as needed

# Now, you can resize the main window and the elements will adjust accordingly
window.resize(1280, 720)  # Adjust the size (width and height) as needed



button_script.clicked.connect(on_click_script)
button_ontology.clicked.connect(on_click_ontology)
button_check.clicked.connect(on_click_check)
button_db_save.clicked.connect(on_click_save_icompatibility)
button_show_incompatibilities.clicked.connect(on_click_show_incompatibilities)

window.show()
sys.exit(app.exec_())