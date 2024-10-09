import os

from PyQt6.QtWidgets import QWidget, QVBoxLayout

from GUI.ExcelViewerWidget import ExcelViewerWidget


class ViewIllnessesWidget(QWidget):
    def __init__(self):
        super().__init__()

        exe_dir = os.path.dirname(os.path.abspath(__file__))
        general_path = os.path.abspath(os.path.join(exe_dir, '../ExcelFiles'))

        excel = ExcelViewerWidget(general_path,
                                   "Illnesses.xlsx",
                                   "Excel table for illnesses: ")

        layout = QVBoxLayout()
        layout.addWidget(excel)

        self.setLayout(layout)
