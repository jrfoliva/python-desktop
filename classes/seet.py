#
# Inclusão de Botões de navegadores, editar no cadastro, cadastro de sede, melhoria no recibo
# Inclusão da rotina para emissão do controle de peças para a IBM versão 2.5.20
# Reconstrução do aplicativo SEET para versão 1.5.20
# Melhorias: Abrir ou chamar as rotinas cadastro e emissor ao invés de abrir os frames
# ao mesmo tempo. Incluir botão de retorno para a tela principal
# Criado uma classe para gerenciar o arquivo de dados.

# imports
import locale
import tkinter as tk
from time import strftime

from cadastro import CadFunc
from emproxxi import EmProxxi
from emibm import EmIBM
from sededest import SedeDest

class WindowControl(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(MainFrame)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class MainFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Layout da janela principal
        self.master.geometry('800x450+300+140')
        self.master.resizable(0, 0)
        self.master.title('SEET - Sistema Emissor de Etiquetas Ver. 3.6.20')
        self.fonte = ('Arial', 14, 'normal')
        self.imgfundo = tk.PhotoImage(file='/seet/images/fundo.png')
        self.imgfundo = self.imgfundo.subsample(1, 1)
        self.lbfundo = tk.Label(self, image=self.imgfundo)
        self.lbfundo.pack()
        self.statusbar = tk.Label(None, bd=2, relief=tk.SUNKEN, anchor=tk.W, bg='white')
        self.statusbar.place(y=430, width=800)

        # Botões da tela principal
        self.imgpessoa = tk.PhotoImage(file='/seet/images/pessoa.png')
        self.btcadastro = tk.Button(self, width=80, height=70, image=self.imgpessoa,
                                    compound='top', text='Funcionários',
                                    command=lambda: master.switch_frame(CadFunc))
        self.btcadastro.place(x=20, y=20)

        self.imgsede = tk.PhotoImage(file='/seet/images/sede.png')
        self.btsede = tk.Button(self, width=80, height=70, image=self.imgsede,
                                 compound='top', text='Sede/Destino', anchor='s',
                                 command=lambda: master.switch_frame(SedeDest))
        self.btsede.place(x=130, y=20)

        self.imgetiqueta = tk.PhotoImage(file='/seet/images/etiqueta.png')
        self.btemproxxi = tk.Button(self, width=80, height=70, image=self.imgetiqueta,
                                   compound='top', text='Emissor Proxxi', anchor='s',
                                   command=lambda: master.switch_frame(EmProxxi))
        self.btemproxxi.place(x=240, y=20)

        self.btemibm = tk.Button(self, width=80, height=70, image=self.imgetiqueta,
                                    compound='top', text='Emissor IBM', anchor='s',
                                    command=lambda: master.switch_frame(EmIBM))
        self.btemibm.place(x=350, y=20)

        # Empacota Frame principal
        self.pack(fill='both', expand=True)

        # chama método atualiza barra de status
        self.atualizaData()

    def atualizaData(self):
        '''Atualiza data na barra de status'''
        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR')
        except:
            locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil')
        info = ' ..: @Desenvolvido por Junior Freire Oliva.'
        data = strftime('%A, %d de %B de %Y')
        self.statusbar.configure(text='Hoje é '+data + info, anchor='center', bg='cyan')


if __name__=='__main__':
    windowControl = WindowControl()
    windowControl.mainloop()