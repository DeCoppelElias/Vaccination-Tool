from PyQt6.QtCore import QDate, QSize
from PyQt6.QtWidgets import QWidget, QStackedLayout, QLabel, QVBoxLayout, QDateEdit, QComboBox, QSpinBox, QTableWidget, \
    QPushButton, QDateTimeEdit, QHeaderView, QScrollArea, QGroupBox, QSpacerItem, QSizePolicy, QGridLayout

from GUI.PatientCheckGUI.VaccineInputForm import VaccineInputForm
from GUI.PatientCheckGUI.PatientResultsWidget import PatientResultsWidget


class PatientCheckWidget(QWidget):
    def __init__(self, vaccineManager):
        super().__init__()

        self.vaccineManager = vaccineManager
        self.resultScreen = PatientResultsWidget(vaccineManager)

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(VaccineInputForm(self, vaccineManager))
        self.stacked_layout.addWidget(self.resultScreen)
        self.stacked_layout.addWidget(QLabel("Something went wrong during vaccine initialisation. \n"
                                "By going to the 'View Vaccines' and 'View Illnesses',"
                                "you can check if all excel files are present."))
        self.refresh()

        self.setLayout(self.stacked_layout)

    def refresh(self):
        if self.vaccineManager.initialised:
            self.stacked_layout.setCurrentIndex(0)
        else:
            self.stacked_layout.setCurrentIndex(2)

    def toResults(self, patient_name, remark_dict):
        self.resultScreen.addResults(patient_name, remark_dict)
        self.stacked_layout.setCurrentIndex(1)
