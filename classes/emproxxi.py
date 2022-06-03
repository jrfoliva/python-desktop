# Classe que coleta os dados como nota fiscal séries, funcionário para emitir o recibo e etiquetas

# Importações
import csv
import os
import tkinter as tk
from time import strftime
from tkinter import ttk, messagebox
import webbrowser

from reportlab.pdfgen import canvas


class EmProxxi(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.fonte = ('Calibri', 12, 'normal')
        self.pecas = []
        tk.Label(self, text='Emissor de Etiqueta e Recibo', font=('Arial', 14, 'normal')).pack(pady=10)
        self.entradas = {}

        # widgets
        framecab = tk.LabelFrame(self, text=' Cabeçalho ', fg='blue', font=self.fonte)
        framecab.pack(fill='x', padx=15, pady=10)

        ttk.Label(framecab, text='Data:', font=self.fonte).grid(row=0, column=0, sticky='W', padx=4)
        self.data = tk.StringVar()
        self.entradas['data'] = self.data
        ttk.Entry(framecab, textvariable=self.data, width=15, font=self.fonte, justify='center').grid(row=0, column=1, sticky='w',
                                                                                       padx=4)

        ttk.Label(framecab, text='Funcionário:', font=self.fonte).grid(row=0, column=2, sticky='w', padx=4)
        self.funcionario = tk.StringVar()
        self.entradas['funcionario'] = self.funcionario
        self.cbfuncionario = ttk.Combobox(framecab, textvariable=self.funcionario, state='readonly',
                                          font=self.fonte)
        self.cbfuncionario.grid(row=0, column=3, sticky='w', padx=4)

        ttk.Label(framecab, text='Num. NF:', font=self.fonte).grid(row=0, column=4, sticky='W', padx=4)
        self.nf = tk.StringVar()
        self.entradas['nota fiscal'] = self.nf
        ttk.Entry(framecab, textvariable=self.nf, width=10, font=self.fonte, justify='center').grid(row=0, column=5, sticky='W',
                                                                                     padx=4)

        ttk.Label(framecab, text='Sede/Destino:', font=self.fonte).grid(row=1, column=0, sticky='w', padx=4)
        self.destino = tk.StringVar()
        self.entradas['destino'] = self.destino
        self.cbdestino = ttk.Combobox(framecab, textvariable=self.destino, state='readonly',
                                          font=self.fonte)
        self.cbdestino.grid(row=1, column=1, sticky='w', padx=4, pady=4)

        framepeca = tk.LabelFrame(self, text=' Dados da peça ', fg='blue', font=self.fonte)
        framepeca.pack(fill='x', padx=15, pady=10)

        ttk.Label(framepeca, text='Série Instalada:', font=self.fonte).grid(row=0, column=0, sticky='W', padx=4,
                                                                              pady=10)
        self.serieInstalada = tk.StringVar()
        self.entradas['serie instalada'] = self.serieInstalada
        ttk.Entry(framepeca, textvariable=self.serieInstalada, width=10, font=self.fonte, justify='center').grid(row=0, column=1,
                                                                                                 sticky='W', padx=4)

        ttk.Label(framepeca, text='Série devolvida:', font=self.fonte).grid(row=0, column=2, sticky='W', padx=4)
        self.serieRetirada = tk.StringVar()
        self.entradas['serie devolvida'] = self.serieRetirada
        ttk.Entry(framepeca, textvariable=self.serieRetirada, width=10, font=self.fonte, justify='center').grid(row=0, column=3,
                                                                                                sticky='W', padx=4)

        frameradiobut = tk.LabelFrame(framepeca, text='Estado da Peça: ', font=self.fonte)
        frameradiobut.grid(row=0, column=5, padx=30, pady=4)

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

        self.btetiqueta = tk.Button(framebutton, text='Etiqueta', width=10, font=('Arial', 14, 'normal'),
                                    fg='blue', state='disable', command=self.etiqueta)
        self.btetiqueta.pack(side='left', padx=4)

        self.btrecibo = tk.Button(framebutton, text='Recibo', width=10, font=('Arial', 14, 'normal'),
                                  fg='blue', state='disable', command=self.recibo)
        self.btrecibo.pack(side='left', padx=4)

        self.btlimpar = tk.Button(framebutton, text='Cancelar', width=10, font=('Arial', 14, 'normal'),
                                  fg='blue', command=self.limpar_campos)
        self.btlimpar.pack(side='left', padx=4)

        self.btvoltar = tk.Button(framebutton, text='Voltar', width=10, font=('Arial', 14, 'normal'),
                                  fg='blue', command=self.voltar)
        self.btvoltar.pack(side='right', padx=4, pady=20)

        frameetiquetas = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        frameetiquetas.pack(fill='x', padx=15, pady=10)

        tk.Label(frameetiquetas, text='Notas Fiscais:', font=self.fonte, fg='blue').pack()
        self.lbetiqueta = tk.Label(frameetiquetas, font=self.fonte, fg='red')
        self.lbetiqueta.pack()

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
        self.entradas['serie instalada'].set('')
        self.entradas['serie devolvida'].set('')
        self.entradas['estado peca'].set('BAD')
        self.pecas.clear()
        self.exibe_etiqueta()
        self.btetiqueta.configure(state='disable')
        self.btrecibo.configure(state='disable')


    def exibe_etiqueta(self):
        '''Exibe os dados das etiquetas ja incluidas'''
        texto = ''
        for etiqueta in self.pecas:
            texto += etiqueta['nota fiscal'] + ' '
        self.lbetiqueta.configure(text=texto)


    def nova_peca(self):
        '''Cria uma lista com de peças'''
        dados = self.get()
        if dados['nota fiscal'] != '':
            self.pecas.append(dados)
            self.exibe_etiqueta()
            self.resetcampos()
            self.btetiqueta.configure(state='normal')
            self.btrecibo.configure(state='normal')
        else:
            messagebox.showinfo('', 'Preencha os campos para a emissão da etiqueta!')


    def get(self):
        dados = {}
        for key in self.entradas.keys():
            dados[key] = self.entradas[key].get()
        return dados


    def recibo(self):
        dados = self.pecas
        path = '/seet/recibos/recibo_'
        campos = ['Nota Fiscal', 'Destino', 'Serial Instalada', 'Serial Devolvida', 'Estado da Peça']
        #vlrcampos = [dados['nota fiscal'], dados['serie instalada'], dados['serie retirada'], dados['estado peca']]

        funcionario = dados[0]['funcionario']
        data = dados[0]['data']

        try:
            fields = ['matricula', 'funcionario']
            with open ('/seet/dados/funcionarios.csv', 'r') as file:
                reader = csv.DictReader(file, fieldnames=fields)
                for row in reader:
                    if row['funcionario'] == funcionario:
                        matricula = row['matricula']

        except Exception as erro:
            messagebox.showerror('', erro)

        try:
            nome_pdf = path + dados[0]['funcionario'] + '_{}'.format(strftime('%d%m%Y'))
            path_to_open = "C:\seet\\recibos\\recibo_"+ dados[0]['funcionario'] + '_{}.pdf'.format(strftime('%d%m%Y'))
            pdf = canvas.Canvas('{}.pdf'.format(nome_pdf))
            x = 660
            y = 60
            # Linha dos campos
            pdf.setFont('Helvetica-Oblique', 12)
            for campo in campos:
                pdf.drawString(y, x, '{}'.format(campo))
                y += (len(campo) + 85)
            x = 645
            y = 60
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
                    y += (len(reg) + 92)

                dadosNota.clear()
                y = 60
                x-=15

            x-=15
            pdf.setTitle(nome_pdf)
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(180, 760, 'CONTROLE DE PEÇAS DEVOLVIDAS')
            pdf.drawString(180, 759, '________________________________')
            pdf.setFont("Helvetica-Oblique", 12)
            pdf.drawString(60, 700, 'Funcionário: {} - Almox.: {}.'.format(funcionario, matricula))
            pdf.drawString(440, 700, 'Data: '+ data)
            pdf.drawString(60, x, 'Volume(s): '+ str(volumes))
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
            for etiqueta in self.pecas:
                nota = etiqueta['nota fiscal']
                with open('/seet/layout/layout.txt', 'r')as input, open('/seet/layout/etiqueta.txt', 'w+') as output:
                    output.write(input.read())
                    output.write('\nBARCODE 490,591,"39",102,0,180,3,8,"{nf}"'.format(nf=nota))
                    output.write('\nTEXT 459,476,"4",180,2,2,"{nf}"'.format(nf=nota))
                    output.write('\nPRINT 1,1')
                    output.write('\n<xpml></page></xpml><xpml><end/></xpml>CLS')
                os.system(print_com1)
        except Exception as erro:
            messagebox.showerror('', erro)



    def atualizafunc(self):
        listafunc = []
        try:
            with open('/seet/dados/funcionarios.csv', 'r') as file:
                reader = csv.DictReader(file)
                for linha in reader:
                    if linha['funcionario'] != 'funcionario':
                        listafunc.append(linha['funcionario'])
                listafunc.sort()
            self.cbfuncionario['values'] = listafunc
        except :
            messagebox.showinfo('', 'Cadastrar funcionário primeiro!')
        listadest = []
        try:
            with open('/seet/dados/sededest.csv', 'r') as file:
                reader = csv.DictReader(file)
                for linha in reader:
                    if linha['cidade'] != 'cidade':
                        listadest.append(linha['cidade'])
                listadest.sort()
            self.cbdestino['values'] = listadest
        except :
            messagebox.showinfo('', 'Cadastrar sedes primeiro!')


    def resetcampos(self):
        data = strftime('%d/%m/%Y')
        self.entradas['data'].set(data)
        self.entradas['nota fiscal'].set('')
        self.entradas['serie instalada'].set('')
        self.entradas['serie devolvida'].set('')
        self.entradas['estado peca'].set('BAD')
