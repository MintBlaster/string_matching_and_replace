import sys
from PyQt5.QtWidgets import QApplication
from ui import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(open("styles.qss").read())  # Load styles from QSS file
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())