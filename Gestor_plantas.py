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
        print("O ficheiro plantas.json ainda não existe.")  # Possivel erro : Ficheiro JSON nao existe
        print("Será criado automaticamente.")
        return {"utilizadores": [], "plantas": []}

    except json.JSONDecodeError:
        print("Erro: o ficheiro plantas.json contém dados inválidos.") # Possivel erro : Ficheiro JSON com dados invalidos
        print("A aplicação vai começar sem dados.")
        return {"utilizadores": [], "plantas": []}

    except OSError:
        print("Erro ao abrir o ficheiro de dados.")  # Possivel erro : Erro ao abrir o Ficheiro JSON 
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
                continue

        if not username_repetido: #se o username nao estiver repetido avanza
            break

    # GERAR ID
    if len(dados[utilizadores]) == 0:
        novo_id = 1
    else:
        maior_id=0
        for utilizador in dados["utilizadores"]:
            if utilizador["id"] > maior_id:
                maior_id = utilizador["id"]
            novo_id = maior_id + 1

    # CRIAR UTILIZADOR
    utilizador = {
        "id": novo_id,
        "nome": nome,
        "idade": idade,
        "username": username
    }

    dados["utilizadores"].append(utilizador)

    guardar_dados(dados)    # chama a funcao e guarda imediatamente no JSON

    print("\nConta criada com sucesso!")
    print(f"Nome: {nome}")
    print(f"Username: {username}")
    print(f"ID de utilizador: {novo_id}")

# ----------- ENTRAR NA CONTA --------------------------------------------------------------------------------------------

