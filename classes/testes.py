import os, csv


def grava_arq(dados):
    existearq = os.path.exists('/seet/dados/funcionarios.csv')
    try:

        with open('/seet/dados/funcionarios.csv', 'a') as file:
            writer = csv.DictWriter(file, fieldnames=dados.keys(), lineterminator='\n')
            if not existearq:
                writer.writeheader()
                writer.writerow(dados)
            else:
                writer.writerow(dados)
            print('Registro gravado com sucesso!')
    except Exception as erro:
        print(erro)
    input()

def ler_arq():
    print(30 * '#')
    print('Imprimindo dados do arquivo...')
    campos = ['matricula', 'funcionario']
    try:
        with open('/seet/dados/funcionarios.csv') as file:
            reader = csv.DictReader(file, fieldnames=campos)
            for reg in reader:
                print('{} : {}'.format(reg['matricula'], reg['funcionario']))
    except Exception as erro:
        print(erro)
    input()

def cadastrar():
    dados = {}
    dados['matricula'] = input('Matricula: ')
    dados['funcionario'] = input('Nome do funcionario: ')
    grava_arq(dados)


while True:
    os.system('cls')
    print('\t\t##Sistema para testes##')
    menu = ['1 - Cadastro', '2 - Exibir dados do arquivo', '0 - Sair\n']
    for r in menu:
        print(r)
    op = input('Escolha uma opção:')
    if op == '1':
        cadastrar()
    if op == '2':
        ler_arq()
    if op == '0':
        break
    else:
        print('Opção incorreta!')

