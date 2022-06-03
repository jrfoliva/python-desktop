# Manutenção de arquivo e estração de dados
# 01/05/2020 - Junior Freire Oliva

# Importações
import os, csv
from tkinter import messagebox

class FileManager:
    def __init__(self, arquivo):
        self.arquivo = arquivo

    # métodos

    def check_reg(self, dados):
        matricula = dados['matricula']
        existearq = os.path.exists(self.arquivo)
        try:
            if existearq:
                with open(self.arquivo, 'r') as file:
                    reader = csv.DictReader(file, fieldnames=dados.keys())
                    for registro in reader:
                        if matricula == registro['matricula']:
                            dados['matricula'] = registro['matricula']
                            dados['funcionario'] = registro['funcionario']
                            return True
                    return False
        except Exception as erro:
            messagebox.showerror('', erro)


    def insert(self, inputs):
        fields = ['matricula', 'funcionario']
        existearq = os.path.exists(self.arquivo)
        try:
            with open(self.arquivo, 'a') as file:
                writer = csv.DictWriter(file, fieldnames=fields, lineterminator='\n')
                if existearq:
                    writer.writerow(inputs)
                else:
                    writer.writeheader()
                    writer.writerow(inputs)
            messagebox.showinfo('', 'Registro gravado com sucesso!')
        except Exception as erro:
            messagebox.showerror('', erro)


    def delete(self, info):
        filetemp = '/seet/dados/temp.csv'
        fields = ['matricula', 'funcionario']

        try:
            with open(self.arquivo, 'r') as old, open(filetemp, 'a') as new :
                writer = csv.DictWriter(new, fieldnames=fields, lineterminator='\n')
                for row in csv.DictReader(old, fieldnames=fields, lineterminator='\n'):
                    existearq = os.path.exists(filetemp)
                    if info not in row.values():
                        if not existearq:
                            writer.writeheader()
                            writer.writerow(row)
                        else:
                            writer.writerow(row)
            os.remove(self.arquivo)
            os.rename(filetemp, self.arquivo)
        except Exception as erro:
            messagebox.showerror('', erro)