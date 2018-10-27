SERVER_HOST = 'localhost'   # Host padrão do servidor
PORT = 8000                 # Porta padrão
MAX_BYTES = 64000           # Número maximo de bytes que podem ser enviados pela rede
ENCODING = 'utf-8'          # Codificação padrão

# Lista de comandos permitidos
COMMANDS = [
    'ADD_WORD',
    'RMV_WORD',
    'SRC_WORD',
    'SHOW_ALL'
]

# Lista de resultados das exuções dos comandos
RESULTS = {
    'ADD_SUCCESS': 'Palavra adicionada com sucesso.',
    'ADD_FAIL': 'A palavra já está no dicionário.',
    'REM_SUCCESS': 'Palavra removida com sucesso.',
    'REM_FAIL': 'A palavra não está no dicionário.',
    'SRC_SUCCESS': 'Palavra encontrada.',
    'SRC_FAIL': 'Palavra não encontrada',
    'SHOW_SUCCESS': 'Dicionário enviado com sucesso.',
    'SHOW_ERROR': 'Erro ao tentar enviar dados ao cliente.',
    'DICT_EMPTY': 'Dicionário vazio.',
    'INVALID_CMD': 'Comando inválido.'
}

# Objeto JSON que define o padrão de respostas do servidor
SERVER_RESPONSE = {
    # Resultado da execução de pedido
    'results': None,
    # Mensagem informando sobre a execução do pedido
    'message': ''
}

# Objeto JSON que define o padrão de pedidos do cliente
CLIENT_REQUEST = {
    # Comando que o servidor deverá executar
    'command': '',
    # A palavra que será adicionada/removida/buscada
    'word': None,
    # Significado da palavra que será adicionada
    'meaning': None
}
