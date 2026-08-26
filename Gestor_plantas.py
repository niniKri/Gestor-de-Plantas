# Trabalho realizado por Anny Santos

import json
from datetime import datetime, date

FICHEIRO = "plantas.json"

# ========================================================================================================================
# 1 - FUNÇÃO: CARREGAR DADOS -> Guarda plantas e as contas 
# ========================================================================================================================

#Esta função serve para carregar os dados guardados no ficheiro JSON. 
#Primeiro, tenta abrir e ler o ficheiro. 
#Depois, verifica se os dados estão no formato correto e garante que existem as listas de utilizadores e plantas.

def carregar_dados():
    try:
        with open(FICHEIRO, "r", encoding="utf-8") as ficheiro:
            dados = json.load(ficheiro)

            if not isinstance(dados, dict):
                print("Erro: o ficheiro JSON está inválido.") # Possivel erro : Ficheiro JSON invalido
                return {"utilizadores": [], "plantas": []}

            if "utilizadores" not in dados:
                dados["utilizadores"] = []

            if "plantas" not in dados:
                dados["plantas"] = []

            return dados

    except FileNotFoundError:
        print("\n O ficheiro plantas.json ainda não existe.")  # Possivel erro : Ficheiro JSON nao existe
        print("Será criado automaticamente.")
        return {"utilizadores": [], "plantas": []}

    except json.JSONDecodeError:
        print("\nErro: o ficheiro plantas.json contém dados inválidos.") # Possivel erro : Ficheiro JSON com dados invalidos
        print("A aplicação vai começar sem dados.")
        return {"utilizadores": [], "plantas": []}

    except OSError:
        print("\nErro ao abrir o ficheiro de dados.")  # Possivel erro : Erro ao abrir o Ficheiro JSON 
        return {"utilizadores": [], "plantas": []}

# ========================================================================================================================
# 2 - FUNÇÃO: GUARDAR DADOS
# ========================================================================================================================

#Esta função serve para guardar os dados da aplicação no ficheiro JSON. 
#Recebe os dados através do parâmetro dados, abre o ficheiro em modo de escrita e grava os dados no formato JSON. 

def guardar_dados(dados):
    try:
        with open(FICHEIRO, "w", encoding="utf-8") as ficheiro:
            json.dump(
                dados,
                ficheiro,
                indent=4,
                ensure_ascii=False
            )

    except OSError:
        print("Erro: não foi possível guardar os dados.")  # Possivel erro : Nao foi possivel guardar os dados

# ========================================================================================================================
#  3 - FUNÇÃO: Criar ou entrar numa conta
# ========================================================================================================================

# -----------CRIAR CONTA--------------------------------------------------------------------------------------------------
def criar_conta(dados):
    
    print("\n--- CRIAR CONTA ---")

    # NOME
    while True:
        nome = input("Nome: ").strip().upper()
        if nome == "":
            print("Erro: o nome não pode estar vazio.") # Possivel erro: nome estar vazio
            continue
        if not nome.replace(" ", "").isalpha():
            print("Erro: o nome não pode conter números ou caracteres especiais.") # Possivel erro: nome invalido
            continue
        break

    # IDADE
    while True:
        try:
            idade = int(input("Idade: "))
        except ValueError:
            print("Erro: a idade deve ser um número inteiro.") # Possivel erro: nao ser inteiro
            continue
        if idade <= 0:
            print("Erro: a idade deve ser superior a 0.") # Possivel erro: idade ser menor que 0 
            continue
        break

    # USERNAME
    while True:
        username = input("Username: ").strip()

        if username == "":
            print("Erro: o username não pode estar vazio.") # Possivel erro: username estar vazio
            continue

        username_repetido = False
        for utilizador in dados["utilizadores"]:
            if utilizador["username"].lower() == username.lower():
                print("Erro: esse username já está registado.") # Possivel erro: ja existitr um username com ese nome
                username_repetido = True
                break #trocado -> tinha continue

        if not username_repetido: #se o username nao estiver repetido avanza
            break

    # PASSWORD
    while True:
        password = input("Password (Por-favor anotar a password num papel!): ").strip()

        if password == "":
            print("Erro: a password não pode estar vazia.") # Possivel erro: password vazia
            continue

        if len(password) < 6:
            print("Erro: a password deve ter pelo menos 6 caracteres.") # Possivel erro: n tem caracteres
            continue

        password_confirmacao = input("Confirmar password: ").strip()

        if password != password_confirmacao:
            print("Erro: as passwords não coincidem.") # Possivel erro: as passes nao coincidem
            continue

        break

    # GERAR ID
# GERAR ID
    if len(dados["utilizadores"]) == 0:
        novo_id = 1
    else:
        maior_id = 0

        for utilizador in dados["utilizadores"]:
            if utilizador["id"] > maior_id:
                maior_id = utilizador["id"]

        novo_id = maior_id + 1

    # CRIAR UTILIZADOR
    utilizador = {
        "id": novo_id,
        "nome": nome,
        "idade": idade,
        "username": username,
        "password": password

    }

    dados["utilizadores"].append(utilizador)

    guardar_dados(dados)    # chama a funcao e guarda imediatamente no JSON

    print(f"\n A Conta do {username} foi criada com sucesso! ✔️")

# ----------- ENTRAR NA CONTA --------------------------------------------------------------------------------------------

def entrar_conta(dados):
    print("\n--- ENTRAR NA CONTA ---")

    if dados["utilizadores"]:
        print("Usernames existentes:")
        for utilizador in dados["utilizadores"]:
            print(f"- {utilizador['username']}")
    else:
        print("Ainda não existem contas registadas.")
        return None
    # ----------------------------------------------------
    # USERNAME
    while True:
        username = input("Selecione o seu username: ").strip()

        if username == "":
            print("Erro: o username não pode estar vazio.") # Possivel erro: username estar vazio
            continue
        break

    # PROCURAR UTILIZADOR
    for utilizador in dados["utilizadores"]:
        if utilizador["username"].lower() == username.lower():

            # PASSWORD
            while True:
                password = input("Password: ").strip()

                if password == "":
                    print("Erro: a password não pode estar vazia.") # Possivel erro: password vazio
                    continue

                if password == utilizador["password"]:
                    print(f"\nBem-vinda, {utilizador['nome']}!")
                    return utilizador

                print("Erro: password incorreta.") # Possivel erro: password incorreto
                continue

    print("\nNão existe nenhuma conta registada com esse username.") # Possivel erro: nao existe esse username
    return None

# ========================================================================================================================
#  4 - FUNÇÃO: MENUS (INICIO E DAS PLANTAS)
# ========================================================================================================================

# ----------- MENU INICIAL --------------------------------------------------------------------------------------------

def menu_inicial(dados):
    while True:
        print("\n====================================")
        print(" 🌻 GESTOR DE CUIDADO DE PLANTAS 🌻 ")
        print("====================================")
        print("1. Criar conta")
        print("2. Entrar na conta")
        print("0. Sair")
        print("===================================")
        opcao = input("Por-favor escolha uma opção: ").strip()

        if opcao == "0":
            print("\nObrigado por usar o nosso Gestor de cuidado de plantas!")
            print("A sair do programa...\n")

            break

        elif opcao == "1":
            criar_conta(dados)

        elif opcao == "2":

            utilizador_atual = entrar_conta(dados)

            if utilizador_atual is not None:
                resultado = menu_da_conta(dados, utilizador_atual)

                if resultado == "voltar":
                    continue

# ----------- MENU PLANTAS --------------------------------------------------------------------------------------------

def menu_da_conta(dados, utilizador):

    while True:
        print("\n===================================")
        print("        🌻CUIDADO DE PLANTAS🌻      ")
        print("===================================")
        print(f"Bem-vindo {utilizador['nome']}!")
        print("-----------------------------------")
        print("1. Adicionar planta")
        print("2. Listar plantas")
        print("3. Procurar planta")
        print("4. Atualizar planta")
        print("5. Remover planta")
        print("6. Rega Urgente!")
        print("0. Voltar Atrás")
        print("===================================")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("\nA voltar ao menu inicial...")
            return "voltar"

        elif opcao == "1":
            print("-")

        elif opcao == "2":
            print("-")

        elif opcao == "3":
            print("-")

        elif opcao == "4":
           print("-")

        elif opcao == "5":
            print("-")

        elif opcao == "6":
            print("-")

        else:
            print("Erro: opção inválida.")
# ========================================================================================================================
# PROGRAMA PRINCIPAL
# ========================================================================================================================

dados = carregar_dados()
menu_inicial(dados)