from PyQt6.QtCore import QDate, QSize, Qt
from PyQt6.QtWidgets import QWidget, QStackedLayout, QLabel, QVBoxLayout, QDateEdit, QComboBox, QSpinBox, QTableWidget, \
    QPushButton, QDateTimeEdit, QHeaderView, QScrollArea, QGroupBox, QSpacerItem, QSizePolicy, QGridLayout

from GUI.PatientCheckGUI.VaccineInputForm import VaccineInputForm
from GUI.PatientCheckGUI.PatientResultsWidget import PatientResultsWidget


class PatientCheckWidget(QWidget):
    def __init__(self, main_window, vaccineManager):
        super().__init__()

        self.vaccineManager = vaccineManager

        self.error_screen = QGroupBox()
        self.error_layout = QGridLayout()
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(main_window.toCheckVaccines)
        self.refresh_button.setFixedSize(QSize(100, 30))
        self.error_message = QLabel("Something went wrong during vaccine initialisation. \n"
                                    "By going to the 'View Vaccines' and 'View Illnesses', "
                                    "you can check if all excel files are present.")
        self.error_screen.setLayout(self.error_layout)

        self.error_layout.addWidget(self.error_message, 0, 0, alignment=Qt.AlignmentFlag.AlignBottom)
        self.error_layout.addWidget(self.refresh_button, 0, 5)

        self.resultScreen = PatientResultsWidget(self, vaccineManager)

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(VaccineInputForm(self, vaccineManager))
        self.stacked_layout.addWidget(self.resultScreen)
        self.stacked_layout.addWidget(self.error_screen)
        self.refreshUI()

        self.setLayout(self.stacked_layout)

        self.vaccineManager.updated.connect(self.refreshUI)

    def refreshUI(self):
        if self.vaccineManager.initialised:
            self.stacked_layout.setCurrentIndex(0)
        else:
            self.stacked_layout.setCurrentIndex(2)

    def toResults(self, patient_name, remark_dict):
        self.resultScreen.addResults(patient_name, remark_dict)
        self.stacked_layout.setCurrentIndex(1)

    def toInput(self):
        self.refreshUI()
