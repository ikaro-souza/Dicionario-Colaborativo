import socket
import json
import communication


def line(size, symbol='-'):
    return symbol * size


class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.request = communication.CLIENT_REQUEST
        self.server_host = communication.SERVER_HOST
        self.port = communication.PORT
        self.server_response = communication.SERVER_RESPONSE

    def send_request(self):
        # Guarda a string do pedido serializado
        request_json = json.dumps(self.request)
        self.socket.sendto(request_json.encode(communication.ENCODING), (self.server_host, self.port))

    def get_server_response(self):
        # Verifica se o comando é mostrar_dicionário
        if self.request['command'] != communication.COMMANDS[3]:
            try:
                data, server_address = self.socket.recvfrom(communication.MAX_BYTES)
                server_response = json.loads(data.decode(communication.ENCODING))
            except ConnectionError:
                server_response = communication.SERVER_RESPONSE
                server_response['message'] = 'Sem resposta do servidor.'
        else:
            server_response = communication.SERVER_RESPONSE

            # Transforma o resultado da resposta em uma lista que irá conter os
            # objetos JSON que contêm uma palavra e seu significado
            server_response['results'] = []

            while True:
                try:
                    data, server_address = self.socket.recvfrom(communication.MAX_BYTES)

                    # Guarda a resposta desserializada do servidor
                    response = json.loads(data.decode(communication.ENCODING))

                    # Sai do looping caso o servidor não tenha enviado uma palavra
                    if response['results'] is None or response['results'] == '':
                        # Guarda a mensagem da resposta do servidor
                        server_response['message'] = response['message']
                        break
                    else:
                        # Adiciona ao resultado final, o resultado desserializado da resposta  do servidor
                        server_response['results'].append(json.loads(response['results']))
                except ConnectionError:
                    server_response = communication.SERVER_RESPONSE
                    server_response['message'] = 'Sem resposta do servidor.'
            
        self.server_response = server_response

    def show_server_message(self):
        print('{}\n{}\n{}'.format(line(50, '*'), self.server_response['message'], line(50, '*')))


if __name__ == '__main__':
    c = Client()
