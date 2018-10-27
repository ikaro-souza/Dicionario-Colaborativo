import socket
import threading
import json
import communication as communication
import time

'''
    Classe que implementa um servidor com capacidade de aceitar e responder 
    pedidos simultaneos de clientes
'''


class MultithreadingServer:
    def __init__(self, max_clients, server_socket=None, host=communication.SERVER_HOST, port=communication.PORT):
        if server_socket is None:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.server_socket = server_socket

        self.host = host
        self.port = port
        self.dict_file = 'dictionary.json'
        self.max_clients = max_clients
        self.current_clients = 0
        self.current_request = communication.CLIENT_REQUEST
        self.current_client_address = ()

    # Salva as atualizações feitas ao dicionário e cria o arquivo do dicionário caso ele não exista
    def save_dict(self, dictionary=None):
        if dictionary is None:
            dictionary = {'words': {}}

        try:
            with open(self.dict_file, 'w') as f:
                json.dump(dictionary, f, indent=2, sort_keys=True)
                f.close()
        except (FileNotFoundError or TypeError) as err:
            return err

    # Desserializa o dicionário para ser usado no programa, também serve para garantir que o
    # arquivo do dicionário seja criado antes do servidor começar a aceitar pedidos, chamando
    # a função save_dict()
    def load_dict(self):
        # self.file_in_use = True

        try:
            with open(self.dict_file, 'r') as f:
                dictionary = json.load(f)
                f.close()
                return dictionary
        except FileNotFoundError:
            print('\tArquivo inexistente.')
            print('\tCriando o arquivo.')
            self.save_dict()
            self.load_dict()
            print('\tArquivo criado com sucesso.')

    # Adiciona uma nova palavra ao dicionário
    def add_word(self):

        # Guarda o dicionário na variável dictionary
        dictionary = self.load_dict()

        # Cria uma server_response padrão
        result = communication.SERVER_RESPONSE

        # Verifica se a palavra enviada pelo cliente já está presente no dicionário
        if self.current_request['word'] not in dictionary['words'].keys():
            # Adiciona a palavra e seu significado ao dicionário
            dictionary['words'][self.current_request['word']] = self.current_request['meaning']

            self.save_dict(dictionary)

            # Modifica a mensagem da resposta do servidor para informar que a palavra foi adicionada
            result['message'] = communication.RESULTS['ADD_SUCCESS']
        else:
            # Modifica a mensagem da resposta do servidor para informar que a palavra ja estava no dicionário
            result['message'] = communication.RESULTS['ADD_FAIL']

        result['results'] = None
        return result
    
    def remove_word(self):
        dictionary = self.load_dict()
        result = communication.SERVER_RESPONSE

        # Verifica se a palavra enviada pelo cliente ja se encontra no dicionário
        if self.current_request['word'] in dictionary['words'].keys():
            # Remove a palavra
            dictionary['words'].pop(self.current_request['word'])

            self.save_dict(dictionary)

            # Modifica a mensagem da resposta do servidor para informar que a palavra foi removida
            result['message'] = communication.RESULTS['REM_SUCCESS']
        else:
            # Modifica a mensagem da resposta do servidor para informar que a palavra estava no dicionário
            result['message'] = communication.RESULTS['REM_FAIL']

        result['results'] = None
        return result

    def search_word(self):
        dictionary = self.load_dict()
        result = communication.SERVER_RESPONSE

        # Verifica se a palavra enviada pelo cliente ja se encontra no dicionário
        if self.current_request['word'] in dictionary['words'].keys():
            # Modifica o resultado da resposta do servidor para uma string
            # com a palavra e seu significado
            result['results'] = 'Palavra: {}\nSignificado: {}'.format(self.current_request['word'],
                                                                      dictionary['words'][self.current_request['word']])
        else:
            result['results'] = None
            # Modifica a mensagem para informar que a palavra não foi encontrada
            result['message'] = communication.RESULTS['SRC_FAIL']

        return result

    def show_all(self):
        dictionary = self.load_dict()
        result = communication.SERVER_RESPONSE

        # Verifica se o dicionário está vazio
        if len(dictionary['words']) == 0:
            # Modifica a mensagem da resposta do servidor para informar que o dicionário está vazio
            result['message'] = communication.RESULTS['DICT_EMPTY']
            return result
        else:
            # Envia cada palavra do dicionário
            for word in dictionary['words']:
                # Dicionário(Python) contendo a palavra e seu significado
                data = {
                    'word': word,
                    'meaning': dictionary['words'][word]
                }

                # Serializa a variavel data em um objeto json e guarda uma string representando
                # o objeto json no resultado da resposta do servidor
                result['results'] = json.dumps(data)

                result_json = json.dumps(result)

                try:
                    print('\tEnviando palavra ao cliente.....')
                    self.server_socket.sendto(result_json.encode(communication.ENCODING),
                                              self.current_client_address)
                    print('\tPalavra enviada com sucesso.')
                except Exception:
                    result['results'] = None
                    result['message'] = communication.RESULTS['SHOW_ERROR']
                    return result

            result['results'] = None
            result['message'] = communication.RESULTS['SHOW_SUCCESS']
            return result

    # Executa o pedido do cliente em um novo thread
    def start_client_thread(self):
        # Guarda o momento em que o thread começou a ser executado
        thread_start_time = time.clock()
        # Guarda o nome do thread
        current_thread_name = threading.current_thread().name

        print('Executando no thread {}'.format(current_thread_name))
        print('Requisito recebido de {}'.format(self.current_client_address))
        print('Decodificando e desserializando requisito.....')

        comando = self.current_request['command']
        # Caso o comando seja adicionar_palavra
        if comando == communication.COMMANDS[0]:
            print('{thread}: Cliente requisitou a adição da palavra {}'.format(self.current_request['word'], 
                                                                               thread=current_thread_name))
            result = self.add_word()
            print('{thread}: {}'.format(result['message'], thread=current_thread_name))

        # Caso o comando seja remover_palavra
        elif comando == communication.COMMANDS[1]:
            print('{thread}: Cliente requisitou a remoção da palavra {}'.format(self.current_request['word'], 
                                                                                thread=current_thread_name))
            result = self.remove_word()
            # self.file_in_use = False
            print('{thread}: {}'.format(result['message'], thread=current_thread_name))

        # Caso o comando seja buscar_palavra
        elif comando == communication.COMMANDS[2]:
            print('{thread}: Cliente requisitou a busca da palavra {}'.format(self.current_request['word'],
                                                                              thread=current_thread_name))
            result = self.search_word()
            print('{thread}: {}'.format(result['message'], thread=current_thread_name))

        # Caso o comando seja mostrar_dicionário
        elif comando == communication.COMMANDS[3]:
            print('{thread}: Cliente requisitou a exibição de todo o dicionário.'.format(thread=current_thread_name))
            result = self.show_all()
            print('{thread}: {}'.format(result['message'], thread=current_thread_name))

        # Caso o comando seja inválido
        else:
            result = communication.SERVER_RESPONSE
            result['message'] = communication.RESULTS['INVALID_CMD']
            print('{thread}: {}'.format(result['message'], thread=current_thread_name))

        # Guarda a string do resultado serializado
        server_response = json.dumps(result).encode(communication.ENCODING)

        # Envia a resposta para o cliente
        self.server_socket.sendto(server_response, self.current_client_address)

        # Mostra por quanto tempo o thread foi executado
        print('{thread:} spent {time: .6f}'.format(thread=current_thread_name,
                                                   time=time.clock() - thread_start_time))

    def run_server(self):
        self.load_dict()
        self.server_socket.bind((self.host, self.port))

        while True:
            print('\nAguardando requisito de cliente.....\n')
            client_request, client_address = self.server_socket.recvfrom(communication.MAX_BYTES)
            self.current_clients += 1

            # Impede que o servidor responda mais clientes do que o limite permitido
            while self.current_clients == self.max_clients:
                pass

            # Desserializa o pedido do cliente
            self.current_request = json.loads(client_request.decode(communication.ENCODING))

            # Guarda o endereço do cliente
            self.current_client_address = client_address

            # Cria e inicia novo thread para o cliente
            new_client_thread = threading.Thread(target=self.start_client_thread)
            new_client_thread.start()
            new_client_thread.join()

            self.current_clients -= 1
