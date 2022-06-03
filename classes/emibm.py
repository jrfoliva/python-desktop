# Classe que coleta os dados como nota fiscal séries, funcionário para emitir o recibo e etiquetas

# Importações
import csv
import os
import tkinter as tk
from time import strftime
from tkinter import ttk, messagebox
import webbrowser

from reportlab.pdfgen import canvas


class EmIBM(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.fonte = ('Calibri', 12, 'normal')
        self.pecas = []
        tk.Label(self, text='Controle de Devolução de Peças IBM', font=('Arial', 14, 'normal')).pack(pady=10)
        self.entradas = {}

        # widgets
        framefields = tk.LabelFrame(self, text='Informações: ', fg='blue', font=self.fonte)
        framefields.pack(fill='x', padx=15, pady=10)

        ttk.Label(framefields, text='Data:', font=self.fonte).grid(row=0, column=0, sticky='W', padx=4)
        self.data = tk.StringVar()
        self.entradas['data'] = self.data
        ttk.Entry(framefields, textvariable=self.data, width=15, font=self.fonte, justify='center').grid(row=0, column=1, sticky='w',
                                                                                       padx=4)

        ttk.Label(framefields, text='Funcionário:', font=self.fonte).grid(row=0, column=2, sticky='w', padx=4)
        self.funcionario = tk.StringVar()
        self.entradas['funcionario'] = self.funcionario
        self.cbfuncionario = ttk.Combobox(framefields, textvariable=self.funcionario, state='readonly',
                                          font=self.fonte, justify='center')
        self.cbfuncionario.grid(row=0, column=3, sticky='w', padx=4)

        ttk.Label(framefields, text='Num. NF:', font=self.fonte).grid(row=0, column=4, sticky='W', padx=4)
        self.nf = tk.StringVar()
        self.entradas['nota fiscal'] = self.nf
        ttk.Entry(framefields, textvariable=self.nf, width=15, font=self.fonte, justify='center').grid(row=0, column=5, sticky='W',
                                                                                     padx=4)

        ttk.Label(framefields, text='Part Number:', font=self.fonte).grid(row=2, column=0, sticky='W', padx=4,
                                                                          pady=15)
        self.part = tk.StringVar()
        self.entradas['part number'] = self.part
        ttk.Entry(framefields, textvariable=self.part, width=15, font=self.fonte, justify='center').grid(row=2, column=1,
                                                                                                 sticky='W', padx=4)

        ttk.Label(framefields, text='Quantidade:', font=self.fonte).grid(row=2, column=2, sticky='W', padx=4)
        self.qtd = tk.StringVar()
        self.entradas['quantidade'] = self.qtd
        ttk.Entry(framefields, textvariable=self.qtd, width=15, font=self.fonte, justify='center').grid(row=2, column=3,
                                                                                      sticky='W', padx=4)

        ttk.Label(framefields, text='Order:', font=self.fonte).grid(row=2, column=4, sticky='W', padx=4)
        self.order = tk.StringVar()
        self.entradas['order'] = self.order
        ttk.Entry(framefields, textvariable=self.order, width=15, font=self.fonte, justify='center').grid(row=2, column=5,
                                                                                        sticky='W', padx=4)

        ttk.Label(framefields, text='Num. Lacre:', font=self.fonte).grid(row=3, column=0, sticky='W', padx=4)
        self.lacre = tk.StringVar()
        self.entradas['num lacre'] = self.lacre
        ttk.Entry(framefields, textvariable=self.lacre, width=15, font=self.fonte, justify='center').grid(row=3, column=1,
                                                                                        sticky='W', padx=4)

        frameradiobut = tk.LabelFrame(framefields, text='Estado da Peça: ', font=self.fonte)
        frameradiobut.grid(row=3, column=4, columnspan=2, sticky='W', padx=4, pady=4)

        self.estadoPeca = tk.StringVar()
        self.entradas['estado peca'] = self.estadoPeca
        # Looping para criar os radiobuttons
        pecaEstado = ['BAD', 'DIVER', 'GOOD']
        for i in range(len(pecaEstado)):
            curRad = tk.Radiobutton(frameradiobut, text=pecaEstado[i], variable=self.estadoPeca,
                                    value=pecaEstado[i], font=self.fonte)
            if pecaEstado[i] == 'BAD':
                curRad.select()
            curRad.grid(row=0, column=i, sticky='W')

        framebutton = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        framebutton.pack(side='bottom', fill='x', padx=15, pady=10)

        self.btincluir = tk.Button(framebutton, text='Incluir Peça', width=10, font=('Arial', 14, 'normal'),
                                  fg='blue', command=self.nova_peca)
        self.btincluir.pack(side='left', padx=4, pady=20)

        # self.btetiqueta = tk.Button(framebutton, text='Etiqueta', width=10, font=('Arial', 14, 'normal'),
        #                             fg='blue', state='disable', command=self.etiqueta)
        # self.btetiqueta.pack(side='left', padx=4)

        self.btrecibo = tk.Button(framebutton, text='Recibo', width=10, font=('Arial', 14, 'normal'),
                                  fg='blue', state='disable', command=self.recibo)
        self.btrecibo.pack(side='left', padx=4)

        self.btlimpar = tk.Button(framebutton, text='Cancelar', width=10, font=('Arial', 14, 'normal'),
                                  fg='blue', command=self.limpar_campos)
        self.btlimpar.pack(side='left', padx=4)

        self.btvoltar = tk.Button(framebutton, text='Voltar', width=10, font=('Arial', 14, 'normal'),
                                  fg='blue', command=self.voltar)
        self.btvoltar.pack(side='right', padx=4, pady=20)

        framenotas = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        framenotas.pack(fill='x', padx=15, pady=10)

        tk.Label(framenotas, text='Peça(s):', font=self.fonte, fg='blue').pack()
        self.lbpecas = tk.Label(framenotas, font=self.fonte, fg='red')
        self.lbpecas.pack()

        #-----------------------------------------------------------------------------------------------#
        # Reset campos e atualiza combobox funcionário
        self.resetcampos()
        self.atualizafunc()

    # Métodos
    def voltar(self):
        from seet import MainFrame
        self.master.switch_frame(MainFrame)


    def limpar_campos(self):
        self.entradas['nota fiscal'].set('')
        self.entradas['part number'].set('')
        self.entradas['quantidade'].set('')
        self.entradas['order'].set('')
        self.entradas['num lacre'].set('')
        self.entradas['estado peca'].set('BAD')
        self.pecas.clear()
        self.exibe_pecas()
        #self.btetiqueta.configure(state='disable')
        self.btrecibo.configure(state='disable')


    def exibe_pecas(self):
        '''Exibe os dados das etiquetas ja incluidas'''
        texto = ''
        for peca in self.pecas:
            texto += peca['part number'] + ' '
        self.lbpecas.configure(text=texto)


    def nova_peca(self):
        '''Cria uma lista com de etiquetas'''
        dados = self.get()
        if dados['nota fiscal'] != '':
            self.pecas.append(dados)
            self.exibe_pecas()
            self.resetcampos()
            #self.btetiqueta.configure(state='normal')
            self.btrecibo.configure(state='normal')
        else:
            messagebox.showinfo('', 'Preencha todos os campos para emissão do controle!')


    def get(self):
        dados = {}
        for key in self.entradas.keys():
            dados[key] = self.entradas[key].get().upper()
        return dados


    def recibo(self):
        dados = self.pecas
        path = '/seet/recibos/recibo_'
        campos = ['Nota Fiscal', 'Part Number', 'Quantidade', 'Order', 'Lacre', 'Estado da Peça']
        #vlrcampos = [dados['nota fiscal'], dados['serie instalada'], dados['serie retirada'], dados['estado peca']]
        funcionario = dados[0]['funcionario']
        data = dados[0]['data']
        try:
            with open ('/seet/dados/funcionarios.csv', 'r') as file:
                fields = ['matricula', 'funcionario']
                reader = csv.DictReader(file, fieldnames=fields)
                for row in reader:
                    print(row['funcionario'], funcionario)
                    if row['funcionario'].upper() == funcionario:
                        matricula = row['matricula']

        except Exception as erro:
            messagebox.showerror('', erro)

        try:
            nome_pdf = path + dados[0]['funcionario'] + '_{}'.format(strftime('%d%m%Y'))
            path_to_open = "C:\seet\\recibos\\recibo_"+ dados[0]['funcionario'] + '_{}.pdf'.format(strftime('%d%m%Y'))
            pdf = canvas.Canvas('{}.pdf'.format(nome_pdf))
            x = 660
            y = 35
            # Linha dos campos
            pdf.setFont('Helvetica-Oblique', 12)
            for campo in campos:
                pdf.drawString(y, x, '{}'.format(campo))
                y += (len(campo) + 80)
            x = 645
            y = 35
            # Linha dos valores dos campos
            dadosNota = []
            volumes = 0
            for nota in dados:
                for key, value in nota.items():
                    if key != 'funcionario' and key != 'data':
                        dadosNota.append(nota[key])

                volumes += 1

                for reg in dadosNota:
                    pdf.drawString(y, x, '{}'.format(reg))
                    y += (len(reg) + 85)
                dadosNota.clear()
                y = 35
                x -= 15

            x -= 15
            pdf.setTitle(nome_pdf)
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(180, 760, 'CONTROLE DE PEÇAS DEVOLVIDAS')
            pdf.drawString(180, 759, '________________________________')
            pdf.setFont("Helvetica-Oblique", 12)
            pdf.drawString(y, 700, 'Funcionário: {} - Almox.: {}.'.format(funcionario, matricula))
            pdf.drawString(475, 700, 'Data: '+ data)
            pdf.drawString(y, x, 'Volume(s): '+ str(volumes))
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(250, 400, 'Motorista:_______________________________________')
            pdf.drawString(250, 380, 'RG:__________________, Data retirada:____/____/_____')
            pdf.drawString(250, 350, 'Assinatura:______________________________________')
            pdf.save()
            messagebox.showinfo('', '{}.pdf criado com sucesso!'.format(nome_pdf))
            webbrowser.open_new(path_to_open)
        except Exception as erro:
            messagebox.showerror('', erro)


    def etiqueta(self):
        print_com1 = 'copy \seet\layout\etiqueta.txt COM1'
        try:
            for etiqueta in self.etiquetas:
                nota = etiqueta['nota fiscal']
                with open('/seet/layout/layout.txt', 'r') as input, open('/seet/layout/etiqueta.txt', 'w+') as output:
                    output.write(input.read())
                    output.write('\nBARCODE 490,591,"39",102,0,180,3,8,"{nf}"'.format(nf=nota))
                    output.write('\nTEXT 459,476,"4",180,2,2,"{nf}"'.format(nf=nota))
                    output.write('\nPRINT 1,1')
                    output.write('\n<xpml></page></xpml><xpml><end/></xpml>CLS')
                os.system(print_com1)
        except Exception as erro:
            messagebox.showerror('', erro)



    def atualizafunc(self):
        lista = []
        try:
            with open('/seet/dados/funcionarios.csv', 'r') as file:
                reader = csv.DictReader(file)
                for linha in reader:
                    if linha['funcionario'] != 'funcionario':
                        lista.append(linha['funcionario'])
                lista.sort()
            self.cbfuncionario['values'] = lista
        except :
            messagebox.showinfo('', 'Cadastrar funcionário primeiro!')

    def resetcampos(self):
        data = strftime('%d/%m/%Y')
        self.entradas['data'].set(data)
        self.entradas['nota fiscal'].set('')
        self.entradas['part number'].set('')
        self.entradas['quantidade'].set('')
        self.entradas['order'].set('')
        self.entradas['num lacre'].set('')
        self.entradas['estado peca'].set('BAD')
