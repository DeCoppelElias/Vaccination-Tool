from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class WarningDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WARNING!")

        QBtn = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel("Warning! The advice from this tool may differ from the current guidelines. \n"
                         "Always check whether the advice from this tool is correct using the most recent package "
                         "leaflets and VWVJ/HGR guidelines.")
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
