import communication
import tkinter as tk
from tkinter import ttk

commands = {
    'Adicionar palavra': communication.COMMANDS[0],
    'Remover palavra': communication.COMMANDS[1],
    'Buscar palavra': communication.COMMANDS[2],
    'Exibir dicionario': communication.COMMANDS[3]
}


class Window(tk.Tk):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.current_command = ''

        self.title('Dicionline')

        self.wordStringVar = tk.StringVar()
        self.meaningStringVar = tk.StringVar()

        self.wordStringVar.trace_add('write', self.entry_changed)
        self.meaningStringVar.trace_add('write', self.entry_changed)

        self.formFrame = tk.Frame(master=self)
        self.formLabelsFrame = tk.Frame(master=self.formFrame)
        self.formEntriesFrame = tk.Frame(master=self.formFrame)
        self.formButtonFrame = tk.Frame(master=self.formFrame)
        self.serverResponseFrame = tk.Frame(master=self)

        self.serverResponseScroll = tk.Scrollbar(master=self.serverResponseFrame, orient=tk.VERTICAL)
        self.serverResponseText = tk.Text(master=self.serverResponseFrame, width=70,
                                          bg='white', yscrollcommand=self.serverResponseScroll.set)
        self.serverResponseScroll.configure(command=self.serverResponseText.yview)

        self.optionsLabel = ttk.Label(master=self.formLabelsFrame, text='Opções:')
        self.wordLabel = ttk.Label(master=self.formLabelsFrame, text='Palavra:')
        self.meaningLabel = ttk.Label(master=self.formLabelsFrame, text='Significado:')
        self.commandsComboBox = ttk.Combobox(master=self.formEntriesFrame, state='readonly')
        self.commandsComboBox.bind('<<ComboboxSelected>>', self.new_command_selected)
        self.commandsComboBox['values'] = self.load_commands()
        self.wordEntry = ttk.Entry(master=self.formEntriesFrame, state='disabled',
                                   textvariable=self.wordStringVar)

        self.meaningEntry = ttk.Entry(master=self.formEntriesFrame, state='disabled',
                                      textvariable=self.meaningStringVar)

        self.sendButton = ttk.Button(master=self.formButtonFrame, text='Enviar',
                                     command=self.send_request, state='disabled')

        self.formFrame.pack(fill=tk.X)
        self.serverResponseFrame.pack(fill=tk.BOTH)

        self.formLabelsFrame.grid(row=0, column=0, pady=5, sticky=tk.W)
        self.formEntriesFrame.grid(row=0, column=1, pady=5, sticky=tk.E)
        self.formButtonFrame.grid(row=1, column=1, columnspan=2, pady=5, sticky=tk.E)

        self.optionsLabel.pack(fill=tk.BOTH, expand=True)
        self.wordLabel.pack(fill=tk.BOTH, expand=True)
        self.meaningLabel.pack(fill=tk.BOTH, expand=True)
        self.commandsComboBox.pack(fill=tk.X, expand=True)
        self.wordEntry.pack(fill=tk.X, expand=True)
        self.meaningEntry.pack(fill=tk.X, expand=True)
        self.sendButton.pack(side=tk.RIGHT, expand=True)
        self.serverResponseText.pack(side=tk.LEFT, expand=True)
        self.serverResponseScroll.pack(side=tk.RIGHT, fill=tk.Y, expand=True)

        self.width = self.serverResponseText.winfo_reqwidth() + self.serverResponseScroll.winfo_reqwidth()
        self.height = 500
        self.geometry('{}x{}'.format(self.width, self.height))

        self.resize_widgets()

    def resize_widgets(self):
        self.formFrame.configure(padx=self.width * 0.2, height=self.height * 0.2)
        self.serverResponseFrame.configure(height=self.height * 0.8)
        self.serverResponseText.configure(height=self.height * 0.8)
        self.formLabelsFrame.configure(padx=self.width*0.05)
        self.formEntriesFrame.configure(padx=self.width*0.05)
        self.formButtonFrame.configure(padx=self.width*0.05)

    def load_commands(self):
        result = []

        for command in commands.keys():
            result.append(command)

        return result

    def new_command_selected(self, event):
        self.current_command = commands[self.commandsComboBox.get()]
        self.controller.change_command()
        self.wordStringVar.set('')
        self.meaningStringVar.set('')

        if self.current_command == communication.COMMANDS[0]:
            self.wordEntry['state'] = 'normal'
            self.meaningEntry['state'] = 'normal'
        elif self.current_command == communication.COMMANDS[1] or self.current_command == communication.COMMANDS[2]:
            self.wordEntry['state'] = 'normal'
            self.meaningEntry['state'] = 'disabled'
        else:
            self.wordEntry['state'] = 'disabled'
            self.meaningEntry['state'] = 'disabled'

    def entry_changed(self, *args):
        if self.current_command == communication.COMMANDS[0]:
            if self.wordStringVar.get() != '' and self.meaningStringVar.get() != '':
                self.sendButton['state'] = 'normal'
            else:
                self.sendButton['state'] = 'disabled'

        elif self.current_command == communication.COMMANDS[1] or self.current_command == communication.COMMANDS[2]:
            if self.wordStringVar.get() != '':
                self.sendButton['state'] = 'normal'
            else:
                self.sendButton['state'] = 'disabled'

    def send_request(self, event=None):
        self.controller.send_request()
        self.show_server_response()

    def show_server_response(self):
        self.serverResponseText.delete('1.0', tk.END)
        response = self.controller.get_server_response()
        print(response)

        if isinstance(response['results'], list):
            for item in response['results']:
                self.serverResponseText.insert(tk.END, '{}\nSignificado: {}\n\n'.format(item['word'].upper(),
                                                                                        item['meaning']))
        else:
            if isinstance(response['results'], str):
                self.serverResponseText.insert(tk.INSERT,response['results'])
            else:
                self.serverResponseText.insert(tk.INSERT, response['message'])
