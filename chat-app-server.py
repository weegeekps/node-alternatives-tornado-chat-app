from tornado.ioloop import IOLoop
from tornado.web import Application, url
from tornado.websocket import WebSocketHandler
import json


connectedClients = []


class ChatServerHandler(WebSocketHandler):

    __client_index = -1
    client_name = u'unset'

    @staticmethod
    def __send_message(sender, message):
        payload = {
            u'message': {
                u'message': message,
                u'sender': sender,
            }
        }

        serialized_payload = json.dumps(payload)

        for client in connectedClients:
            client.write_message(serialized_payload)

    def check_origin(self, origin):
        return True

    def open(self, *args):
        connectedClients.append(self)

        self.__client_index = connectedClients.index(self)
        self.client_name = u'user{0}'.format(self.__client_index)

        print 'Connection opened from {0}.'.format(self.request.remote_ip)

        self.__send_message(
            sender= u'Server',
            message= u'{0} has connected.'.format(self.client_name),
        )

    def on_message(self, message):
        print 'Message received from {0}'.format(self.client_name)

        if not isinstance(message, unicode):
            print 'Message from {0} not unicode.'.format(self.client_name)
            return

        self.__send_message(self.client_name, message)

    def on_close(self):
        connectedClients.remove(self)

        self.__send_message(
            sender= u'Server',
            message= u'{0} has disconnected.'.format(self.client_name),
        )


def make_app():
    settings = {
        'xsrf_cookies': False,
    }

    return Application([
        url(r'/', ChatServerHandler),
    ], **settings)

def main():
    app = make_app()
    app.listen(8001)
    IOLoop.instance().start()

main()
