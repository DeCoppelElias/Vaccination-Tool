import sys

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QWidget, QMainWindow, \
    QToolBar
from PyQt6.QtWidgets import QStackedLayout

from GUI.ViewIllnessesWidget import ViewIllnessesWidget
from GUI.WarningDialog import WarningDialog
from GUI.ViewVaccinesWidget import ViewVaccinesWidget
from GUI.PatientCheckGUI.PatientCheckWidget import PatientCheckWidget


class MainWindow(QMainWindow):
    def __init__(self, vaccineManager):
        super().__init__()

        dlg = WarningDialog()
        if not dlg.exec():
            sys.exit()

        self.setWindowTitle("Vaccine Tool")
        self.setFixedSize(QSize(800, 600))

        self.vaccineManager = vaccineManager

        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.toggleViewAction().setVisible(False)
        self.addToolBar(toolbar)

        button_action = QAction("Patient Check", self)
        button_action.triggered.connect(self.toCheckVaccines)
        toolbar.addAction(button_action)

        button_action = QAction("View Vaccines", self)
        button_action.triggered.connect(self.toViewVaccines)
        toolbar.addAction(button_action)

        button_action = QAction("View Illnesses", self)
        button_action.triggered.connect(self.toViewIllnesses)
        toolbar.addAction(button_action)

        self.checkVaccinesWidget = PatientCheckWidget(self, self.vaccineManager)
        self.viewVaccinesWidget = ViewVaccinesWidget(self.vaccineManager)
        self.viewIllnessesWidget = ViewIllnessesWidget(self.vaccineManager)

        self.stack_layout = QStackedLayout()

        self.stack_layout.addWidget(self.checkVaccinesWidget)
        self.stack_layout.addWidget(self.viewVaccinesWidget)
        self.stack_layout.addWidget(self.viewIllnessesWidget)
        self.stack_layout.setCurrentIndex(0)

        widget = QWidget()
        widget.setLayout(self.stack_layout)
        self.setCentralWidget(widget)

    def toCheckVaccines(self):
        self.vaccineManager.reLoadVaccines()
        self.stack_layout.setCurrentIndex(0)

    def toViewVaccines(self):
        self.vaccineManager.reLoadVaccines()
        self.stack_layout.setCurrentIndex(1)

    def toViewIllnesses(self):
        self.vaccineManager.reLoadVaccines()
        self.stack_layout.setCurrentIndex(2)
