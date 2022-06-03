# Importações
import csv
import os
import tkinter as tk
from tkinter import messagebox as mbox
from filemanager import FileManager

# Arquivo de dados dos funcionários
FILESEDE = '/seet/dados/sededest.csv'

class SedeDest(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.fonte = ('Arial', 14, 'normal')
        tk.Label(self, text='Cadastro de Sedes/Destinatários', font=self.fonte).pack(pady=10)
        self.inputs = {}
        self.fields = []
        self.lastindex = 0

        # LabelFrame
        framefields = tk.LabelFrame(self, text=' Dados da sede ', fg='blue', font=self.fonte)
        framefields.pack()

        # Widgets
        tk.Label(framefields, text='Sede:', font=self.fonte).grid(row=0, column=0, sticky='W', padx=4, pady=10)
        self.sede = tk.StringVar()
        self.inputs['sede'] = self.sede
        self.entrysede = tk.Entry(framefields, textvariable=self.sede, width=40,
                                        font=self.fonte, justify='center')
        self.entrysede.grid(row=1, column=0, sticky='w', padx=4)
        self.fields.append(self.entrysede)

        tk.Label(framefields, text='Cidade:', font=self.fonte).grid(row=0, column=1, sticky='w', padx=4)
        self.cidade = tk.StringVar()
        self.inputs['cidade'] = self.cidade
        self.entrycidade = tk.Entry(framefields, textvariable=self.cidade, width=28,
                                    font=self.fonte, justify='center')
        self.entrycidade.grid(row=1, column=1, columnspan=2, sticky='w', padx=4)
        self.fields.append(self.entrycidade)

        tk.Label(framefields, text='Endereço:', font=self.fonte).grid(row=2, column=0, sticky='w', padx=4)
        self.endereco = tk.StringVar()
        self.inputs['endereco'] = self.endereco
        self.entryendereco = tk.Entry(framefields, textvariable=self.endereco, width=40,
                                          font=self.fonte, justify='center')
        self.entryendereco.grid(row=3, column=0, sticky='w', padx=4)
        self.fields.append(self.entryendereco)

        tk.Label(framefields, text='Número:', font=self.fonte).grid(row=2, column=1, sticky='w', padx=4)
        self.numero = tk.StringVar()
        self.inputs['numero'] = self.numero
        self.entrynumero = tk.Entry(framefields, textvariable=self.numero, width=7,
                                    font=self.fonte, justify='center')
        self.entrynumero.grid(row=3, column=1, sticky='w', padx=4)
        self.fields.append(self.entrynumero)

        tk.Label(framefields, text='Comp:', font=self.fonte).grid(row=2, column=2, sticky='w', padx=4)
        self.comp = tk.StringVar()
        self.inputs['comp'] = self.comp
        self.entrycomp = tk.Entry(framefields, textvariable=self.comp, width=20,
                                    font=self.fonte, justify='center')
        self.entrycomp.grid(row=3, column=2, sticky='w', padx=4)
        self.fields.append(self.entrycomp)

        tk.Label(framefields, text='Bairro:', font=self.fonte).grid(row=4, column=0, sticky='w', padx=4)
        self.bairro = tk.StringVar()
        self.inputs['bairro'] = self.bairro
        self.entrybairro = tk.Entry(framefields, textvariable=self.bairro, width=40,
                                    font=self.fonte, justify='center')
        self.entrybairro.grid(row=5, column=0, sticky='w', padx=4)
        self.fields.append(self.entrybairro)

        tk.Label(framefields, text='Estado:', font=self.fonte).grid(row=4, column=1, sticky='w', padx=4)
        self.estado = tk.StringVar()
        self.inputs['estado'] = self.estado
        self.entryestado = tk.Entry(framefields, textvariable=self.estado, width=7,
                                    font=self.fonte, justify='center')
        self.entryestado.grid(row=5, column=1, sticky='w', padx=4)
        self.fields.append(self.entryestado)

        tk.Label(framefields, text='Cep:', font=self.fonte).grid(row=4, column=2, sticky='w', padx=4)
        self.cep = tk.StringVar()
        self.inputs['cep'] = self.cep
        self.entrycep = tk.Entry(framefields, textvariable=self.cep,
                                    font=self.fonte, justify='center')
        self.entrycep.grid(row=5, column=2, sticky='w', padx=4, pady=10)
        self.fields.append(self.entrycep)

        framebuttons = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        framebuttons.pack(side='bottom', fill='x', pady=20)

        self.imganterior = tk.PhotoImage(file='/seet/images/anterior.png')
        self.btanterior = tk.Button(framebuttons, image=self.imganterior, command=self.anterior)
        self.btanterior.pack(padx=4, pady=10, side='left')

        self.imgproximo = tk.PhotoImage(file='/seet/images/proximo.png')
        self.btproximo = tk.Button(framebuttons, image=self.imgproximo, command=self.proximo)
        self.btproximo.pack(padx=4, side='left')

        self.imgnovo = tk.PhotoImage(file='/seet/images/novo.png')
        self.btnovo = tk.Button(framebuttons, image=self.imgnovo, command=self.novo)
        self.btnovo.pack(padx=4, side='left')

        self.imgeditar = tk.PhotoImage(file='/seet/images/editar.png')
        self.bteditar = tk.Button(framebuttons, image=self.imgeditar, command=self.editar)
        self.bteditar.pack(padx=4, side='left')

        self.imgexcluir = tk.PhotoImage(file='/seet/images/excluir.png')
        self.btexcluir = tk.Button(framebuttons, image=self.imgexcluir, command=self.excluir)
        self.btexcluir.pack(padx=4, side='left')

        self.imgsalvar = tk.PhotoImage(file='/seet/images/salvar.png')
        self.btsalvar = tk.Button(framebuttons, image=self.imgsalvar, command=self.salvar)
        self.btsalvar.pack(padx=4, side='left')

        self.imgvoltar = tk.PhotoImage(file='/seet/images/voltar.png')
        self.btvoltar = tk.Button(framebuttons, image=self.imgvoltar, command=self.voltar)
        self.btvoltar.pack(padx=4, side='right')

        self.carrega_dados_arquivo()

    # -----------------------------------------------------------------------------------------------
    # Métodos

    def disable_fields(self):
        for field in self.fields:
            field.configure(state='disable')


    def enable_fields(self):
        for field in self.fields:
            field.configure(state='normal')


    def carrega_dados_arquivo(self):
        ''' Verifica se existe o arquivo, caso não exista será criado
            Caso exista, carrega o ultimo registro e o exibe. '''
        self.registroslist = []
        existearq = os.path.exists(FILESEDE)
        dados = {}
        if not existearq:
            with open(FILESEDE, 'w') as file:
                writer = csv.DictWriter(file, fieldnames=self.inputs.keys(), lineterminator='\n')
                writer.writeheader()
        else:
            with open(FILESEDE, 'r') as file:
                reader = csv.DictReader(file, fieldnames=self.inputs.keys())
                for registros in reader:
                    for key, value in registros.items():
                        dados[key] = value
                    self.registroslist.append(dados)
                    dados = {}
        self.lastindex = (len(self.registroslist)-1)
        self.exibe(self.lastindex)
        self.disable_fields()

    def voltar(self):
        from seet import MainFrame
        self.master.switch_frame(MainFrame)


    def novo(self):
        for field in self.inputs:
            self.inputs[field].set('')
        self.enable_fields()
        self.entrysede.focus()
        self.btnovo.configure(state='disable')
        self.btsalvar.configure(state='normal')
        self.btexcluir.configure(state='disable')


    def get(self):
        '''Captura valores preenchidos dos campos'''
        dados = {}
        for key, value in self.inputs.items():
            if value.get() != '' or key == 'comp':
                dados[key] = value.get().upper()
        return dados


    def exibe(self, index):
        '''Exibe os dados através do índice passado.'''
        self.btsalvar.configure(state='disable')
        self.btnovo.configure(state='normal')
        self.bteditar.configure(state='normal')
        if index == 0:
            self.btanterior.configure(state='disable')
            self.btproximo.configure(state='disable')
            self.btexcluir.configure(state='disable')
            for key in self.inputs.keys():
                self.inputs[key].set('')

        if index >= 1:
            self.btexcluir.configure(state='normal')
            dados = self.registroslist[index]
            for key, value in dados.items():
                self.inputs[key].set(value)
            if index == 1:
                self.btanterior.configure(state='disable')
            if index == self.lastindex:
                self.btproximo.configure(state='disable')
            if index < len(self.registroslist)-1:
                self.btproximo.configure(state='normal')
            if index > 1:
                self.btanterior.configure(state='normal')

    def anterior(self):
        '''Vai para o registro anterior.'''
        self.lastindex -= 1
        self.disable_fields()
        self.exibe(self.lastindex)


    def proximo(self):
        '''Vai para o próximo registro.'''
        self.lastindex += 1
        self.exibe(self.lastindex)


    def editar(self):
        self.bteditar.configure(state='disable')
        dados = self.get()
        dados_antigos = dados
        self.enable_fields()
        filetemp = '/seet/dados/temp.csv'
        try:
            with open(FILESEDE, 'r') as old, open(filetemp, 'a') as new:
                writer = csv.DictWriter(new, fieldnames=self.inputs.keys(), lineterminator='\n')
                for row in csv.DictReader(old, fieldnames=self.inputs.keys(), lineterminator='\n'):
                    existearq = os.path.exists(filetemp)
                    if dados['cep'] != row['cep']:
                        if not existearq:
                            writer.writeheader()
                            writer.writerow(row)
                        else:
                            writer.writerow(row)
            os.remove(FILESEDE)
            os.rename(filetemp, FILESEDE)
        except Exception as erro:
            mbox.showerror('', erro)

        for key, value in dados_antigos.items():
            self.inputs[key].set(value)

        self.btsalvar.configure(state='normal')
        self.btexcluir.configure(state='disable')


    def excluir(self):
        dados = self.get()
        cep = dados['cep']
        filetemp = '/seet/dados/temp.csv'
        try:
            with open(FILESEDE, 'r') as old, open(filetemp, 'a') as new:
                writer = csv.DictWriter(new, fieldnames=self.inputs.keys(), lineterminator='\n')
                for row in csv.DictReader(old, fieldnames=self.inputs.keys(), lineterminator='\n'):
                    existearq = os.path.exists(filetemp)
                    if cep not in row.values():
                        if not existearq:
                            writer.writeheader()
                            writer.writerow(row)
                        else:
                            writer.writerow(row)
            os.remove(FILESEDE)
            os.rename(filetemp, FILESEDE)
        except Exception as erro:
            mbox.showerror('', erro)
        self.carrega_dados_arquivo()


    def salvar(self):
        dados = self.get()
        try:
            for key, value in self.inputs.items():
                if value.get() != '' or key == 'comp':
                    emptyfield = False
                else:
                    emptyfield = True
            if not emptyfield:
                with open(FILESEDE, 'a') as file:
                    writer = csv.DictWriter(file, fieldnames=dados.keys(), lineterminator='\n')
                    writer.writerow(dados)
                mbox.showinfo('', 'Dados salvos com sucesso!')
                self.btsalvar.configure(state='disable')
                self.btnovo.configure(state='normal')
                self.carrega_dados_arquivo()
            else:
                mbox.showinfo('', 'Preencha todos os campos!')
        except Exception as erro:
            mbox.showerror('', erro)