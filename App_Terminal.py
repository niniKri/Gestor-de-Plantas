# Trabalho realizado por Anny Santos

import json
from datetime import datetime, date, timedelta

FICHEIRO = "plantas.json"

# ========================================================================================================================
# 1 - FUNÇÃO: CARREGAR DADOS -> Guarda plantas e as contas 
# ========================================================================================================================

def carregar_dados():
    try:
        with open(FICHEIRO, "r", encoding="utf-8") as ficheiro:
            dados = json.load(ficheiro)

            if not isinstance(dados, dict):
                print("Erro: o ficheiro JSON está inválido.") # Possivel erro : Ficheiro JSON invalido
                return {"utilizadores": [], "plantas": []}

            if not isinstance(dados.get("utilizadores"), list):
                dados["utilizadores"] = []

            if not isinstance(dados.get("plantas"), list):
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
        nome = input("Nome: ").strip()
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

    # GERAR ID DO UTILIZADOR
    if not dados["utilizadores"]:
        novo_id = 1
    else:
        novo_id = max([utilizador["id"] for utilizador in dados["utilizadores"]], default=0) + 1
        
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

    print(f"\nA conta de {username} adicionada com sucesso!")

# ----------- ENTRAR NA CONTA --------------------------------------------------------------------------------------------

def entrar_conta(dados):
    print("\n----- ENTRAR NA CONTA ------")

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
        print("-----------------------------------")
        username = input("\nSelecione o seu username: ").strip()

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
        print("1. Criar conta") #✔️
        print("2. Entrar na conta") #✔️
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
        print("       🌻 CUIDADO DE PLANTAS 🌻     ")
        print("===================================")
        print(f"Bem-vindo {utilizador['nome']}!")
        print("-----------------------------------")
        print("1. Adicionar planta")       #✔️
        print("2. Listar plantas")         #✔️
        print("3. Atualizar planta")       #✔️
        print("4. Remover planta")         #✔️
        print("5. Rega Urgente!")          #✔️      
        print("6. Editar o meu Perfil")    #✔️
        print("0. Voltar Atrás")           #✔️
        print("===================================")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("\nA voltar ao menu inicial...")
            return "voltar"

        elif opcao == "1":
            adicionar_planta(dados, utilizador)

        elif opcao == "2":
            listar_plantas(dados, utilizador)

        elif opcao == "3":
            atualizar_planta(dados, utilizador)

        elif opcao == "4":
            remover_planta(dados, utilizador)

        elif opcao == "5":
            rega_urgente(dados, utilizador)

        elif opcao == "6":
            editar_perfil(dados, utilizador)

        else:
            print("Erro: opção inválida.")

# ========================================================================================================================
#  5 - ADICIONAR PLANTAS
# ========================================================================================================================

def adicionar_planta(dados, utilizador):

    print("\n--- ADICIONAR PLANTA 🌱 ---")

    # NOME
    while True:
        nome = input("Nome da planta: ").strip()

        if nome == "":
            print("Erro: o nome não pode estar vazio.") # Possivel erro: estar vazio
            continue

        nome_repetido = False

        for planta in dados["plantas"]:
            if (planta["nome"].lower() == nome.lower()and planta["user_id"] == utilizador["id"]):
                nome_repetido = True
                break

        if nome_repetido:
            print("Erro: já tens uma planta com esse nome.") # Possivel erro: se ja for repetido o nome da planta
            continue

        break

    # TIPO
    while True:
        tipo = input("Tipo de planta: ").strip()

        if tipo == "":
            print("Erro: o tipo não pode estar vazio.") #Possivel erro: estar vazio
            continue

        break

    # CUIDADOS
    cuidados = input("Algum cuidado em específico?: ").strip()

    # DATA DA ÚLTIMA REGA
    while True:

        ultima_rega = input("Data da última rega (AAAA-MM-DD): ").strip()

        if ultima_rega == "":
            print("Erro: a data não pode estar vazia.") # Possivel erro: estar vazio
            continue

        try:
            data = datetime.strptime( ultima_rega, "%Y-%m-%d").date()

            if data > date.today():
                print("Erro: a data não pode ser futura.") # Possivel erro: data errada
                continue

            break

        except ValueError:
            print("Erro: data inválida. " "Utiliza o formato AAAA-MM-DD.") #Possivel erro: Tipo invalido

    # FREQUÊNCIA DE REGA
    while True:
        try:
            frequencia_rega = int(input("Frequência de rega (dias): "))

            if frequencia_rega <= 0:
                print("Erro: a frequência deve ser superior a 0.") # Possivel erro: frequencia inferior a 0 
                continue
            break

        except ValueError:
            print("Erro: a frequência deve ser um número inteiro.") #Possivel erro: nao e numero inteiro

    # GERAR ID DA PLANTA
    if len(dados["plantas"]) == 0:
        novo_id = 1

    else:
        maior_id = 0

        for planta in dados["plantas"]:
            if planta["id"] > maior_id:
                maior_id = planta["id"]

        novo_id = maior_id + 1

    # CRIAR PLANTA
    planta = {
        "id": novo_id,
        "user_id": utilizador["id"],
        "nome": nome,
        "tipo": tipo,
        "cuidados": cuidados,
        "ultima_rega": ultima_rega,
        "frequencia_rega": frequencia_rega,
        "estado": "ativo"
    }

    dados["plantas"].append(planta)

    # GUARDAR AS ALTERAÇÕES
    guardar_dados(dados)

    print(f"{nome} adicionada com sucesso!")

# ========================================================================================================================
#  6 - LISTAR PLANTAS
# ========================================================================================================================

def listar_plantas(dados, utilizador):

    print("\n--- MINHAS PLANTAS ---")

    minhas_plantas = []

    for planta in dados["plantas"]:
        if planta["user_id"] == utilizador["id"]:
            minhas_plantas.append(planta)

    if not minhas_plantas: 
        print("Não tens nenhuma planta registada.")  # Possivel erro: sem plantas registadas
        return

    for planta in minhas_plantas:

        print("\n-----------------------------------")
        print(f"ID:                 {planta['id']}")
        print(f"Nome:               {planta['nome']}")
        print(f"Tipo:               {planta['tipo']}")
        print(f"Cuidados:           {planta['cuidados']}")
        print(f"Última rega:        {planta['ultima_rega']}")
        print(
            f"Frequência de rega: "
            f"{planta['frequencia_rega']} dias"
        )
        print(f"Estado:             {planta['estado']}")

    print("-----------------------------------")
    print(f"Tens un total de {len(minhas_plantas)} plantas")

# ========================================================================================================================
#  7 - ATUALIZAR PLANTA
# ========================================================================================================================

def atualizar_planta(dados, utilizador):

    print("\n--- ATUALIZAR PLANTA ---")

    tem_plantas = False     # Verificar se o utilizador tem plantas

    for planta in dados["plantas"]:
        if planta["user_id"] == utilizador["id"]:
            tem_plantas = True
            break

    if not tem_plantas:
        print("Não tens nenhuma planta registada.")
        return

    #Funciones complementares
    montrar_plantas(dados,utilizador)
    planta_encontrada = procurar_planta(dados, utilizador)

    print("\nDeixa vazio se não quiseres alterar o valor.")

    # NOME
    while True:
        novo_nome = input(f"Novo nome [{planta_encontrada['nome']}]: ").strip()

        if novo_nome == "":
            break

        nome_repetido = False

        for planta in dados["plantas"]:
            if (
                planta != planta_encontrada
                and planta["user_id"] == utilizador["id"]
                and planta["nome"].lower() == novo_nome.lower()
            ):
                nome_repetido = True
                break

        if nome_repetido:
            print("Erro: já tens outra planta com esse nome.")
            continue

        planta_encontrada["nome"] = novo_nome
        break

    # TIPO
    novo_tipo = input(
        f"Novo tipo [{planta_encontrada['tipo']}]: "
    ).strip()

    if novo_tipo != "":
        planta_encontrada["tipo"] = novo_tipo

    # CUIDADOS
    novos_cuidados = input(
        f"Novos cuidados [{planta_encontrada['cuidados']}]: "
    ).strip()

    if novos_cuidados != "":
        planta_encontrada["cuidados"] = novos_cuidados

    # DATA DA ÚLTIMA REGA
    while True:

        nova_data = input( f"Nova data da última rega [{planta_encontrada['ultima_rega']}]: ").strip()

        if nova_data == "":
            break

        try:

            data_rega = datetime.strptime( nova_data,"%Y-%m-%d").date()

            if data_rega > date.today():
                print("Erro: a data não pode ser futura.")
                continue

            planta_encontrada["ultima_rega"] = nova_data
            break

        except ValueError:
            print("Erro: data inválida, utiliza o formato AAAA-MM-DD.")

    # FREQUÊNCIA DE REGA
    while True:
        nova_frequencia = input(f"Nova frequência de rega [{planta_encontrada['frequencia_rega']}]: ").strip()

        if nova_frequencia == "":
            break

        try:
            nova_frequencia = int(nova_frequencia)

            if nova_frequencia <= 0:
                print("Erro: a frequência deve ser superior a 0.")
                continue

            planta_encontrada["frequencia_rega"] = nova_frequencia
            break

        except ValueError:
            print("Erro: a frequência deve ser um número inteiro.")

    guardar_dados(dados)
    print("\nPlanta atualizada com sucesso!")

# =======================================================================================================================
#  8 - REMOVER PLANTA
# ========================================================================================================================

def remover_planta(dados, utilizador):

    print("\n--- REMOVER PLANTA ---")

    tem_plantas = False     # Verificar se o utilizador tem plantas

    for planta in dados["plantas"]:
        if planta["user_id"] == utilizador["id"]:
            tem_plantas = True
            break

    if not tem_plantas:
        print("Não tens nenhuma planta registada.")  #Possivel erro: sem plantas registadas
        return

    # MOSTRAR AS PLANTAS DO UTILIZADOR     -----------------------------------------------------------------------------------------------> transformar en funcion ????
    montrar_plantas(dados,utilizador)
    planta_encontrada = procurar_planta(dados, utilizador)


    # CONFIRMAR ELIMINACAO

    while True:
        confirmacao = input("\nTens a certeza que queres remover esta planta? (s/n): ").strip().lower()

        if confirmacao == "s":
            break

        elif confirmacao == "n":
            print("Operação cancelada.")
            return

        else:
            print("Erro: responde apenas com 's' ou 'n'.") #Possivel erro: so pode responder com s e n

    # REMOVER
    dados["plantas"].remove(planta_encontrada)

    # GUARDAR AS ALTERAÇÕES
    guardar_dados(dados)

    print(f"\nA planta '{planta_encontrada['nome']}' foi removida com sucesso!")

# ========================================================================================================================
# 9 -  EDITAR PERFIL
# ========================================================================================================================

def editar_perfil(dados, utilizador):

    print("\n--- EDITAR O MEU PERFIL ---")
    print("Deixa vazio se não quiseres alterar o valor.")

    # NOME
    while True:
        novo_nome = input(f"Novo nome [{utilizador['nome']}]: ").strip()

        if novo_nome == "":
            break

        if not novo_nome.replace(" ", "").isalpha():
            print("Erro: o nome não pode conter números ou caracteres especiais.") #Possivel erro: nao pode ter carateres
            continue

        utilizador["nome"] = novo_nome
        break

    # IDADE
    while True:
        nova_idade = input(f"Nova idade [{utilizador['idade']}]: ").strip()

        if nova_idade == "":
            break

        try:
            nova_idade = int(nova_idade)
            utilizador["idade"] = nova_idade
            break

        except ValueError:
            print("Erro: a idade deve ser um número inteiro.")  # Possivel erro: nao ser numero inteiro

    # USERNAME
    while True:
        novo_username = input(f"Novo username [{utilizador['username']}]: ").strip()

        if novo_username == "":
            break

        username_repetido = False

        for outro_utilizador in dados["utilizadores"]:
            if (
                outro_utilizador["id"] != utilizador["id"]
                and outro_utilizador["username"].lower()
                == novo_username.lower()
            ):
                username_repetido = True
                break

        if username_repetido:
            print("Erro: esse username já está registado.")  # Possivel erro: ja exisitr esse username no programa
            continue

        utilizador["username"] = novo_username
        break

    # PASSWORD
    while True:
        nova_password = input("Nova password (deixa vazio para manter a atual): ").strip()

        if nova_password == "":
            break

        if len(nova_password) < 6:
            print("Erro: a password deve ter pelo menos 6 caracteres.")  # Possivel erro: nao ter o limite
            continue

        utilizador["password"] = nova_password
        break

    # GUARDAR AS ALTERAÇÕES
    guardar_dados(dados)

    print("\nPerfil atualizado com sucesso!")

# ========================================================================================================================
# 10 - REGA URGENTE
# ========================================================================================================================

def rega_urgente(dados, utilizador):

    print("\n--- 🌧️ REGA DAS PLANTAS ---")
    encontrou_plantas = False

    for planta in dados["plantas"]:
        if planta["user_id"] == utilizador["id"]:
            encontrou_plantas = True

            try:
                ultima_rega = datetime.strptime(planta["ultima_rega"],"%Y-%m-%d").date()
                proxima_rega = ultima_rega + timedelta(days=planta["frequencia_rega"])
                diferenca = (date.today() - proxima_rega).days

                print("\n-----------------------------------")
                print(f"Nome: {planta['nome']}")
                print(f"Tipo: {planta['tipo']}")
                print(f"Última rega: {planta['ultima_rega']}")
                print(f"Frequência de rega: {planta['frequencia_rega']} dias")

                if diferenca > 0:
                    print(f"A rega está atrasada há {diferenca} dias!🥀")

                elif diferenca == 0:
                    print("A planta precisa de ser regada hoje!")

                else:
                    dias_faltam = abs(diferenca)
                    print(f"Faltam {dias_faltam} dias para a próxima rega.")

            except (ValueError, KeyError, TypeError):

                print(f"Erro nos dados da {planta['nome']} ") # Possivel erro: dados da planta

    if not encontrou_plantas:
        print("\nNão tens nenhuma planta registada.") # Possivel erro: planta nao encontrada
    else:
        print("\n-----------------------------------")
# =======================================================================================================================
#  1- fUNCION COMPLEMENTAR - Mostrar plantas
# ========================================================================================================================

def montrar_plantas(dados,utilizador):
    print("As tuas plantas:")
    for planta in dados["plantas"]:
        if planta["user_id"] == utilizador["id"]:
            print(f"- {planta['nome']}")

# =======================================================================================================================
#  2 fUNCION COMPLEMENTAR - Procurar Plantas
# ========================================================================================================================

def procurar_planta(dados, utilizador):

    while True:
        nome_planta = input("Nome da planta: ").strip()

        if nome_planta == "":
            print("Erro: o nome da planta não pode estar vazio.") #Possivel erro: nao pode estar vazio
            continue

        planta_encontrada = None

        for planta in dados["plantas"]:
            if (
                planta["nome"].lower() == nome_planta.lower()
                and planta["user_id"] == utilizador["id"]
            ):
                planta_encontrada = planta
                break

        if planta_encontrada is None:
            print(f"Erro: Não foi encontrada nenhuma planta chamada {nome_planta}.") #Possivel erro: nso foi encontrado planta com esse nome
            continue

        print("\nPlanta encontrada:")
        print(f"Nome: {planta_encontrada['nome']}")
        print(f"Tipo: {planta_encontrada['tipo']}")
        print(f"Cuidados: {planta_encontrada['cuidados']}")
        print(f"Última rega: {planta_encontrada['ultima_rega']}")
        print(f"Frequência de rega: {planta_encontrada['frequencia_rega']} dias")

        return planta_encontrada
# ========================================================================================================================
# PROGRAMA PRINCIPAL
# ========================================================================================================================

dados = carregar_dados()
menu_inicial(dados)