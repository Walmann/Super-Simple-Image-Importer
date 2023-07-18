import json
import sys
from PySide6.QtWidgets import (
    QApplication,
    QListWidget,
    QListWidgetItem,
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QLabel,
    QCheckBox,
    QRadioButton,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QButtonGroup,
    QWidget,
)
from PySide6.QtCore import Qt, Signal, QObject, QEventLoop

from bin.handle_settings import SettingsHandlerClass
from datetime import datetime

from bin.handler_worker_queue import worker_queue_handler

# class Signals(QObject):
#     finished = Signal()


class work_order:
    def __init__(
        self, SortIntoFolders, FolderStructureSelection, FolderStructureNamingMethod
    ):
        self.SortIntoFolders = SortIntoFolders
        self.FolderStructureSelection = FolderStructureSelection
        self.FolderStructureNamingMethod = FolderStructureNamingMethod


class Export_jobs_widget(QMainWindow):
    start_import_signal = Signal(dict)

    def __init__(self, file_list_import):
        super().__init__()
        self.work_queue = {}
        self.file_list_import = file_list_import
        self.dateSetup = datetime.now().strftime('%Y-%m-%d')


        self.FolderStructureSelection = None
        self.SortIntoFolders = None
        self.FolderStructureNamingMethod = None

        self.setWindowTitle("Velg importering innstillinger")

        # Sjekker om filen "WorkQueue.json" eksisterer, og oppretter den hvis den ikke gjør det
        # self.check_work_queue_file()

        # Laster inn innstillingene fra SettingsHandlerClass
        self.settings_handler = SettingsHandlerClass()
        self.get_settings()

        # Opprett hovedlayout
        layout = QHBoxLayout()

        # Layout for innstillinger på venstre side
        settings_layout = QVBoxLayout()

        # Label for "Sorter Importeringen inn i mapper" checkbox
        self.sort_label = QLabel("Sorter Importeringen inn i mapper")
        settings_layout.addWidget(self.sort_label)

        # Checkbox for "Sorter Importeringen inn i mapper"
        self.sort_checkbox = QCheckBox()
        self.sort_checkbox.setChecked(self.SortIntoFolders)
        self.sort_checkbox.clicked.connect(self.setting_changed)
        settings_layout.addWidget(self.sort_checkbox)

        # Radio buttons for "FolderStructureSelection"
        self.folder_structure_selection_group = QButtonGroup()

        self.radio_label = QLabel("Velg Mappestruktur:")
        settings_layout.addWidget(self.radio_label)

        self.radio_button1 = QRadioButton("Ingen")
        self.radio_button1.setChecked(self.FolderStructureSelection == "")
        self.radio_button1.toggled.connect(self.setting_changed)
        settings_layout.addWidget(self.radio_button1)
        self.folder_structure_selection_group.addButton(self.radio_button1)

        self.radio_button2 = QRadioButton("År")
        self.radio_button2.setChecked(self.FolderStructureSelection == "YYYY")
        self.radio_button2.toggled.connect(self.setting_changed)
        settings_layout.addWidget(self.radio_button2)
        self.folder_structure_selection_group.addButton(self.radio_button2)

        self.radio_button3 = QRadioButton("År-Måned")
        self.radio_button3.setChecked(self.FolderStructureSelection == "YYYY-MM")
        self.radio_button3.toggled.connect(self.setting_changed)
        settings_layout.addWidget(self.radio_button3)
        self.folder_structure_selection_group.addButton(self.radio_button3)

        self.radio_button4 = QRadioButton("År-Måned-Dato")
        self.radio_button4.setChecked(self.FolderStructureSelection == "YYYY-MM-DD")
        self.radio_button4.toggled.connect(self.setting_changed)
        settings_layout.addWidget(self.radio_button4)
        self.folder_structure_selection_group.addButton(self.radio_button4)

        # Radio buttons for "FolderStructureNamingMethod"
        self.naming_label = QLabel("Navngi mappene direkte eller lag undermapper?:")
        settings_layout.addWidget(self.naming_label)

        # Radio buttons for "FolderStructureNamingMethod"
        self.folder_structure_naming_group = QButtonGroup()

        self.naming_button1 = QRadioButton("Lag undermapper")
        self.naming_button1.setChecked(self.FolderStructureNamingMethod == "subFolders")
        self.naming_button1.toggled.connect(self.setting_changed)
        settings_layout.addWidget(self.naming_button1)
        self.folder_structure_naming_group.addButton(self.naming_button1)

        self.naming_button2 = QRadioButton("Sett navnet direkte på mappen")
        self.naming_button2.setChecked(self.FolderStructureNamingMethod == "direct")
        self.naming_button2.toggled.connect(self.setting_changed)
        settings_layout.addWidget(self.naming_button2)
        self.folder_structure_naming_group.addButton(self.naming_button2)

        # Felt for å skrive inn navnet på importen
        self.name_label = QLabel("Velg navn på ny mappe: (?)")
        settings_layout.addWidget(self.name_label)
        self.name_label.setCursor(Qt.WhatsThisCursor)
        self.name_label.setToolTip(
            f"Hvis ingen tekst er satt, vil {self.dateSetup} bli brukt som navn"
        )

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(f"{self.dateSetup}")
        settings_layout.addWidget(self.name_input)

        # FUTURE Add Jobs function. Now i just need it to import a single job first. This button is disabled to not cunfuse pepole
        # # Button for å legge til i jobblisten
        # self.add_button = QPushButton("Legg til i jobblisten")
        # self.add_button.clicked.connect(self.add_to_work_queue)
        # settings_layout.addWidget(self.add_button)

        # Button for å starte importeringen
        self.start_button = QPushButton("Start Import")
        self.start_button.clicked.connect(self.start_import)
        settings_layout.addWidget(self.start_button)

        # Legg til innstillingene i hovedlayoutet
        layout.addLayout(settings_layout)

        # Skillelinjemellom layout og jobbliste
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        # QListWidget for jobblisten på høyre side
        self.job_list_widget = QListWidget()
        self.job_list_widget.setWindowTitle("Jobber i kø")
        layout.addWidget(self.job_list_widget)

        # Opprett en widget for å vise layoutet og sett den som sentralwidget i hovedvinduet
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def setting_changed(self, checked=None):
        sender = self.sender()  # Henter objektet som utløste signalet

        if sender.isChecked():
            # Setter variabelen basert på hvilken RadioButton som er valgt

            # datetime.now().strftime('%Y-%m-%d')


            if sender == self.radio_button1:
                self.FolderStructureSelection = ""
            elif sender == self.radio_button2:
                self.FolderStructureSelection = "%Y"
            elif sender == self.radio_button3:
                self.FolderStructureSelection = "%Y-%m"
            elif sender == self.radio_button4:
                self.FolderStructureSelection = "%Y-%m-%d"
            elif sender == self.naming_button1:
                self.FolderStructureNamingMethod = "subFolders"
            elif sender == self.naming_button2:
                self.FolderStructureNamingMethod = "direct"
        if sender == self.sort_checkbox:
            self.SortIntoFolders = checked
            print(self.SortIntoFolders)

    def get_settings(self):
        default_sort_into_folders = True
        default_folder_structure_selection = ""
        default_folder_structure_naming_method = "subFolders"

        self.SortIntoFolders = self.settings_handler.LoadSetting("SortIntoFolders")
        self.FolderStructureSelection = self.settings_handler.LoadSetting(
            "FolderStructureSelection"
        )
        self.FolderStructureNamingMethod = self.settings_handler.LoadSetting(
            "FolderStructureNamingMethod"
        )

        if self.SortIntoFolders is None:
            self.SortIntoFolders = default_sort_into_folders

        if self.FolderStructureSelection is None:
            self.FolderStructureSelection = default_folder_structure_selection

        if self.FolderStructureNamingMethod is None:
            self.FolderStructureNamingMethod = default_folder_structure_naming_method

    # def check_work_queue_file(self):
    #     try:
    #         with open("WorkQueue.json", "r"):
    #             pass
    #     except FileNotFoundError:
    #         with open("WorkQueue.json", "w"):
    #             pass

    def add_to_work_queue(self):
        # Hent innholdet fra "WorkQueue.json" hvis det eksisterer
        try:
            self.work_queue = worker_queue_handler.load()
        except FileNotFoundError:
            self.work_queue = {}

        # Legg til de nye elementene i work_queue-dictionaryen
        work_name = self.name_input.text()

        if work_name == "":
            self.name_input.placeholderText()

        if len(work_name) == 0:
            work_name = self.dateSetup

        # Make sure there are no duplicate names in work_queue
        duplicate_number = 0
        while True:
            if work_name not in self.work_queue:
                break
            else:
                duplicate_number = duplicate_number + 1
                work_name = work_name.split("(")[0]
                work_name = f"{work_name}({str(duplicate_number)})"

        self.work_queue[work_name] = {}
        self.work_queue[work_name]["FolderName"] = work_name
        self.work_queue[work_name]["SortIntoFolders"] = self.SortIntoFolders
        self.work_queue[work_name]["FolderStructureSelection"] = self.FolderStructureSelection
        self.work_queue[work_name]["FolderStructureNamingMethod"] = self.FolderStructureNamingMethod
        self.work_queue[work_name]["FilesToImport"] = self.file_list_import


        # Skriv work_queue-dictionaryen til "WorkQueue.json"
        # with open("WorkQueue.json", "w") as file:
            # for x in self.work_queue:
                # file.write(json.dump(self.work_queue))
        worker_queue_handler.save(self, work_queue=self.work_queue)


        # Legg til Work_name i Work_queue elementer i UI
        self.job_list_widget.addItem(work_name)

    def start_import(self):
        try:
            self.work_queue = worker_queue_handler.load()
        except FileNotFoundError:
            # self.work_queue = {}
            self.add_to_work_queue()

        if len(self.work_queue) == 0:
            self.add_to_work_queue()

        # Sender signalet med work_queue
        self.get_work_queue()

    def get_work_queue(self):
        try:
            self.work_queue = worker_queue_handler.load()
        except FileNotFoundError:
            self.work_queue = {}

        # return self.work_queue
        self.start_import_signal.emit(self.work_queue)

    # def waitForSelection(self):

    # loop = QEventLoop()
    # self.start_import_signal.connect(loop.quit)
    # loop.exec_()
    # return self.work_queue


# def start(file_list):
#     temp = QApplication.instance()

#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()

#     work_queue = window.waitForSelection()

#     return work_queue

#     sys.exit(app.exec())
