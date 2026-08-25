#Trabalho realizado por Anny Santos

import json
from datetime import datetime, date
FICHEIRO = "plantas.json"

# =====================================================================

#Funciones: 

#1. menu
def menu():
        print("\n--- Gestor de Plantas ---")
        print("1. Adicionar planta")
        print("2. Listar plantas")
        print("3. Procurar planta")
        print("4. Atualizar planta")
        print("5. Remover planta")
        print("0. Sair")


# =====================================================================

#Programa Principal:

while True:
    menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "0": 
        print("A sair do programa...")
        break
        
    elif opcao == "1":
        print("Adicionar planta")

    elif opcao == "2":
        print("Listar plantas")

    elif opcao == "3":
        print("Procurar planta")

    elif opcao == "4":
        print("Atualizar planta")

    elif opcao == "5":
        print("Remover planta")

    else:
        print("Opção inválida. Tente novamente.")
