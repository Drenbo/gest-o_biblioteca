import json
import os

def criar_banco():
    if not os.path.exists('banco_biblioteca.json'):
        modelo = {"livros": [], "emprestimos": []}
        with open('banco_biblioteca.json', 'w') as file:
            json.dump(modelo, file, indent=5)
        print("Banco de dados criado com sucesso!")
    else:
        print("Banco de dados já existe.")

def carregar_banco():
    try:
        with open('banco_biblioteca.json', 'r') as file:
            dicionario = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        dicionario = {"livros": [], "emprestimos": []}
    return dicionario

def salvar_banco(dicionario):
    with open('banco_biblioteca.json', 'w') as file:
        json.dump(dicionario, file, indent=5)

def visualizar_livros():
    dicionario = carregar_banco()

    if not dicionario.get('livros', []):
        print("Nenhum livro cadastrado.")
    else:
        print("Livros disponíveis:")
        for livro in dicionario['livros']:
            print(f"Título: {livro['titulo']}, Autor: {livro['autor']}, Cópias disponíveis: {livro['copias']}")

def adicionar_livro():
    titulo = input('Qual o título do livro? ')
    autor = input('Qual o nome do autor? ')
    copias = int(input('Quantas cópias? '))

    novo_livro = {
        "titulo": titulo,
        "autor": autor,
        "copias": copias
    }

    dicionario = carregar_banco()
    dicionario.setdefault('livros', []).append(novo_livro)
    salvar_banco(dicionario)

    print("Livro adicionado com sucesso!")

def emprestar_livro():
    dicionario = carregar_banco()
    emprestimo = input("Qual livro deseja alugar? ")
    encontrado = False

    for livro in dicionario.get('livros', []):
        if livro['titulo'].lower() == emprestimo.lower():
            encontrado = True
            if livro['copias'] > 0:
                usuario = input("Digite seu nome para registrar o empréstimo: ")
                livro['copias'] -= 1

                novo_emprestimo = {
                    "titulo": livro['titulo'],
                    "usuario": usuario
                }
                dicionario.setdefault('emprestimos', []).append(novo_emprestimo)

                print(f"Empréstimo realizado com sucesso! Livro: {livro['titulo']}")
            else:
                print("O livro está em falta.")
            break

    if not encontrado:
        print("Livro não encontrado.")

    salvar_banco(dicionario)

def devolver_livro():
    dicionario = carregar_banco()
    devolucao = input("Qual livro deseja devolver? ")
    usuario = input("Informe o nome do usuário que fez o empréstimo: ")
    encontrado = False

    for emprestimo in dicionario.get('emprestimos', []):
        if emprestimo['titulo'].lower() == devolucao.lower() and emprestimo['usuario'].lower() == usuario.lower():
            encontrado = True
            dicionario['emprestimos'].remove(emprestimo)

            for livro in dicionario.get('livros', []):
                if livro['titulo'].lower() == devolucao.lower():
                    livro['copias'] += 1
                    print(f"Devolução realizada com sucesso! Livro: {livro['titulo']}")
                    break
            break

    if not encontrado:
        print("Empréstimo não encontrado. Verifique as informações.")

    salvar_banco(dicionario)

def visualizar_emprestimos():
    dicionario = carregar_banco()

    if not dicionario.get('emprestimos', []):
        print("Nenhum empréstimo registrado.")
    else:
        print("Lista de empréstimos:")
        for emprestimo in dicionario['emprestimos']:
            print(f"Livro: {emprestimo['titulo']}, Usuário: {emprestimo['usuario']}")

def menu():
    criar_banco()

    while True:
        print("\nBem-vindo à nossa Biblioteca virtual!")
        print("Escolha uma opção abaixo:")
        print("1. Visualizar Livros")
        print("2. Adicionar Livro")
        print("3. Empréstimo de Livros")
        print("4. Devolver Livro")
        print("5. Visualizar Empréstimos")
        print("6. Sair")
        
        try:
            resposta = int(input(": "))
        except ValueError:
            print("Por favor, insira um número válido.")
            continue

        if resposta == 1:
            visualizar_livros()
        elif resposta == 2:
            adicionar_livro()
        elif resposta == 3:
            emprestar_livro()
        elif resposta == 4:
            devolver_livro()
        elif resposta == 5:
            visualizar_emprestimos()
        elif resposta == 6:
            print("Encerrando o sistema. Obrigado pela vsita!")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu()
