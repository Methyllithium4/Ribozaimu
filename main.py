import sys
import os

os.environ["DESKTOP_STARTUP_ID"] = "Zaimu-chan"
os.environ["RESOURCE_NAME"] = "zaimu-chan"
os.environ["RESOURCE_CLASS"] = "Zaimu-chan"
os.environ["QT_WAYLAND_DISABLE_WINDOWDECORATION"] = "1"
from setproctitle import setproctitle

setproctitle("Zaimu-chan")
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from assistant import AssistantWindow

app = QApplication(sys.argv)

app.setApplicationName("zaimu-chan")
app.setApplicationDisplayName("zaimu-chan")
app.setOrganizationName("zaimu-chan")
app.setWindowIcon(QIcon("assets/icon.png"))
app.setDesktopFileName("zaimu-chan")

window = AssistantWindow()

window.setWindowTitle("zaimu-chan")

sys.exit(app.exec())

