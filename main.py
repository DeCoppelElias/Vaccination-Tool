import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication
from GUI.MainWindow import MainWindow
from VaccineManager.VaccineManager import VaccineManager

# Init vaccines (read excel files)
vaccineManager = VaccineManager()

# Start GUI app
app = QApplication(sys.argv)

window = MainWindow(vaccineManager)
window.show()
app.exec()
