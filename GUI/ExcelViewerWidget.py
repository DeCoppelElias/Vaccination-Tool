import os
import pandas as pd
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QTableWidget, QStackedLayout, QVBoxLayout, \
    QTableWidgetItem


class ExcelViewerWidget(QWidget):
    def __init__(self, general_path, file_name, explanation):
        super().__init__()
        self.excel_path = os.path.abspath(os.path.join(general_path, file_name))

        info_label = QLabel(explanation + self.excel_path)

        reload_button = QPushButton("Reload Excel")
        reload_button.clicked.connect(self.reloadExcel)
        reload_button.setFixedSize(QSize(100, 30))

        info_container = QHBoxLayout()
        info_container.addWidget(info_label)
        info_container.addWidget(reload_button)

        self.excel_table = QTableWidget()
        self.stack_layout = QStackedLayout()
        self.stack_layout.addWidget(self.excel_table)
        self.stack_layout.addWidget(QLabel("MISSING"))
        self.reloadExcel()

        layout = QVBoxLayout()
        layout.addLayout(info_container)
        layout.addLayout(self.stack_layout)

        self.setLayout(layout)

    def reloadExcel(self):
        if os.path.isfile(self.excel_path):
            df = pd.read_excel(self.excel_path)

            # Set the row and column count based on the DataFrame
            self.excel_table.setRowCount(len(df))
            self.excel_table.setColumnCount(len(df.columns))
            self.excel_table.setHorizontalHeaderLabels(df.columns)

            # Populate the table with data from the DataFrame
            for row in range(len(df)):
                for col in range(len(df.columns)):
                    value = str(df.iloc[row, col])
                    self.excel_table.setItem(row, col, QTableWidgetItem(value))

            self.excel_table.resizeColumnsToContents()
            self.stack_layout.setCurrentIndex(0)
        else:
            self.stack_layout.setCurrentIndex(1)