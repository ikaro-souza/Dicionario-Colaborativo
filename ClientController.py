import Client
import ClientUI
import communication


class ClientController:
    def __init__(self):
        self.client = Client.Client()
        self.gui = ClientUI.Window(controller=self)
        self.gui.mainloop()

    def change_command(self):
        self.client.request['command'] = self.gui.current_command

    def send_request(self):
        cmd = self.client.request['command']

        if cmd == communication.COMMANDS[0]:
            self.client.request['word'] = self.gui.wordEntry.get()
            self.client.request['meaning'] = self.gui.meaningEntry.get()

        elif cmd == communication.COMMANDS[1]:
            self.client.request['word'] = self.gui.wordEntry.get()

        elif cmd == communication.COMMANDS[2]:
            self.client.request['word'] = self.gui.wordEntry.get()

        self.client.send_request()
        self.client.get_server_response()

    def get_server_response(self):
        return self.client.server_response


if __name__ == '__main__':
    controller = ClientController()
