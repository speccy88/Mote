#! /usr/bin/python
from PyQt4 import QtGui, QtCore
from client import MoteClient
import sys, time

TERMINAL_GREEN = "#7FFF00"
ERROR_RED = "#FF0000"
RESPONSE_BLUE = "#1CA4FF"
ADDRESSES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Viewer(QtGui.QWidget):
    
    def __init__(self, id_):
        super(Viewer, self).__init__()
        
        self.id_ = id_
        self.init()
        
    def init(self):
        self.address = ADDRESSES[self.id_]
        font1 = QtGui.QFont("Ubuntu", 12, QtGui.QFont.Bold)
        title = QtGui.QLabel("Mote "+self.address)
        title.setFont(font1)
        send = QtGui.QPushButton("Send")
        self.cmd = QtGui.QLineEdit()
        font2 = QtGui.QFont("Monospace", 10, QtGui.QFont.Bold)
        col = QtGui.QColor(TERMINAL_GREEN)
        self.display = QtGui.QTextEdit()
        self.display.setFont(font2)
        self.display.setStyleSheet("QTextEdit {background-color: black}")
        self.display.setReadOnly(True)

        send.clicked.connect(self.Send)

        h0 = QtGui.QHBoxLayout()
        h0.addStretch(1)
        h0.addWidget(title)
        h0.addStretch(1)
        v = QtGui.QVBoxLayout()
        v.addLayout(h0)
        h = QtGui.QHBoxLayout()
        h.addWidget(self.cmd)
        h.addWidget(send)
        v.addLayout(h)
        v.addWidget(self.display)

        self.setLayout(v) 
        
    def Send(self):
        c = MoteClient("192.168.0.198")
        cmd = str(self.cmd.text())
        self.cmd.clear()
        if cmd[0] == "!":
            self.Write(cmd)
            c.Store(self.address, cmd[1:])
        elif cmd[0] == "@":
            self.Write(cmd)
            resp = c.Fetch(self.address, cmd[1:])
            self.Write(resp, color=RESPONSE_BLUE)
        else:
            self.Write("Command should be Fetch(@) or Store(!)", color=ERROR_RED)
        c.Close()

    def Write(self, msg, color=TERMINAL_GREEN):
        self.display.setColor(QtGui.QColor(color))
        self.display.append(msg)
 
class Main(QtGui.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.init()
        
    def init(self):
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)    
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        self.statusBar().showMessage("Status")

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        pos = [(i,j) for i in range(1) for j in range(4)]
        grid = QtGui.QGridLayout()
        self.viewers = []        
       
        for index, coord in enumerate(pos):
            view = Viewer(index+1)
            self.viewers.append(view)
            grid.addWidget(view, coord[0] ,coord[1])
            
        w = QtGui.QWidget() 
        w.setLayout(grid)

        self.setCentralWidget(w)
        #self.setGeometry(400, 100, 500, 600)
        self.setWindowTitle('Mote Network Debugger')    
        self.show()

    def add(self, text):
        for i, viewer in enumerate(self.viewers):
            viewer.display.append(text+" "+str(i+1))

class SerialThread(QtCore.QThread):
    def run(self):
        count = 0
        while count < 15:
            time.sleep(0.05)
            self.emit( QtCore.SIGNAL('update(QString)'), "emit"+str(count))
            count += 1
       
app = QtGui.QApplication(sys.argv)
#thread = SerialThread()
ex = Main()
#ex.connect(thread, QtCore.SIGNAL('update(QString)'), ex.add)
#thread.start()
sys.exit(app.exec_())
