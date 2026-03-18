import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from android_tab import AndroidTab
from ios_tab import IOSTab
from windows_tab import WindowsTab
from macos_tab import MacOSTab
from device_search_window import DeviceSearchWindow

class SpywareFramework(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZeroClick Spyware Framework")
        self.setGeometry(100, 100, 800, 600)
        
        tabs = QTabWidget()
        tabs.addTab(AndroidTab(), "Android")
        tabs.addTab(IOSTab(), "iOS")
        tabs.addTab(WindowsTab(), "Windows")
        tabs.addTab(MacOSTab(), "macOS")
        self.setCentralWidget(tabs)


def show_main_window():
    main_window = SpywareFramework()
    main_window.show()
    return main_window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    search_window = DeviceSearchWindow()
    search_window.show()
    # Nach Zielauswahl kann show_main_window() aufgerufen werden
    sys.exit(app.exec_())