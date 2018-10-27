import argparse
from MultithreadingServer import MultithreadingServer


if __name__ == '__main__':

    argparser = argparse.ArgumentParser()
    argparser.add_argument('-max', type=int)

    args = argparser.parse_args()

    if args.max != 0:
        max_clients = args.max
    else:
        max_clients = 700
    
    server = MultithreadingServer(max_clients)
    server.run_server()
