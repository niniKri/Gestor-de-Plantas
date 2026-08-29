# Trabalho realizado por Anny Santos

# ============================================================
# Indice:
# 
# - Bibliotecas: linha 
# - CONFIGURAÇÕES: LINHA
# - FUNÇÕES AUXILIARES
# - 
# - 
# - 
# - 
# - 
# - 
# - 
# ============================================================


#Corregir:
#1. mensagem de erro do mensagem


# ============================================================
# Bibliotecas necessárias
# ============================================================
import json
from datetime import datetime, date, timedelta
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

# =======================================================================================================================
# CONFIGURAÇÕES
# =======================================================================================================================
FICHEIRO = "plantas.json"

COR_FUNDO = "#D3E6D4"
COR_TITULO = "#303030"
COR_TEXTO = "#222222"
COR_ENTRADA = "#ECB38B"

COR_BOTAO = "#F6CFB3"
COR_BOTAO_HOVER = "#568B52"
COR_BOTAO_SAIDA = "#A87A5C"
COR_BOTAO_SAIDA_HOVER = "#BD8359"

# =======================================================================================================================
# FUNÇÕES AUXILIARES
# =======================================================================================================================

# Botones: 
def criar_botao_base(janela, texto, comando, cor, cor_hover, largura=30):

    #Botao comun:
    botao = tk.Button( 
        janela,
        text=texto,
        width=largura,
        height=2,
        bg=cor,
        fg=COR_TITULO,
        activebackground=cor_hover,
        activeforeground=COR_TITULO,
        relief="flat",
        bd=0,
        highlightthickness=1,
        font=("Inter", 12, "bold"),
        cursor="hand2",
        padx=10,
        pady=5,
        command=comando
    )

    botao.bind(
        "<Enter>",
        lambda evento: botao.config(bg=cor_hover)
    )

    botao.bind(
        "<Leave>",
        lambda evento: botao.config(bg=cor)
    )

    return botao


def criar_botao(janela, texto, comando, largura=30):
    return criar_botao_base(
        janela,
        texto,
        comando,
        COR_BOTAO,
        COR_BOTAO_HOVER,
        largura
    )


def criar_botao_saida(janela, texto, comando, largura=30):
    return criar_botao_base(
        janela,
        texto,
        comando,
        COR_BOTAO_SAIDA,
        COR_BOTAO_HOVER,
        largura
    )

#Imagen fundo:

def colocar_fundo(janela):
    try:
        imagem_fundo = tk.PhotoImage(file="img.png")
        imagem_fundo = imagem_fundo.subsample(2, 2) #Reduz a img a metade
        fundo = tk.Label(janela,image=imagem_fundo)
        fundo.place(x=0,y=0,relwidth=1,relheight=1)
        janela.imagem_fundo = imagem_fundo # NAO ELIMINAR!
        return fundo

    #Possiveis erros:
    except tk.TclError:
        print("Aviso: não foi possível carregar a imagem de fundo.")
        janela.configure(bg=COR_FUNDO)
        return None


def obter_minhas_plantas(dados, utilizador):
    minhas_plantas = []
    for planta in dados["plantas"]:
        if planta.get("user_id") == utilizador["id"]:
            minhas_plantas.append(planta)
    return minhas_plantas


def procurar_planta_por_id(dados, utilizador, planta_id):
    for planta in dados["plantas"]:
        if(planta.get("id") == planta_id and planta.get("user_id") == utilizador["id"]):
            return planta
    return None


def obter_novo_id_plantas(dados):
    if not dados["plantas"]:
        return 1
    maior_id = 0
    for planta in dados["plantas"]:
        try:
            if int(planta.get("id", 0)) > maior_id:
                maior_id = int(planta.get("id", 0))
        except (ValueError, TypeError):
            pass
    return maior_id + 1


def obter_novo_id_utilizador(dados):
    if not dados["utilizadores"]:
        return 1
    maior_id = 0
    for utilizador in dados["utilizadores"]:
        try:
            if int(utilizador.get("id", 0)) > maior_id:
                maior_id = int(utilizador.get("id", 0))
        except (ValueError, TypeError):
            pass
    return maior_id + 1

# =======================================================================================================================
# 1 - CARREGAR DADOS
# =======================================================================================================================

def carregar_dados():
    try:
        with open(FICHEIRO, "r", encoding="utf-8") as ficheiro: # 1 - Abre o ficheiro JSON (ler)
            dados = json.load(ficheiro) 

            if not isinstance(dados, dict): # 2- Verifica se e um dicionario
                messagebox.showerror("Erro! O ficheiro JSON está inválido.") # messagebox -> mostra o erro
                return {"utilizadores": [], "plantas": []}

            if not isinstance(dados.get("utilizadores"), list): # 3- Verifica se Utilizadores e uma lista
                dados["utilizadores"] = []

            if not isinstance(dados.get("plantas"), list): # 4- Verifica se plantas e uma lista
                dados["plantas"] = []

            return dados

    #Possiveis erros:
    except FileNotFoundError: #Ficheiro plantas.json nao existe
        return {"utilizadores": [], "plantas": []}

    except json.JSONDecodeError: #Ficheiro existe, mas o conteudo nao e valido
        messagebox.showerror("Erro! O ficheiro plantas.json contém dados inválidos.")
        return {"utilizadores": [], "plantas": []}

    except OSError: # Quando não se consegue aceder ao ficheiro
        messagebox.showerror("Erro! Não foi possível abrir o ficheiro de dados.")
        return {"utilizadores": [], "plantas": []}

# =======================================================================================================================
# 2 - GUARDAR DADOS
# =======================================================================================================================

def guardar_dados(dados):
    try:
        with open(FICHEIRO, "w", encoding="utf-8") as ficheiro:
            json.dump( #1 - transforma os dados do python e transforma em JSON
                dados, # neste caso utilizadores e plantas
                ficheiro, # onde sera guardado
                indent=4,
                ensure_ascii=False
            )

        return True
    
    #Possiveis erros:
    except OSError:
        messagebox.showerror("Erro! Não foi possível guardar os dados.")
        return False

# =======================================================================================================================
# 3 - MENU INICIAL
# =======================================================================================================================

def menu_inicial(dados):

    janela = tk.Tk() # Cria a janela Principal
    janela.title("Gestor de Cuidado de Plantas")
    janela.geometry("500x400")
    janela.resizable(False, False) #Utilizador nao pode alterar tamanho
    colocar_fundo(janela)

    titulo = tk.Label( #Titulo principal
        janela,
        text="GESTOR DE CUIDADO DE PLANTAS",
        font=("Inter",18, "bold"),
        fg=COR_TITULO,
        bg=COR_FUNDO    )
    titulo.pack(pady=30) #Espacio vertical ao rededor

    # Botão criar conta
    botao_criar_conta = criar_botao(janela,"Criar conta",lambda: janela_criar_conta(dados),25)
    botao_criar_conta.pack(pady=10)

    # Botão entrar
    botao_entrar = criar_botao(janela,"Entrar na conta",lambda: janela_entrar_conta(dados),25)
    botao_entrar.pack(pady=10)


    # Botão sair
    botao_sair = criar_botao_saida(janela,"Sair",janela.destroy,25)
    botao_sair.pack(pady=10)

    janela.mainloop() #Fica sempre aberta 

# =======================================================================================================================
# 4 - CRIAR CONTA
# =======================================================================================================================

def janela_criar_conta(dados):
    janela = tk.Toplevel()
    janela.title("Criar conta")
    janela.geometry("500x600")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)

    #titulo:
    tk.Label(
        janela,
        text="CRIAR CONTA",
        font=("Inter", 18, "bold"),
        bg=COR_FUNDO,
        fg=COR_TITULO
    ).pack(pady=15)

    # NOME
    tk.Label(janela,text="Nome:",bg=COR_FUNDO).pack()
    entrada_nome = tk.Entry(janela, width=35, bg=COR_ENTRADA, font=("Inter", 15))
    entrada_nome.pack(pady=5)

    # IDADE
    tk.Label(janela,text="Idade:",bg=COR_FUNDO).pack()
    entrada_idade = tk.Entry(janela, width=35, bg=COR_ENTRADA, font=("Inter", 15))
    entrada_idade.pack(pady=5)

    # USERNAME
    tk.Label(janela,text="Username:",bg=COR_FUNDO).pack()
    entrada_username = tk.Entry(janela, width=35, bg=COR_ENTRADA, font=("Inter", 15))
    entrada_username.pack(pady=5)

    # PASSWORD
    tk.Label(janela,text="Password:",bg=COR_FUNDO).pack()
    entrada_password = tk.Entry(janela, width=35, show="*", bg=COR_ENTRADA, font=("Inter", 15))
    entrada_password.pack(pady=5)
    # CONFIRMAR PASSWORD
    tk.Label(janela, text="Confirmar Password:", bg=COR_FUNDO).pack()
    entrada_confirmacao = tk.Entry(janela, width=35, show="*", bg=COR_ENTRADA, font=("Inter", 15))
    entrada_confirmacao.pack(pady=5)

    def criar():
        nome = entrada_nome.get().strip()
        idade_texto = entrada_idade.get().strip()
        username = entrada_username.get().strip()
        password = entrada_password.get()
        confirmacao = entrada_confirmacao.get()

        #Possiveis erros:
        #  NOME
        if nome == "":
            messagebox.showerror("Erro! O nome não pode estar vazio.",parent=janela)
            return
        if not nome.replace(" ", "").isalpha():
            messagebox.showerror("Erro! O nome não pode conter números ou caracteres especiais.",parent=janela)
            return

        #  IDADE
        try:
            idade = int(idade_texto)
        except ValueError:
            messagebox.showerror("Erro! A idade deve ser um número inteiro.", parent=janela)
            return
        if idade <= 0:
            messagebox.showerror("Erro! A idade deve ser superior a 0.", parent=janela)
            return

        #  USERNAME
        if username == "":
            messagebox.showerror("Erro! O username não pode estar vazio.", parent=janela)
            return
        for utilizador in dados["utilizadores"]:
            if utilizador.get("username", "").lower() == username.lower():
                messagebox.showerror("Erro! Esse username já está registado.", parent=janela)
                return
            
        #  PASSWORD
        if password == "":
            messagebox.showerror("Erro! A password não pode estar vazia.", parent=janela)
            return
        if len(password) < 6:
            messagebox.showerror("Erro! A password deve ter pelo menos 6 caracteres.",parent=janela)
            return
        if password != confirmacao:
            messagebox.showerror("Erro! As passwords não coincidem.",parent=janela)
            return
        
        #--------------------------------------------------------------

        # GERAR ID
        novo_id = obter_novo_id_utilizador(dados) # Chama a funcao

        # CRIAR UTILIZADOR
        utilizador = {
            "id": novo_id,
            "nome": nome,
            "idade": idade,
            "username": username,
            "password": password
        }
        dados["utilizadores"].append(utilizador)

        if guardar_dados(dados):

            messagebox.showinfo(f"A conta de {username} foi criada com sucesso!",parent=janela)
            janela.destroy()

    #--------------------------------------------------------------
    frame_botoes = tk.Frame(janela, bg=COR_FUNDO)
    frame_botoes.pack(side="bottom", pady=15)

    # BOTÃO CRIAR
    botao_criar = criar_botao(frame_botoes,"Criar conta",criar,25)
    botao_criar.pack(pady=10)

    # BOTÃO CANCELAR
    botao_cancelar = criar_botao_saida(frame_botoes,"Cancelar",janela.destroy,25)
    botao_cancelar.pack(pady=10)

# ============================================================
# 5 - ENTRAR NA CONTA
# ============================================================

# Funcao: Janela para entrar
def janela_entrar_conta(dados):
    janela = tk.Toplevel()
    janela.title("Entrar na conta")
    janela.geometry("500x400")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)

    tk.Label(janela,text="ENTRAR NA CONTA",font=("Inter", 18, "bold"),bg=COR_FUNDO,fg=COR_TITULO).pack(pady=15)
    tk.Label(janela,text="Username:",bg=COR_FUNDO).pack()

    entrada_username = tk.Entry(janela,width=30,bg=COR_ENTRADA,font=("Inter", 15))
    entrada_username.pack(pady=5)

    tk.Label(janela,text="Password:",bg=COR_FUNDO).pack()
    entrada_password = tk.Entry(janela,width=30,show="*",bg=COR_ENTRADA,font=("Inter", 15))
    entrada_password.pack(pady=5)

    # Funcao: Entrar
    def entrar():
        username = entrada_username.get().strip()
        password = entrada_password.get()

        if username == "":
            messagebox.showerror("Erro! O username não pode estar vazio.",parent=janela)
            return

        if password == "":
            messagebox.showerror("Erro! A password não pode estar vazia.",parent=janela)
            return

        for utilizador in dados["utilizadores"]:
            if utilizador.get("username", "").lower() == username.lower():
                if password == utilizador.get("password", ""):
                    janela.destroy()
                    janela_conta(dados,utilizador)
                    return

                else:
                    messagebox.showerror( "Erro! Password incorreta.",parent=janela)
                    return

        messagebox.showerror("Erro! Não existe nenhuma conta registada com esse username.",parent=janela)

    #Botones:
    frame_botoes = tk.Frame(janela, bg=COR_FUNDO)
    frame_botoes.pack(side="bottom")

    botao_entrar = criar_botao(frame_botoes, "Entrar", entrar, 25)
    botao_entrar.pack(pady=10)

    botao_cancelar = criar_botao_saida(frame_botoes,"Cancelar",janela.destroy,25)
    botao_cancelar.pack(pady=10)

# =======================================================================================================================
# 6 - MENU Utilizador
# =======================================================================================================================

def janela_conta(dados, utilizador):

    janela = tk.Toplevel()
    janela.title("Minha conta")
    janela.geometry("500x650")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)

    tk.Label(
        janela,
        text="Gestor de Cuidado de Plantas",
        font=("Arial", 18, "bold"),
        bg=COR_FUNDO,
        fg=COR_TITULO
     ).pack(pady=20)
    
    label_bem_vindo = tk.Label(
        janela,
        text=f"Bem-vindo, {utilizador['nome']}!",
        font=("Arial", 13),
        bg=COR_FUNDO,
        fg=COR_TEXTO
    )
    label_bem_vindo.pack(pady=5)

    # ADICIONAR
    botao = criar_botao(
        janela,
        "Adicionar planta",
        lambda: janela_adicionar_planta(dados, utilizador),
        30
    )
    botao.pack(pady=7)

    # LISTAR
    botao = criar_botao(
        janela,
        "Listar plantas",
        lambda: janela_listar_plantas(dados, utilizador),
        30
    )
    botao.pack(pady=7)

    # ATUALIZAR
    botao = criar_botao(
        janela,
        "Atualizar planta",
        lambda: janela_atualizar_planta(dados, utilizador),
        30
    )
    botao.pack(pady=7)

    # REMOVER
    botao = criar_botao(
        janela,
        "Remover planta",
        lambda: janela_remover_planta(dados, utilizador),
        30
    )
    botao.pack(pady=7)

    # REGA URGENTE
    botao = criar_botao(
        janela,
        "Rega urgente",
        lambda: janela_rega_urgente(dados, utilizador),
        30
    )
    botao.pack(pady=7)

    # EDITAR PERFIL
    botao = criar_botao(
        janela,
        "Editar o meu perfil",
        lambda: janela_editar_perfil(dados, utilizador, label_bem_vindo),
        30
    )
    botao.pack(pady=7)

    # SAIR
    botao = criar_botao(
        janela,
        "Voltar atrás",
        janela.destroy,
        30
    )
    botao.pack(pady=15)

# ============================================================
# 7 - ADICIONAR PLANTA
# ============================================================

def janela_adicionar_planta(dados, utilizador):

    janela = tk.Toplevel()
    janela.title("🌱 Adicionar planta")
    janela.geometry("500x550")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)

    tk.Label(
        janela,
        text="🌱 ADICIONAR PLANTA",
        font=("Arial", 18, "bold"),
        bg=COR_FUNDO
    ).pack(pady=20)

    # NOME
    tk.Label(
        janela,
        text="Nome da planta:",
        bg=COR_FUNDO
    ).pack()

    entrada_nome = tk.Entry(
        janela,
        width=40,
        bg=COR_ENTRADA
    )
    entrada_nome.pack(pady=5)

    # TIPO
    tk.Label(
        janela,
        text="Tipo de planta:",
        bg=COR_FUNDO
    ).pack()

    entrada_tipo = tk.Entry(
        janela,
        width=40,
        bg=COR_ENTRADA
    )
    entrada_tipo.pack(pady=5)

    # CUIDADOS
    tk.Label(
        janela,
        text="Cuidados específicos:",
        bg=COR_FUNDO
    ).pack()

    entrada_cuidados = tk.Entry(
        janela,
        width=40,
        bg=COR_ENTRADA
    )
    entrada_cuidados.pack(pady=5)

    # DATA
    tk.Label(
        janela,
        text="Data da última rega (AAAA-MM-DD):",
        bg=COR_FUNDO
    ).pack()

    entrada_data = tk.Entry(
        janela,
        width=40,
        bg=COR_ENTRADA
    )
    entrada_data.pack(pady=5)

    # FREQUÊNCIA
    tk.Label(
        janela,
        text="Frequência de rega (dias):",
        bg=COR_FUNDO
    ).pack()

    entrada_frequencia = tk.Entry(
        janela,
        width=40,
        bg=COR_ENTRADA
    )
    entrada_frequencia.pack(pady=5)

    def adicionar():

        nome = entrada_nome.get().strip()
        tipo = entrada_tipo.get().strip()
        cuidados = entrada_cuidados.get().strip()
        ultima_rega = entrada_data.get().strip()
        frequencia_texto = entrada_frequencia.get().strip()

        # NOME
        if nome == "":
            messagebox.showerror("Erro! O nome da planta não pode estar vazio.",parent=janela)
            return

        # Verificar nome repetido
        for planta in dados["plantas"]:
            if (planta.get("user_id") == utilizador["id"]and planta.get("nome", "").lower() == nome.lower()):
                messagebox.showerror("Erro! Já tens uma planta com esse nome.",parent=janela)
                return

        # TIPO
        if tipo == "":
            messagebox.showerror("Erro! O tipo da planta não pode estar vazio.",
                parent=janela
            )
            return

        # ----------------------------------------------------
        # DATA
        # ----------------------------------------------------

        if ultima_rega == "":
            messagebox.showerror(
                "Erro",
                "A data da última rega não pode estar vazia.",
                parent=janela
            )
            return

        try:
            data = datetime.strptime(
                ultima_rega,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Data inválida. Utiliza o formato AAAA-MM-DD.",
                parent=janela
            )
            return

        if data > date.today():
            messagebox.showerror(
                "Erro",
                "A data não pode ser futura.",
                parent=janela
            )
            return

        # ----------------------------------------------------
        # FREQUÊNCIA
        # ----------------------------------------------------

        try:
            frequencia_rega = int(frequencia_texto)

        except ValueError:
            messagebox.showerror(
                "Erro",
                "A frequência deve ser um número inteiro.",
                parent=janela
            )
            return

        if frequencia_rega <= 0:
            messagebox.showerror(
                "Erro",
                "A frequência deve ser superior a 0.",
                parent=janela
            )
            return

        # ----------------------------------------------------
        # CRIAR PLANTA
        # ----------------------------------------------------

        nova_planta = {
            "id": obter_novo_id_plantas(dados),
            "user_id": utilizador["id"],
            "nome": nome,
            "tipo": tipo,
            "cuidados": cuidados,
            "ultima_rega": ultima_rega,
            "frequencia_rega": frequencia_rega,
            "estado": "ativo"
        }

        dados["plantas"].append(nova_planta)

        if guardar_dados(dados):

            messagebox.showinfo(
                "Sucesso",
                f"A planta '{nome}' foi adicionada com sucesso!",
                parent=janela
            )

            janela.destroy()

    botao = criar_botao(
        janela,
        "Adicionar planta",
        adicionar,
        25
    )

    botao.pack(pady=20)

    tk.Button(
        janela,
        text="Cancelar",
        width=25,
        command=janela.destroy
    ).pack()


# ============================================================
# 8 - LISTAR PLANTAS
# ============================================================

def janela_listar_plantas(dados, utilizador):

    janela = tk.Toplevel()
    janela.title("Minhas plantas")
    janela.geometry("650x600")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)

    tk.Label(
        janela,
        text="MINHAS PLANTAS",
        font=("Arial", 18, "bold"),
        bg=COR_FUNDO
    ).pack(pady=15)

    minhas_plantas = obter_minhas_plantas(
        dados,
        utilizador
    )

    if not minhas_plantas:

        tk.Label(
            janela,
            text="Não tens nenhuma planta registada.",
            font=("Arial", 13),
            bg=COR_FUNDO
        ).pack(pady=50)

        tk.Button(
            janela,
            text="Fechar",
            width=20,
            command=janela.destroy
        ).pack()

        return

    # FRAME COM SCROLL
    frame_principal = tk.Frame(
        janela,
        bg=COR_FUNDO
    )

    frame_principal.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )

    canvas = tk.Canvas(
        frame_principal,
        bg=COR_FUNDO
    )

    scrollbar = tk.Scrollbar(
        frame_principal,
        orient="vertical",
        command=canvas.yview
    )

    frame_plantas = tk.Frame(
        canvas,
        bg=COR_FUNDO
    )

    frame_plantas.bind(
        "<Configure>",
        lambda evento: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=frame_plantas,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # MOSTRAR PLANTAS
    for planta in minhas_plantas:

        frame = tk.LabelFrame(
            frame_plantas,
            text=f"🌱 {planta.get('nome', 'Sem nome')}",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=15,
            pady=10
        )

        frame.pack(
            fill="x",
            padx=5,
            pady=8
        )

        texto = (
            f"ID: {planta.get('id')}\n"
            f"Tipo: {planta.get('tipo', '')}\n"
            f"Cuidados: {planta.get('cuidados', '')}\n"
            f"Última rega: {planta.get('ultima_rega', '')}\n"
            f"Frequência de rega: "
            f"{planta.get('frequencia_rega', '')} dias\n"
            f"Estado: {planta.get('estado', 'ativo')}"
        )

        tk.Label(
            frame,
            text=texto,
            justify="left",
            anchor="w",
            bg="white",
            font=("Arial", 10)
        ).pack(
            anchor="w"
        )

    tk.Button(
        janela,
        text="Fechar",
        width=20,
        command=janela.destroy
    ).pack(pady=10)


# ============================================================
# 9 - ATUALIZAR PLANTA
# ============================================================

def janela_atualizar_planta(dados, utilizador):

    minhas_plantas = obter_minhas_plantas(
        dados,
        utilizador
    )

    if not minhas_plantas:

        messagebox.showinfo(
            "Informação",
            "Não tens nenhuma planta registada."
        )

        return

    janela = tk.Toplevel()
    janela.title("Atualizar planta")
    janela.geometry("550x650")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)

    tk.Label(
        janela,
        text="✏️ ATUALIZAR PLANTA",
        font=("Arial", 18, "bold"),
        bg=COR_FUNDO
    ).pack(pady=15)

    # --------------------------------------------------------
    # ESCOLHER PLANTA
    # --------------------------------------------------------

    tk.Label(
        janela,
        text="Escolhe a planta:",
        bg=COR_FUNDO
    ).pack()

    lista_plantas = [
        f"{planta['id']} - {planta['nome']}"
        for planta in minhas_plantas
    ]

    variavel_planta = tk.StringVar()

    menu_plantas = tk.OptionMenu(
        janela,
        variavel_planta,
        *lista_plantas
    )

    menu_plantas.config(
        width=35
    )

    menu_plantas.pack(pady=8)

    # --------------------------------------------------------
    # CAMPOS
    # --------------------------------------------------------

    tk.Label(
        janela,
        text="Novo nome:",
        bg=COR_FUNDO
    ).pack()

    entrada_nome = tk.Entry(
        janela,
        width=40,
        bg=COR_ENTRADA
    )
    entrada_nome.pack(pady=5)

    tk.Label(
        janela,
        text="Novo tipo:",
        bg=COR_FUNDO
    ).pack()

    entrada_tipo = tk.Entry(
        janela,
        width=40,
        bg=COR_ENTRADA
    )
    entrada_tipo.pack(pady=5)

    tk.Label(
        janela,
        text="Novos cuidados:",
        bg=COR_FUNDO
    ).pack()

    entrada_cuidados = tk.Entry(
        janela,
        width=40,
        bg=COR_ENTRADA
    )
    entrada_cuidados.pack(pady=5)

    tk.Label(
        janela,
        text="Nova data da última rega:",
        bg=COR_FUNDO
    ).pack()

    entrada_data = tk.Entry(
        janela,
        width=40,
        bg=COR_ENTRADA
    )
    entrada_data.pack(pady=5)

    tk.Label(
        janela,
        text="Nova frequência de rega:",
        bg=COR_FUNDO
    ).pack()

    entrada_frequencia = tk.Entry(
        janela,
        width=40,
        bg=COR_ENTRADA
    )
    entrada_frequencia.pack(pady=5)

    tk.Label(
        janela,
        text="Deixa os campos vazios para manter os valores atuais.",
        bg=COR_FUNDO,
        font=("Arial", 9, "italic")
    ).pack(pady=8)

    def preencher_campos(*args):

        selecao = variavel_planta.get()

        if selecao == "":
            return

        try:
            planta_id = int(
                selecao.split(" - ")[0]
            )
        except ValueError:
            return

        planta = procurar_planta_por_id(
            dados,
            utilizador,
            planta_id
        )

        if planta is None:
            return

        entrada_nome.delete(0, tk.END)
        entrada_nome.insert(0, planta.get("nome", ""))

        entrada_tipo.delete(0, tk.END)
        entrada_tipo.insert(0, planta.get("tipo", ""))

        entrada_cuidados.delete(0, tk.END)
        entrada_cuidados.insert(0, planta.get("cuidados", ""))

        entrada_data.delete(0, tk.END)
        entrada_data.insert(
            0,
            planta.get("ultima_rega", "")
        )

        entrada_frequencia.delete(0, tk.END)
        entrada_frequencia.insert(
            0,
            str(planta.get("frequencia_rega", ""))
        )

    variavel_planta.trace_add(
        "write",
        preencher_campos
    )

    # --------------------------------------------------------
    # ATUALIZAR
    # --------------------------------------------------------

    def atualizar():

        selecao = variavel_planta.get()

        if selecao == "":
            messagebox.showerror(
                "Erro",
                "Seleciona uma planta.",
                parent=janela
            )
            return

        try:
            planta_id = int(
                selecao.split(" - ")[0]
            )
        except ValueError:
            messagebox.showerror(
                "Erro",
                "Planta inválida.",
                parent=janela
            )
            return

        planta = procurar_planta_por_id(
            dados,
            utilizador,
            planta_id
        )

        if planta is None:
            messagebox.showerror(
                "Erro",
                "A planta não foi encontrada.",
                parent=janela
            )
            return

        novo_nome = entrada_nome.get().strip()
        novo_tipo = entrada_tipo.get().strip()
        novos_cuidados = entrada_cuidados.get().strip()
        nova_data = entrada_data.get().strip()
        nova_frequencia = entrada_frequencia.get().strip()

        # ----------------------------------------------------
        # NOME
        # ----------------------------------------------------

        if novo_nome == "":
            messagebox.showerror(
                "Erro",
                "O nome da planta não pode estar vazio.",
                parent=janela
            )
            return

        for outra_planta in minhas_plantas:

            if (
                outra_planta != planta
                and outra_planta.get("nome", "").lower()
                == novo_nome.lower()
            ):
                messagebox.showerror(
                    "Erro",
                    "Já tens outra planta com esse nome.",
                    parent=janela
                )
                return

        # ----------------------------------------------------
        # TIPO
        # ----------------------------------------------------

        if novo_tipo == "":
            messagebox.showerror(
                "Erro",
                "O tipo não pode estar vazio.",
                parent=janela
            )
            return

        # ----------------------------------------------------
        # DATA
        # ----------------------------------------------------

        try:
            data = datetime.strptime(
                nova_data,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Data inválida. Utiliza AAAA-MM-DD.",
                parent=janela
            )
            return

        if data > date.today():
            messagebox.showerror(
                "Erro",
                "A data não pode ser futura.",
                parent=janela
            )
            return

        # ----------------------------------------------------
        # FREQUÊNCIA
        # ----------------------------------------------------

        try:
            frequencia = int(nova_frequencia)

        except ValueError:
            messagebox.showerror(
                "Erro",
                "A frequência deve ser um número inteiro.",
                parent=janela
            )
            return

        if frequencia <= 0:
            messagebox.showerror(
                "Erro",
                "A frequência deve ser superior a 0.",
                parent=janela
            )
            return

        # ----------------------------------------------------
        # GUARDAR
        # ----------------------------------------------------

        planta["nome"] = novo_nome
        planta["tipo"] = novo_tipo
        planta["cuidados"] = novos_cuidados
        planta["ultima_rega"] = nova_data
        planta["frequencia_rega"] = frequencia

        if guardar_dados(dados):

            messagebox.showinfo(
                "Sucesso",
                "Planta atualizada com sucesso!",
                parent=janela
            )

            janela.destroy()

    botao = criar_botao(
        janela,
        "Guardar alterações",
        atualizar,
        25
    )

    botao.pack(pady=15)

    tk.Button(
        janela,
        text="Cancelar",
        width=25,
        command=janela.destroy
    ).pack()


# ============================================================
# 10 - REMOVER PLANTA
# ============================================================

def janela_remover_planta(dados, utilizador):

    minhas_plantas = obter_minhas_plantas(
        dados,
        utilizador
    )

    if not minhas_plantas:

        messagebox.showinfo(
            "Informação",
            "Não tens nenhuma planta registada."
        )

        return

    janela = tk.Toplevel()
    janela.title("🗑️ Remover planta")
    janela.geometry("450x350")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)

    tk.Label(
        janela,
        text="🗑️ REMOVER PLANTA",
        font=("Arial", 18, "bold"),
        bg=COR_FUNDO
    ).pack(pady=25)

    tk.Label(
        janela,
        text="Seleciona a planta:",
        bg=COR_FUNDO
    ).pack()

    lista_plantas = [
        f"{planta['id']} - {planta['nome']}"
        for planta in minhas_plantas
    ]

    variavel_planta = tk.StringVar()

    menu = tk.OptionMenu(
        janela,
        variavel_planta,
        *lista_plantas
    )

    menu.config(
        width=30
    )

    menu.pack(pady=15)

    def remover():

        selecao = variavel_planta.get()

        if selecao == "":
            messagebox.showerror(
                "Erro",
                "Seleciona uma planta.",
                parent=janela
            )
            return

        try:
            planta_id = int(
                selecao.split(" - ")[0]
            )
        except ValueError:
            messagebox.showerror(
                "Erro",
                "Planta inválida.",
                parent=janela
            )
            return

        planta = procurar_planta_por_id(
            dados,
            utilizador,
            planta_id
        )

        if planta is None:
            messagebox.showerror(
                "Erro",
                "A planta não foi encontrada.",
                parent=janela
            )
            return

        confirmacao = messagebox.askyesno(
            "Confirmar remoção",
            f"Tens a certeza que queres remover "
            f"a planta '{planta['nome']}'?",
            parent=janela
        )

        if not confirmacao:
            return

        dados["plantas"].remove(planta)

        if guardar_dados(dados):

            messagebox.showinfo(
                "Sucesso",
                f"A planta '{planta['nome']}' foi removida com sucesso!",
                parent=janela
            )

            janela.destroy()

    botao = criar_botao(
        janela,
        "🗑️ Remover",
        remover,
        25
    )

    botao.pack(pady=15)

    tk.Button(
        janela,
        text="Cancelar",
        width=25,
        command=janela.destroy
    ).pack()


# ============================================================
# 11 - EDITAR PERFIL
# ============================================================

def janela_editar_perfil(
    dados,
    utilizador,
    label_bem_vindo=None
):

    janela = tk.Toplevel()
    janela.title("👤 Editar perfil")
    janela.geometry("500x500")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)

    tk.Label(
        janela,
        text="👤 EDITAR O MEU PERFIL",
        font=("Arial", 18, "bold"),
        bg=COR_FUNDO
    ).pack(pady=20)

    # NOME
    tk.Label(
        janela,
        text="Nome:",
        bg=COR_FUNDO
    ).pack()

    entrada_nome = tk.Entry(
        janela,
        width=35,
        bg=COR_ENTRADA
    )

    entrada_nome.insert(
        0,
        utilizador.get("nome", "")
    )

    entrada_nome.pack(pady=5)

    # IDADE
    tk.Label(
        janela,
        text="Idade:",
        bg=COR_FUNDO
    ).pack()

    entrada_idade = tk.Entry(
        janela,
        width=35,
        bg=COR_ENTRADA
    )

    entrada_idade.insert(
        0,
        str(utilizador.get("idade", ""))
    )

    entrada_idade.pack(pady=5)

    # USERNAME
    tk.Label(
        janela,
        text="Username:",
        bg=COR_FUNDO
    ).pack()

    entrada_username = tk.Entry(
        janela,
        width=35,
        bg=COR_ENTRADA
    )

    entrada_username.insert(
        0,
        utilizador.get("username", "")
    )

    entrada_username.pack(pady=5)

    # PASSWORD
    tk.Label(
        janela,
        text="Nova password:",
        bg=COR_FUNDO
    ).pack()

    entrada_password = tk.Entry(
        janela,
        width=35,
        show="*",
        bg=COR_ENTRADA
    )

    entrada_password.pack(pady=5)

    tk.Label(
        janela,
        text="Deixa a password vazia para manter a atual.",
        font=("Arial", 9, "italic"),
        bg=COR_FUNDO
    ).pack(pady=5)

    def guardar_perfil():

        novo_nome = entrada_nome.get().strip()
        nova_idade_texto = entrada_idade.get().strip()
        novo_username = entrada_username.get().strip()
        nova_password = entrada_password.get()

        # ----------------------------------------------------
        # NOME
        # ----------------------------------------------------

        if novo_nome == "":
            messagebox.showerror(
                "Erro",
                "O nome não pode estar vazio.",
                parent=janela
            )
            return

        if not novo_nome.replace(" ", "").isalpha():
            messagebox.showerror(
                "Erro",
                "O nome não pode conter números ou caracteres especiais.",
                parent=janela
            )
            return

        # ----------------------------------------------------
        # IDADE
        # ----------------------------------------------------

        try:
            nova_idade = int(nova_idade_texto)

        except ValueError:
            messagebox.showerror(
                "Erro",
                "A idade deve ser um número inteiro.",
                parent=janela
            )
            return

        if nova_idade <= 0:
            messagebox.showerror(
                "Erro",
                "A idade deve ser superior a 0.",
                parent=janela
            )
            return

        # ----------------------------------------------------
        # USERNAME
        # ----------------------------------------------------

        if novo_username == "":
            messagebox.showerror(
                "Erro",
                "O username não pode estar vazio.",
                parent=janela
            )
            return

        for outro_utilizador in dados["utilizadores"]:

            if (
                outro_utilizador.get("id") != utilizador.get("id")
                and outro_utilizador.get("username", "").lower()
                == novo_username.lower()
            ):
                messagebox.showerror(
                    "Erro",
                    "Esse username já está registado.",
                    parent=janela
                )
                return

        # ----------------------------------------------------
        # PASSWORD
        # ----------------------------------------------------

        if nova_password != "":
            if len(nova_password) < 6:
                messagebox.showerror(
                    "Erro",
                    "A password deve ter pelo menos 6 caracteres.",
                    parent=janela
                )
                return

            utilizador["password"] = nova_password

        # ----------------------------------------------------
        # ATUALIZAR
        # ----------------------------------------------------

        utilizador["nome"] = novo_nome
        utilizador["idade"] = nova_idade
        utilizador["username"] = novo_username

        if guardar_dados(dados):

            if label_bem_vindo is not None:
                label_bem_vindo.config(
                    text=f"Bem-vindo, {novo_nome}!"
                )

            messagebox.showinfo(
                "Sucesso",
                "Perfil atualizado com sucesso!",
                parent=janela
            )

            janela.destroy()

    botao = criar_botao(
        janela,
        "Guardar alterações",
        guardar_perfil,
        25
    )

    botao.pack(pady=20)

    tk.Button(
        janela,
        text="Cancelar",
        width=25,
        command=janela.destroy
    ).pack()


# ============================================================
# 12 - REGA URGENTE
# ============================================================

def janela_rega_urgente(dados, utilizador):

    janela = tk.Toplevel()
    janela.title("💧 Rega urgente")
    janela.geometry("650x600")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)

    tk.Label(
        janela,
        text="💧 REGA DAS PLANTAS",
        font=("Arial", 18, "bold"),
        bg=COR_FUNDO
    ).pack(pady=15)

    minhas_plantas = obter_minhas_plantas(
        dados,
        utilizador
    )

    if not minhas_plantas:

        tk.Label(
            janela,
            text="Não tens nenhuma planta registada.",
            font=("Arial", 13),
            bg=COR_FUNDO
        ).pack(pady=50)

        tk.Button(
            janela,
            text="Fechar",
            width=20,
            command=janela.destroy
        ).pack()

        return

    # FRAME COM SCROLL
    frame_principal = tk.Frame(
        janela,
        bg=COR_FUNDO
    )

    frame_principal.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )

    canvas = tk.Canvas(
        frame_principal,
        bg=COR_FUNDO
    )

    scrollbar = tk.Scrollbar(
        frame_principal,
        orient="vertical",
        command=canvas.yview
    )

    frame_resultados = tk.Frame(
        canvas,
        bg=COR_FUNDO
    )

    frame_resultados.bind(
        "<Configure>",
        lambda evento: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=frame_resultados,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # --------------------------------------------------------
    # CALCULAR REGA
    # --------------------------------------------------------

    for planta in minhas_plantas:

        frame = tk.LabelFrame(
            frame_resultados,
            text=f"🌱 {planta.get('nome', 'Sem nome')}",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=15,
            pady=10
        )

        frame.pack(
            fill="x",
            padx=5,
            pady=8
        )

        try:

            ultima_rega = datetime.strptime(
                planta["ultima_rega"],
                "%Y-%m-%d"
            ).date()

            frequencia = int(
                planta["frequencia_rega"]
            )

            proxima_rega = (
                ultima_rega
                + timedelta(days=frequencia)
            )

            diferenca = (
                date.today() - proxima_rega
            ).days

            texto = (
                f"Tipo: {planta.get('tipo', '')}\n"
                f"Última rega: {planta['ultima_rega']}\n"
                f"Frequência: {frequencia} dias\n"
                f"Próxima rega: {proxima_rega}"
            )

            tk.Label(
                frame,
                text=texto,
                justify="left",
                anchor="w",
                bg="white",
                font=("Arial", 10)
            ).pack(
                anchor="w"
            )

            if diferenca > 0:

                mensagem = (
                    f"🥀 A rega está atrasada "
                    f"há {diferenca} dias!"
                )

            elif diferenca == 0:

                mensagem = (
                    "💧 A planta precisa de ser "
                    "regada hoje!"
                )

            else:

                dias_faltam = abs(diferenca)

                mensagem = (
                    f"🌿 Faltam {dias_faltam} dias "
                    f"para a próxima rega."
                )

            tk.Label(
                frame,
                text=mensagem,
                font=("Arial", 10, "bold"),
                bg="white"
            ).pack(
                anchor="w",
                pady=(8, 0)
            )

        except (
            ValueError,
            KeyError,
            TypeError
        ):

            tk.Label(
                frame,
                text="❌ Erro nos dados desta planta.",
                bg="white",
                fg="red",
                font=("Arial", 10, "bold")
            ).pack(
                anchor="w"
            )

    tk.Button(
        janela,
        text="Fechar",
        width=20,
        command=janela.destroy
    ).pack(pady=10)


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    dados = carregar_dados()

    menu_inicial(dados)
