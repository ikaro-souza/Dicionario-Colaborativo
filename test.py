import Client
import communication
import json
import random
import threading
import argparse

# Guarda a lista de palavras aleatórias
words = json.load(open('random_words.json'))


def run_client_thread():
    client = Client.Client()
    # Escolhe um comando aleatório
    command = random.choice(communication.COMMANDS)
    client.request['command'] = command

    # print('\n{thread}: executando o comando {cmd}\n'.format(thread=threading.current_thread().name,
    #                                                         cmd=command))

    # Caso seja o camando adicionar_palavra
    if command == communication.COMMANDS[0]:
        # Escolhe uma palavra aleatória
        client.request['word'] = random.choice(words)
        # Escolhe outra palavra aleatória para ser o significado
        client.request['meaning'] = random.choice(words)

    # Caso seja o comando remover_palavra
    elif command == communication.COMMANDS[1]:
        # Escolhe uma palavra aleatória para ser removida
        client.request['word'] = random.choice(words)

    # Caso seja o comando buscar_palavra
    elif command == communication.COMMANDS[2]:
        # Escolhe uma palavra aleatória para ser buscada
        client.request['word'] = random.choice(words)

    # Envia o pedido ao cliente
    client.send_request()
    # Guarda a resposta do servidor
    client.get_server_response()
    # Exibe o resultado
    print(client.server_response)


# Roda os testes dos clientes
def run_test(clients_amount):
    for i in range(clients_amount):
        c_thread = threading.Thread(target=run_client_thread)
        c_thread.start()
        c_thread.join()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, default=0)
    args = parser.parse_args()

    if args.n != 0:
        num_clients = args.n
    else:
        num_clients = 1200

    run_test(num_clients)
