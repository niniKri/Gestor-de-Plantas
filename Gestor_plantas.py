# Trabalho realizado por Anny Santos

import json
from datetime import datetime, date

FICHEIRO = "plantas.json"

# ============================================================
#  FUNÇÃO: CARREGAR DADOS -> Guarda plantas e as contas 
# ============================================================

#Esta função serve para carregar os dados guardados no ficheiro JSON. 
#Primeiro, tenta abrir e ler o ficheiro. 
#Depois, verifica se os dados estão no formato correto e garante que existem as listas de utilizadores e plantas.
#Caso o ficheiro não exista, esteja inválido ou aconteça algum erro ao abri-lo, a função apresenta uma mensagem e inicia a aplicação com listas vazias.

def carregar_dados():
    try:
        with open(FICHEIRO, "r", encoding="utf-8") as ficheiro:
            dados = json.load(ficheiro)

            if not isinstance(dados, dict):
                print("Erro: o ficheiro JSON está inválido.")
                return {"utilizadores": [], "plantas": []}

            if "utilizadores" not in dados:
                dados["utilizadores"] = []

            if "plantas" not in dados:
                dados["plantas"] = []

            return dados

    except FileNotFoundError:
        print("O ficheiro plantas.json ainda não existe.")
        print("Será criado automaticamente.")
        return {"utilizadores": [], "plantas": []}

    except json.JSONDecodeError:
        print("Erro: o ficheiro plantas.json contém dados inválidos.")
        print("A aplicação vai começar sem dados.")
        return {"utilizadores": [], "plantas": []}

    except OSError:
        print("Erro ao abrir o ficheiro de dados.")
        return {"utilizadores": [], "plantas": []}