from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QDialog


class ActionsWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()

        view_vaccines = QPushButton("View vaccines")
        view_vaccines.clicked.connect(main_window.toViewVaccines)
        view_vaccines.setFixedSize(QSize(100, 30))

        view_illnesses = QPushButton("View Illnesses")
        view_illnesses.clicked.connect(main_window.toViewIllnesses)
        view_illnesses.setFixedSize(QSize(100, 30))

        check_vaccines = QPushButton("Check vaccines")
        check_vaccines.clicked.connect(main_window.toCheckVaccines)
        check_vaccines.setFixedSize(QSize(100, 30))

        layout = QVBoxLayout()
        layout.addWidget(view_vaccines)
        layout.addWidget(view_illnesses)
        layout.addWidget(check_vaccines)

        self.setLayout(layout)