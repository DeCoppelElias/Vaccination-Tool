from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QGroupBox, QSizePolicy, QSpacerItem, QGridLayout, \
    QPushButton
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QSizePolicy, QGroupBox


class PatientResultsWidget(QWidget):
    def __init__(self, patientCheckWidget, vaccineManager):
        super().__init__()

        self.vaccineManager = vaccineManager

        self.patient_name = ""
        self.remark_dict = {}

        self.illnessWidgets = []

        self.layout = QVBoxLayout()

        # Scroll area for all supported illnesses
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_content = QWidget()
        self.illness_layout = QVBoxLayout(self.scroll_area_content)
        self.scroll_area.setWidget(self.scroll_area_content)

        # Label for name of patient
        self.name_label = QLabel("")
        self.name_label.setStyleSheet("font-weight: bold; font-size: 16px;")

        self.to_input_button = QPushButton("Back")
        self.to_input_button.clicked.connect(patientCheckWidget.toInput)
        self.to_input_button.setFixedSize(QSize(100, 30))

        self.top_layout = QGridLayout()
        self.top_layout.addWidget(self.name_label, 0, 0, alignment=Qt.AlignmentFlag.AlignBottom)
        self.top_layout.addWidget(self.to_input_button, 0, 5)

        self.layout.addLayout(self.top_layout)
        self.layout.addWidget(self.scroll_area)

        self.refreshUI()

        self.setLayout(self.layout)

        self.vaccineManager.updated.connect(self.refreshUI)

    def addResults(self, patient_name, remark_dict):
        self.patient_name = patient_name
        self.remark_dict = remark_dict
        self.refreshUI()

    def refreshUI(self):
        if not self.vaccineManager.initialised:
            return

        # Change name
        self.name_label.setText("Results for patient: " + self.patient_name)

        # Remove all widgets
        for widget in self.illnessWidgets:
            self.illness_layout.removeWidget(widget)
        self.illnessWidgets = []

        # Add new widget for each illness
        for illness in self.vaccineManager.illnesses:
            remarks = []
            if illness in self.remark_dict.keys():
                remarks = self.remark_dict[illness]

            widget = IllnessEntry(illness, remarks)
            self.illnessWidgets.append(widget)
            self.illness_layout.addWidget(widget)


class IllnessEntry(QGroupBox):
    def __init__(self, illness_name, illness_remarks):
        super().__init__()

        self.layout = QVBoxLayout()

        # Label with name of illness
        label = QLabel(illness_name)
        size_policy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        label.setSizePolicy(size_policy)
        label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.layout.addWidget(label)

        # All remarks about that illness
        self.remarks_layout = QVBoxLayout()

        for remark in illness_remarks:
            remark_label = QLabel(remark)
            remark_label.setStyleSheet("font-size: 12px;")
            self.remarks_layout.addWidget(remark_label)

        self.layout.addLayout(self.remarks_layout)
        self.setLayout(self.layout)
