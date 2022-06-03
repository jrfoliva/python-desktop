# Importações
import csv
import os
import tkinter as tk
from tkinter import messagebox as mbox
from filemanager import FileManager

# Arquivo de dados dos funcionários
FILEFUNC = '/seet/dados/funcionarios.csv'

class CadFunc(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.fonte = ('Arial', 14, 'normal')
        tk.Label(self, text='Cadastro de Funcionários', font=self.fonte).pack(pady=20)
        self.inputs = {}
        self.fields = []
        self.datalist = []
        self.lastindex = 0
        self.fm = FileManager(FILEFUNC)

        # LabelFrame
        framefields = tk.LabelFrame(self, text='Funcionário ', fg='blue', font=self.fonte)
        framefields.pack()

        # Widgets
        tk.Label(framefields, text='Matrícula:', font=self.fonte).grid(row=0, column=0, sticky='W', padx=4, pady=10)
        self.matricula = tk.StringVar()
        self.inputs['matricula'] = self.matricula
        self.entrymatricula = tk.Entry(framefields, textvariable=self.matricula, width=15,
                                        font=self.fonte, justify='center')
        self.entrymatricula.grid(row=1, column=0, sticky='w', padx=4)
        self.fields.append(self.entrymatricula)

        tk.Label(framefields, text='Nome:', font=self.fonte).grid(row=0, column=1, sticky='w', padx=4)
        self.funcionario = tk.StringVar()
        self.inputs['funcionario'] = self.funcionario
        self.entryfuncionario = tk.Entry(framefields, textvariable=self.funcionario, width=50,
                                          font=self.fonte, justify='center')
        self.entryfuncionario.grid(row=1, column=1, sticky='w', padx=4, pady=10)
        self.fields.append(self.entryfuncionario)

        framebuttons = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        framebuttons.pack(side='bottom', fill='x', pady=20)

        self.imganterior = tk.PhotoImage(file='/seet/images/anterior.png')
        self.btanterior = tk.Button(framebuttons, image=self.imganterior, command=self.anterior)
        self.btanterior.pack(padx=4, side='left', pady=10)

        self.imgproximo = tk.PhotoImage(file='/seet/images/proximo.png')
        self.btproximo = tk.Button(framebuttons, image=self.imgproximo, command=self.proximo)
        self.btproximo.pack(padx=4, side='left')

        self.imgnovo = tk.PhotoImage(file='/seet/images/novo.png')
        self.btnovo = tk.Button(framebuttons, image=self.imgnovo, command=self.novo)
        self.btnovo.pack(padx=4, side='left')

        self.imgeditar = tk.PhotoImage(file='/seet/images/editar.png')
        self.bteditar = tk.Button(framebuttons, image=self.imgeditar, command=self.editar)
        self.bteditar.pack(padx=4, side='left')

        self.imgsalvar = tk.PhotoImage(file='/seet/images/salvar.png')
        self.btsalvar = tk.Button(framebuttons, image=self.imgsalvar, state='disable', command=self.salvar)
        self.btsalvar.pack(padx=4, side='left')

        self.imgexcluir = tk.PhotoImage(file='/seet/images/excluir.png')
        self.btexcluir = tk.Button(framebuttons, image=self.imgexcluir, state='disable', command=self.excluir)
        self.btexcluir.pack(padx=4, side='left')

        self.imgvoltar = tk.PhotoImage(file='/seet/images/voltar.png')
        self.btvoltar = tk.Button(framebuttons, image=self.imgvoltar, command=self.voltar)
        self.btvoltar.pack(padx=4, side='right')

        self.disable_fields()
        self.load_data()
        #-----------------------------------------------------------------------------------------------

    # Métodos

    def disable_fields(self):
        for field in self.fields:
            field.configure(state='disable')


    def enable_fields(self):
        for field in self.fields:
            field.configure(state='normal')


    def voltar(self):
        from seet import MainFrame
        self.master.switch_frame(MainFrame)


    def anterior(self):
        self.disable_fields()
        self.lastindex -= 1
        self.exibe(self.lastindex)


    def proximo(self):
        self.lastindex += 1
        self.exibe(self.lastindex)


    def novo(self):
        for key in self.inputs.keys():
            self.inputs[key].set('')
        self.enable_fields()
        self.entrymatricula.focus()
        self.btnovo.configure(state='disable')
        self.btsalvar.configure(state='normal')
        self.bteditar.configure(state='disable')
        self.btexcluir.configure(state='disable')


    def editar(self):
        self.bteditar.configure(state='disable')
        dados = self.get()
        self.fm.delete(dados['matricula'])
        self.enable_fields()
        self.btsalvar.configure(state='normal')
        self.btexcluir.configure(state='disable')


    def get(self):
        '''Captura valores preenchidos dos campos'''
        dados = {}
        for key, value in self.inputs.items():
            if key == 'funcionario':
                dados[key] = value.get().title()
            else:
                dados[key] = value.get()
        return dados


    def exibe(self, index):
        '''Exibe os dados através do índice passado.'''
        self.btsalvar.configure(state='disable')
        self.btnovo.configure(state='normal')
        #print('Index: {} | LastIndex: {}'.format(index, len(self.datalist)-1))
        if index == 0:
            self.btanterior.configure(state='disable')
            self.btproximo.configure(state='disable')
            self.btexcluir.configure(state='disable')
            for key in self.inputs.keys():
                self.inputs[key].set('')

        if index >= 1:
            self.btexcluir.configure(state='normal')
            dados = self.datalist[index]
            for key, value in dados.items():
                self.inputs[key].set(value)
            if index == 1:
                self.btanterior.configure(state='disable')
            if index == self.lastindex:
                self.btproximo.configure(state='disable')
            if index < len(self.datalist)-1:
                self.btproximo.configure(state='normal')
            if index > 1:
                self.btanterior.configure(state='normal')


    def load_data(self):
        self.datalist.clear()
        existfile = os.path.exists(FILEFUNC)
        if existfile:
            try:
                with open(FILEFUNC, 'r') as file:
                    reader = csv.DictReader(file, fieldnames=self.inputs.keys())
                    for registro in reader:
                        self.datalist.append(registro)
                    self.lastindex = len(self.datalist)-1
                    self.exibe(self.lastindex)
            except Exception as error:
                mbox.showerror('', error)
        else:
            mbox.showinfo('', 'Não há registros no arquivo.')

        self.btnovo.configure(state='normal')
        self.btexcluir.configure(state='normal')
        self.bteditar.configure(state='normal')


    def excluir(self):
        dados = self.get()
        if self.fm.check_reg(dados):
            self.fm.delete(dados['matricula'])
            mbox.showinfo('', 'Registro excluído com sucesso!')
            self.btexcluir.configure(state='disable')
            self.load_data()
        else:
            mbox.showinfo('', 'Erro na tentativa de exclusão do registro!')


    def salvar(self):
        dados = self.get()
        matricula = dados['matricula']
        funcionario = dados['funcionario']
        if matricula != '' and  funcionario != '':
            if self.fm.check_reg(dados):
                mbox.showinfo('', 'Informação: {}, já cadastrada!'.format(dados))
            else:
                self.fm.insert(dados)
                self.novo()
        else:
            mbox.showinfo('', 'Preencha todos os campos!')
        self.btnovo.configure(state='normal')
        self.btsalvar.configure(state='disable')
        self.disable_fields()
        self.load_data()