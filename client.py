from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver
import sys
from PyQt5 import QtWidgets
from interface import interface


class Connection1(LineOnlyReceiver):
    factory: 'Connection'

    def connectionMade(self):
        self.factory.window.protocol = self

    def lineReceived(self, line: bytes):
        text = line.decode()
        self.factory.window.plainTextEdit.appendPlainText(text)


class Connection(ClientFactory):
    window: 'ChatWindow'
    protocol = Connection1

    def __init__(self, window):
        self.window = window


class Chat(QtWidgets.QMainWindow, interface.Ui_MainWindow):
    protocol: Connection1
    reactor = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button()

    def button(self):
        self.pushButton.clicked.connect(self.sending)

    def sending(self):
        text = self.lineEdit.text()

        self.protocol.sendLine(text.encode())
        self.lineEdit.clear()


app = QtWidgets.QApplication(sys.argv)

import qt5reactor

chat = Chat()
chat.show()
qt5reactor.install()

from twisted.internet import reactor

chat.reactor = reactor
reactor.connectTCP('localhost', 1111, Connection(chat))
reactor.run()
