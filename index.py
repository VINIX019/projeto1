import csv
import os

nome_arquivo = 'cadastro.csv'


def mostrar_cadastros():
    try:
        with open('cadastro.csv', mode='r', newline='', encoding='utf-8') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)

            try:
                next(leitor_csv)  
            except StopIteration:
                print('O arquivo existe, mas está vazio.')
                return

            print('--- Cadastros ---')
            for linha in leitor_csv:
                if linha:
                    try:
                        
                        nome, tel, v, m, j, vj, vt = linha
                        v = float(v)
                        vj = float(vj)
                        vt = float(vt)

                        print('''
                      Nome: {}
                      Telefone: +55 {}
                      Valor: R${:.2f}
                      Meses: {}
                      Juros: {}%
                      Valor de cada parcela: R${:.2f}
                      Valor final a receber: R${:.2f}
                      '''.format(nome, tel, v, m, j, vj, vt))
                    except (ValueError, IndexError):
                        print(f"Erro ao processar a linha: {linha}. Possível corrupção de dados.")

    except FileNotFoundError:
        print('Nenhum cadastro encontrado')


def gerenciar_cadastros():
    mostrar_cadastros()
    try:
        if not os.path.exists(nome_arquivo):
            return

        acao = input('\nO que deseja fazer? [E]Editar ou [X]Excluir? ').upper()
        if acao not in ['E', 'X']:
            print("Opção inválida.")
            return

        nome_alvo = input('Digite o nome do cliente para ' + ('editar' if acao == 'E' else 'excluir') + ': ')

        registros = []
        encontrado = False
        with open(nome_arquivo, mode='r', newline='', encoding='utf-8') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            header = next(leitor_csv)
            registros.append(header)
            for linha in leitor_csv:
                if linha and linha[0].lower() == nome_alvo.lower():
                    encontrado = True
                    if acao == 'E':
                        print(f"Editando cadastro de {linha[0]}")
                        nome = input(f"Novo nome ({linha[0]}): ") or linha[0]
                        tel = input(f"Novo telefone ({linha[1]}): ") or linha[1]
                        v = float(input(f"Novo valor emprestado ({float(linha[2]):.2f}): ") or linha[2])
                        m = int(input(f"Novos meses ({linha[3]}): ") or linha[3])
                        j = float(input(f"Novos juros ({linha[4]}): ") or linha[4])
                        vj = (v / m) + (v * j / 100)
                        vt = vj * m
                        registros.append([nome, tel, v, m, j, vj, vt])
                    else:  
                        print(f"Cadastro de {linha[0]} excluído com sucesso.")
                else:
                    registros.append(linha)

        if not encontrado:
            print(f"Cliente '{nome_alvo}' não encontrado.")

    
        with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
            writer = csv.writer(arquivo_csv)
            writer.writerows(registros)

    except ValueError:
        print('Entrada inválida. Operação cancelada.')
while True:
    print('''Selecione a opcao desejada
    Clientes[1]
    Resgistrar[2]
    Editar/Excluir[3]
    Sair[4]
    ''')

    try:
        opcao = int(input('Selecione a opcao: '))

        if opcao == 1:
            mostrar_cadastros()
        elif opcao == 2:
            try:
                p = int(input('Quantas pessoas deseja registrar?'))
                arquivo_existe = os.path.exists(nome_arquivo)

                with open(nome_arquivo, 'a', newline='', encoding='utf-8') as arquivo_csv:
                    writer = csv.writer(arquivo_csv)
                    if not arquivo_existe:
                        writer.writerow(
                            ['Nome', 'Telefone', 'Valor emprestado', 'Meses para pagar', 'Juros por mes', 'Valor mensal',
                             'Valor total'])

                    for c in range(p):
                        print('--- Faça o cadastro ---')
                        nome = str(input('Nome: '))
                        tel = int(input('Telefone: +55 '))
                        v = float(input('Digite o valor emprestado: R$'))
                        m = int(input('Quantos meses para pagar: '))
                        j = float(input('Quantos % voce deu de juros? '))

                        vj = (v / m) * (j / 100) + (v / m)
                        vt = vj * m

                        writer.writerow([nome, tel, v, m, j, vj, vt])
                        print('''Cadastro efetuado com sucesso!
                    Nome: {}
                    telefone: +55 {}
                    valor emprestado: R${:.2f}
                    Meses para pagar: {}
                    Juros por mes: {}%
                    Valor a pagar por mes: R${:.2f}
                    Valor total a recever: R${:.2f}
                    '''.format(nome, tel, v, m, j, vj, vt))
            except ValueError:
                print('Entrada invalida. Por favor, digite os dados corretamente!')
        elif opcao == 3:
            gerenciar_cadastros()
        elif opcao == 4:
            print('Saindo do programa!')
            break
        else:
            print('Opcao invalida')
    except ValueError:
        print('Entrada inválida. Por favor, digite um número (1 ou 2).')