import sys
import pair
import connect
import devices
from PySide6.QtWidgets import(
        QApplication,
        QMainWindow,
        QWidget,
        QHBoxLayout,
        QVBoxLayout,
        QGridLayout,
        QPushButton,
        QSizePolicy,
        QFrame,
        QLabel,
        QScrollArea,
        QLineEdit,
        QDialog
)
from PySide6.QtCore import(
        Qt
        )
class MainWindow(QMainWindow):
    def __init__(self):
            #Main Window
            super().__init__()
            #self.setWindowFlags(Qt.WindowType.FramelessWindowHint) #Remove Default Titlebar
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            self.setWindowTitle("Dassh")
            self.resize(960, 540)
            self.setMinimumSize(960, 540)
            central = QWidget()
            central.setObjectName("center")
            central.setStyleSheet("""
                QWidget#center{
                    background-color: #000000;
                    border: none;
                    border-radius: 31.5px;
                }
                                  """)
            self.setCentralWidget(central)
            outerLay = QVBoxLayout(central)
            mLay = QHBoxLayout()
            #mLay.setContentsMargins(8, 8, 8, 8)
            mLay.setSpacing(8)
            self.setStyleSheet("""
                               QMainWindow{
                                background-color: #000000;
                                border-radius: 30px;
                               }
                           """)

            '''
            #titleBar
            titleBar = QWidget()
            titleLay = QHBoxLayout(titleBar)
            titleLay.setSpacing(10)
            wtitle = QLabel("Dassh")
            titleLay.addWidget(wtitle)
            titleLay.addStretch()
            clsw = QPushButton("x")
            clsw.clicked.connect(self.close)
            minw = QPushButton("-")
            minw.clicked.connect(self.showMinimized)
            maxw = QPushButton("+")
            maxw.clicked.connect(self.showMaximized)
            for widget in(minw, maxw, clsw):
                titleLay.addWidget(widget)
            titleBar.setStyleSheet("""
                QPushButton{
                    padding: 10px;
                    border-radius: 15px;
                    border: none;
                }
                QPushButton:hover{
                    background: #262626;
                    border-radius: 50px;
                }
                QPushButton:pressed{
                    background: #737373;
                    border-radius: 50px;
                }

                                """)
            outerLay.addWidget(titleBar)
           '''
            outerLay.addLayout(mLay)


            
            #SideBar
            sidebar = QFrame()
            sidebar.setObjectName("sidebar")
            sidebar.setStyleSheet("""
                                  QFrame#sidebar{
                                    background-color: #171717;
                                    border: 1px solid #404040;
                                    border-radius: 22.5px;
                                  }
                            """)
            sidebar.setFrameShape(QFrame.Shape.NoFrame)
            sidebarLay = QVBoxLayout(sidebar)
            sidebar.setMinimumWidth(160)
            sidebar.setMaximumWidth(180)
            sidebar.setFixedWidth(170)
            sidebarLay.setContentsMargins(2, 2, 2, 2)
            sidebarLay.setSpacing(12)
            mLay.addWidget(sidebar)
            mLay.addStretch()
            
            #Devices
            devicelist = QFrame()
            #devicelist.setMaximumHeight(210)
            #devicelist.setMinimumHeight(200)
            #devicelist.setFixedHeight(100)
            devicelist.setObjectName("Devices")
            deviceLay = QVBoxLayout(devicelist)
            deviceHeader = QHBoxLayout()
            deviceTitle = QLabel("Devices")
            addButton = QPushButton("+")
            addButton.clicked.connect(Dialogs.AddDialog)
            deviceHeader.addWidget(deviceTitle)
            deviceHeader.addStretch()
            deviceHeader.addWidget(addButton)
            deviceLay.addLayout(deviceHeader)
            devicelist.setStyleSheet("""
                QFrame#Devices{
                        border-radius: 15px;
                }
                QPushButton{
                        padding: 10px;
                        border-radius: 12px;
                        border: none;                                            
                        font-size: 15px;
                }
                QPushButton:hover{
                        background-color: #262626;
                        color: white;
                }
                QPushButton:pressed{
                        background-color: #737373;
                        color: white;
                }
            """)
            sidebarLay.addWidget(devicelist)
            devicelist.setSizePolicy(
                    QSizePolicy.Policy.Expanding,
                    QSizePolicy.Policy.Preferred
            )
            data = devices.load()
            device_list = data["devices"]
            for device in device_list:
                button = QPushButton(device["host"])
                button.clicked.connect(
                    lambda checked = False, d=device: ConnectDevice(d)
                )
                deviceLay.addWidget(button)
            deviceLay.addStretch()
            def ConnectDevice(device):
                self.connection = connect.Connect()
                self.connection.connect(device)

            #Stats
            sidebarLay.setContentsMargins(5, 0, 5, 5)
            stats = QWidget()
            stats.setObjectName("stats")
            sidebarLay.addWidget(stats)
            statsLay = QVBoxLayout(stats)
            statsHeader = QLabel("Stats")
            HeaderLay = QHBoxLayout()
            statsLay.addLayout(HeaderLay)
            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            HeaderLay.addWidget(statsHeader)
            HeaderLay.setContentsMargins(5, 5, 0, 0)
            statsLay.addWidget(line)
            stats.setStyleSheet("""
                QWidget#stats{
                    background-color: #000000;
                    border: 1px solid #767676;
                    border-radius: 17.5px;
                    padding: 10px;
                }
                                """)
            statsLay.addStretch()
            #statsLay.setContentsMargins(15, 10, 0, 0)
            
            
class Dialogs:
    @staticmethod
    def AddDialog():
            pairDialog = QDialog()
            dialogHeader = QLabel("Add Device")
            dialogHeaderLay = QHBoxLayout()
            dialogHeaderLay.addWidget(dialogHeader)
            cancelButton = QPushButton("X")
            cancelButton.clicked.connect(pairDialog.reject)
            dialogHeaderLay.addWidget(cancelButton)
            dialogLay = QVBoxLayout(pairDialog)
            dialogLay.addLayout(dialogHeaderLay)

            getHost = QLineEdit()
            getHost.setPlaceholderText("Enter Your IP/Hostname")
            dialogLay.addWidget(getHost)

            getUsr = QLineEdit()
            getUsr.setPlaceholderText("Enter Your Username")
            dialogLay.addWidget(getUsr)
                    
            getPort = QLineEdit()
            getPort.setPlaceholderText("Enter Your Port")
            dialogLay.addWidget(getPort)
                     
            addButton = QPushButton("Add")
            dialogLay.addWidget(addButton)
            addButton.clicked.connect(
                lambda: pair.pair(
                    getPort.text(), 
                    getUsr.text(), 
                    getHost.text()
                    )
                )
            pairDialog.exec()


            


    





def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
if __name__=="__main__":
    main()

