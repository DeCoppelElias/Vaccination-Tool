import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from GUI.ExcelViewerWidget import ExcelViewerWidget


class ViewVaccinesWidget(QWidget):
    def __init__(self, vaccineManager):
        super().__init__()

        exe_dir = os.path.dirname(os.path.abspath(__file__))
        general_path = os.path.abspath(os.path.join(exe_dir, '../ExcelFiles'))

        excel1 = ExcelViewerWidget(general_path,
                                   "Vaccines.xlsx",
                                   "Excel table for vaccine doses and illnesses: ")
        excel2 = ExcelViewerWidget(general_path,
                                   "VaccineIntervals.xlsx",
                                   "Excel table for vaccine intervals: ")
        excel3 = ExcelViewerWidget(general_path,
                                   "VaccineMinimumAges.xlsx",
                                   "Excel table for vaccine minimum ages: ")

        layout = QVBoxLayout()
        layout.addWidget(excel1)
        layout.addWidget(excel2)
        layout.addWidget(excel3)

        self.setLayout(layout)

        vaccineManager.updated.connect(excel1.reloadExcel)
        vaccineManager.updated.connect(excel2.reloadExcel)
        vaccineManager.updated.connect(excel3.reloadExcel)
