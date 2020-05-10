# для подключения через терминал или консоль: telnet 127.0.0.1 1234

from twisted.internet import reactor
from twisted.internet.protocol import connectionDone, ServerFactory
from twisted.protocols.basic import LineOnlyReceiver


class ServerMessages(LineOnlyReceiver):
    factory: 'Server'
    nickname: str = None

    def connectionMade(self):
        self.factory.users.append(self)

    def connectionLost(self, reason=connectionDone):
        self.factory.users.remove(self)

    def lineReceived(self, line: bytes):
        content = line.decode()

        if self.nickname is not None:
            content = self.nickname + ': ' + content

            for person in self.factory.users:
                person.sendLine(content.encode())
        else:
            self.nickname = content
            self.sendLine('Добро пожаловать'.encode())


class ServerStarter(ServerFactory):
    protocol = ServerMessages
    users: list

    def startFactory(self):
        self.users = []
        print('Сервер работает')

    def stopFactory(self):
        print('Сервер остановлен')


reactor.listenTCP(1111, ServerStarter())
reactor.run()
