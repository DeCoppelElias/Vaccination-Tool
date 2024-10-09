from PyQt6.QtCore import QSize, QDate, Qt
from PyQt6.QtWidgets import QWidget, QLabel, QDateEdit, QVBoxLayout, QScrollArea, QPushButton, QGroupBox, QGridLayout, \
    QSpinBox, QTableWidget, QDateTimeEdit, QComboBox, QLineEdit

from GUI.NormalDialog import NormalDialog


class VaccineInputForm(QWidget):
    def __init__(self, patientCheckWidget, vaccineManager):
        super().__init__()

        self.setContentsMargins(9, 0, 9, 0)

        self.patientCheckWidget = patientCheckWidget
        self.vaccines = vaccineManager.vaccines
        self.vaccineManager = vaccineManager

        # Main layout for the form
        self.main_layout = QVBoxLayout()

        # Patient name input
        self.patient_name_label = QLabel("Enter patient name:")
        self.patient_name_input = QLineEdit()
        self.patient_name_input.setFixedSize(QSize(110, 30))
        self.patient_name_input.setPlaceholderText("Full Name")
        self.patient_name_input.setStyleSheet("color: white;")

        self.reset_form_button = QPushButton("Reset Form")
        self.reset_form_button.clicked.connect(self.resetForm)
        self.reset_form_button.setFixedSize(QSize(100, 30))

        self.top_layout = QGridLayout()
        self.top_layout.addWidget(self.patient_name_label, 0, 0, alignment=Qt.AlignmentFlag.AlignBottom)
        self.top_layout.addWidget(self.reset_form_button, 0, 5)

        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addWidget(self.patient_name_input)

        # Birthday input
        self.birthday_label = QLabel("Enter patient birthday:")
        self.birthday_input = QDateEdit()
        self.birthday_input.setFixedSize(QSize(110, 30))
        self.birthday_input.setDisplayFormat("yyyy-MM-dd")
        self.birthday_input.setCalendarPopup(True)
        self.birthday_input.setDate(QDate.currentDate())
        self.main_layout.addWidget(self.birthday_label)
        self.main_layout.addWidget(self.birthday_input)

        # Scrollable area to hold multiple vaccine entries
        self.scroll_area = QScrollArea()
        self.vaccine_container = QWidget()
        self.vaccine_layout = QVBoxLayout()

        # Initialize with a single vaccine entry
        self.vaccine_entries = []
        self.add_vaccine_entry()

        # Set up scroll area
        self.vaccine_container.setLayout(self.vaccine_layout)
        self.scroll_area.setWidget(self.vaccine_container)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        # Add vaccine button
        self.add_vaccine_button = QPushButton("Add Vaccine")
        self.add_vaccine_button.clicked.connect(self.add_vaccine_entry)
        self.add_vaccine_button.setFixedSize(QSize(100, 30))
        self.main_layout.addWidget(self.add_vaccine_button)

        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_data)
        self.submit_button.setFixedSize(QSize(100, 30))
        self.main_layout.addWidget(self.submit_button)

        self.setLayout(self.main_layout)

    def add_vaccine_entry(self):
        # Add a new vaccine entry widget
        vaccine_entry = VaccineEntryWidget(self)
        self.vaccine_entries.append(vaccine_entry)
        self.vaccine_layout.addWidget(vaccine_entry)

    def remove_vaccine_entry(self, widget):
        self.vaccine_entries.remove(widget)
        self.vaccine_layout.removeWidget(widget)
        widget.deleteLater()

    def submit_data(self):
        # Check if data is correctly filled in
        patient_name = self.patient_name_input.text()
        if patient_name == "":
            dlg = NormalDialog("Submit failed", "Please enter a valid patient name.")
            dlg.exec()
            return

        # Reload vaccines in case excel files have changed
        self.vaccineManager.reLoadVaccines()

        # Get all data from filled in vaccine form
        user_vaccines = []
        for i in range(self.vaccine_layout.count()):
            vaccine_entry_widget = self.vaccine_layout.itemAt(i).widget()
            vaccine_name, dose_dates = vaccine_entry_widget.get_vaccine_data()
            print(dose_dates)
            user_vaccines.append((
                vaccine_name,
                len(dose_dates),
                dose_dates
            ))

        # Perform method the check the user vaccines and relocate to results screen
        remark_dict = self.vaccineManager.check_vaccines(user_vaccines, self.birthday_input.date().toPyDate())
        self.patientCheckWidget.toResults(patient_name, remark_dict)

    def resetForm(self):
        self.patient_name_input.setText("")
        self.birthday_input.setDate(QDate.currentDate())
        for vaccine_entry in self.vaccine_entries.copy():
            self.remove_vaccine_entry(vaccine_entry)

        self.vaccine_entries = []
        self.add_vaccine_entry()


class VaccineEntryWidget(QGroupBox):
    def __init__(self, vaccineInputForm):
        super().__init__()

        self.vaccineInputForm = vaccineInputForm

        # Layout for the vaccine entry
        layout = QVBoxLayout()

        # Vaccine selection
        self.vaccine_label = QLabel("Select a vaccine:")
        self.vaccine_combo = QComboBox()
        for vaccine in vaccineInputForm.vaccines:
            self.vaccine_combo.addItem(vaccine.name)
        self.vaccine_combo.setFixedSize(QSize(100, 30))
        self.vaccine_combo.setContentsMargins(10,0,0,0)

        # Remove vaccine button
        self.remove_vaccine_button = QPushButton("Remove Vaccine")
        self.remove_vaccine_button.clicked.connect(self.remove_this)
        self.remove_vaccine_button.setFixedSize(QSize(100, 30))

        # Top banner
        self.top_layout = QGridLayout()
        self.top_layout.addWidget(self.vaccine_label, 0, 0, alignment=Qt.AlignmentFlag.AlignBottom)
        self.top_layout.addWidget(self.remove_vaccine_button, 0, 5)

        # Number of doses input
        self.dose_label = QLabel("Number of doses taken:")
        self.dose_spinbox = QSpinBox()
        self.dose_spinbox.setRange(0, 10)
        self.dose_spinbox.setValue(1)
        self.dose_spinbox.setFixedSize(QSize(100, 30))
        self.dose_spinbox.valueChanged.connect(self.apply_doses)

        # Table for dose dates
        self.dose_table = QTableWidget(1, 1)
        self.dose_table.setHorizontalHeaderLabels(["Dose Date"])

        # Add a row for the first dose date
        self.apply_doses()

        # Add all elements to the layout
        layout.addLayout(self.top_layout)
        layout.addWidget(self.vaccine_combo)
        layout.addWidget(self.dose_label)
        layout.addWidget(self.dose_spinbox)
        layout.addWidget(self.dose_table)

        self.setLayout(layout)

    def apply_doses(self):
        num_doses = self.dose_spinbox.value()

        if num_doses < 1:
            num_doses = 1
            self.dose_spinbox.setValue(1)

        self.dose_table.setColumnCount(num_doses)
        for column in range(num_doses):
            if not self.dose_table.cellWidget(0, column):
                date_edit = QDateTimeEdit(QDate.currentDate())
                date_edit.setDisplayFormat("yyyy-MM-dd")
                date_edit.setCalendarPopup(True)
                self.dose_table.setCellWidget(0, column, date_edit)
                self.dose_table.resizeColumnsToContents()
                self.dose_table.resizeRowsToContents()

    def get_vaccine_data(self):
        vaccine_name = self.vaccine_combo.currentText()
        dose_dates = []
        for column in range(self.dose_table.columnCount()):
            date_edit = self.dose_table.cellWidget(0, column)
            dose_dates.append(date_edit.date().toPyDate())
        return vaccine_name, dose_dates

    def remove_this(self):
        self.vaccineInputForm.remove_vaccine_entry(self)
