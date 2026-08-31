# Trabalho realizado por Anny Santos

# ============================================================
# Indice:# 
# - Bibliotecas:                    linha 24
# - Configurações:                  linha 37
# - Funções auxiliares:             linha 53
# - Carregar dados:                 linha 
# - Guardar dados:                  linha 
# - Menu inicial:                   linha 
# - Criar conta:                    linha 
# - Entrar na conta:                linha 
# - Menu do utilizador:             linha 
# - Adicionar planta:               linha 
# - Listar plantas:                 linha 
# - Atualizar planta:               linha 
# - Remover planta:                 linha 
# - Editar perfil:                  linha 
# - Rega urgente:                   linha 
# - Programa principal:             linha 
# ============================================================

# =======================================================================================================================
# Bibliotecas necessárias
# =======================================================================================================================

import json
from datetime import datetime, date, timedelta
from tkinter import messagebox
import tkinter as tk                             #Nota: envez de escrever tkinter.Tk() escrevo tk.Tk() 
import os
import shutil
from tkinter import filedialog

# =======================================================================================================================
# CONFIGURAÇÕES
# =======================================================================================================================

FICHEIRO = "plantas.json"

COR_FUNDO = "#D3E6D4"
COR_TITULO = "#303030"
COR_TEXTO = "#303030"
COR_ENTRADA = "#FFF0E5"
COR_PREENCHER= "#F6CFB3"
COR_BOTAO = "#F6CFB3"
COR_BOTAO_HOVER = "#568B52"
COR_BOTAO_SAIDA = "#A87A5C"
COR_BOTAO_SAIDA_HOVER = "#D44E4E"

# =======================================================================================================================
# FUNÇÕES AUXILIARES
# =======================================================================================================================

# Botones: 
#-----Botao comun:
def criar_botao_base(janela, texto, comando, cor, cor_hover, largura=30):
    botao = tk.Button( 
        janela,
        text=texto,
        width=largura,
        height=2,
        bg=cor, # tenho de por isto aqui pra que ao abrir o programa o botao n seja branco
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
    #Interatividade do botao com o rato
    botao.bind("<Enter>",lambda evento: botao.config(bg=cor_hover)) #raton clicado
    botao.bind("<Leave>",lambda evento: botao.config(bg=cor)) #volta ao original
    return botao

#-----Botao de entrar
def criar_botao(janela, texto, comando, largura=30):
    return criar_botao_base(
        janela,
        texto,
        comando,
        COR_BOTAO,
        COR_BOTAO_HOVER,
        largura
    )

#-----Botao de saida
def criar_botao_saida(janela, texto, comando, largura=30):
    return criar_botao_base(
        janela,
        texto,
        comando,
        COR_BOTAO_SAIDA,
        COR_BOTAO_SAIDA_HOVER,
        largura
    )

#-----Imagen fundo:
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

#-----Encontrar plantas de dado utilizador
def obter_minhas_plantas(dados, utilizador):
    minhas_plantas = []
    for planta in dados["plantas"]:
        if planta.get("user_id") == utilizador["id"]:
            minhas_plantas.append(planta)
    return minhas_plantas

#----- Busca plantas por id 
def procurar_planta_por_id(dados, utilizador, planta_id):
    for planta in dados["plantas"]:
        if(planta.get("id") == planta_id and planta.get("user_id") == utilizador["id"]):
            return planta
    return None

#....... cada planta com id diferente : adicionar planta
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

#....... cada utilizador com id diferente : criar conta
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

#....... cria zona para fazer scroll em : listas e rega urgente
def criar_area_scroll(janela):
    frame_principal = tk.Frame(janela, bg=COR_FUNDO)
    frame_principal.pack(fill="both", expand=True, padx=15, pady=10)

    canvas = tk.Canvas(frame_principal, bg=COR_FUNDO, highlightthickness=0)
    scrollbar = tk.Scrollbar(frame_principal,orient="vertical",command=canvas.yview)

    frame_resultados = tk.Frame(canvas, bg=COR_FUNDO)
    frame_resultados.bind( "<Configure>", lambda evento: canvas.configure(scrollregion=canvas.bbox("all")))

    janela_canvas = canvas.create_window((0, 0),window=frame_resultados,anchor="nw")

    def ajustar_largura(evento):
        canvas.itemconfig(janela_canvas, width=evento.width)

    canvas.bind("<Configure>", ajustar_largura)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return frame_resultados

#....... Funcao auxiliar para mudar a cor do botao no menu 
def existem_plantas_para_regar(dados, utilizador):
    minhas_plantas = obter_minhas_plantas(dados, utilizador)

    for planta in minhas_plantas:
        try:
            ultima_rega = datetime.strptime(planta["ultima_rega"], "%Y-%m-%d").date()
            frequencia = int(planta["frequencia_rega"])
            proxima_rega = ultima_rega + timedelta(days=frequencia)
            # Se hoje já chegou ou passou da data da próxima rega
            if date.today() >= proxima_rega:
                return True

        except (ValueError, KeyError, TypeError):
            pass

    return False

# =======================================================================================================================
# 1 - CARREGAR DADOS
# =======================================================================================================================

def carregar_dados():
    try:
        with open(FICHEIRO, "r", encoding="utf-8") as ficheiro: # 1 - Abre o ficheiro JSON (ler)
            dados = json.load(ficheiro) 

            if not isinstance(dados, dict): # 2- Verifica se e um dicionario
                messagebox.showerror("Erro","O ficheiro JSON está inválido.") # messagebox -> mostra o erro
                return {"utilizadores": [], "plantas": []}

            if not isinstance(dados.get("utilizadores"), list): # 3- Verifica se Utilizadores e uma lista
                dados["utilizadores"] = []

            if not isinstance(dados.get("plantas"), list): # 4- Verifica se plantas e uma lista
                dados["plantas"] = []

            return dados

    #.......Possiveis erros:
    except FileNotFoundError: #Ficheiro plantas.json nao existe
        return {"utilizadores": [], "plantas": []}

    except json.JSONDecodeError: #Ficheiro existe, mas o conteudo nao e valido
        messagebox.showerror("Erro","O ficheiro plantas.json contém dados inválidos.")
        return {"utilizadores": [], "plantas": []}

    except OSError: # Quando não se consegue aceder ao ficheiro
        messagebox.showerror("Erro","Não foi possível abrir o ficheiro de dados.")
        return {"utilizadores": [], "plantas": []}

# =======================================================================================================================
# 2 - GUARDAR DADOS
# =======================================================================================================================

def guardar_dados(dados):
    try:
        with open(FICHEIRO, "w", encoding="utf-8") as ficheiro:
            json.dump( dados, ficheiro, indent=4,ensure_ascii=False) #transforma os dados do python e transforma em JSON
        return True
    
    #.......Possiveis erros:
    except OSError:
        messagebox.showerror("Erro","Não foi possível guardar os dados.")
        return False

# =======================================================================================================================
# 3 - MENU INICIAL
# =======================================================================================================================

def menu_inicial(dados):
    #----- 1 parte Janela
    janela = tk.Tk() 
    janela.title("Gestor de Cuidado de Plantas")
    janela.geometry("500x400")
    janela.resizable(False, False)
    colocar_fundo(janela)

     #----- 2 parte titulo principal
    titulo = tk.Label( 
        janela,
        text="GESTOR DE CUIDADO DE PLANTAS",
        font=("Inter",18, "bold"),
        fg=COR_TITULO,
        bg=COR_FUNDO    )
    titulo.pack(pady=30) 

    #----- 4 Botones
    botao_criar_conta = criar_botao(janela,"Criar conta",lambda: janela_criar_conta(dados),25)
    botao_criar_conta.pack(pady=10)

    botao_entrar = criar_botao(janela,"Entrar na conta",lambda: janela_entrar_conta(dados),25)
    botao_entrar.pack(pady=10)

    botao_sair = criar_botao_saida(janela,"Sair",janela.destroy,25)
    botao_sair.pack(pady=10)

    #.......Fica sempre aberta 
    janela.mainloop() 

# =======================================================================================================================
# 4 - CRIAR CONTA
# =======================================================================================================================

def janela_criar_conta(dados):
    #----- 1 parte Janela
    janela = tk.Toplevel()
    janela.title("Criar conta")
    janela.geometry("500x600")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)

    #----- 2 parte titulo Principal:
    tk.Label(janela, text="CRIAR CONTA",font=("Inter", 18, "bold"),bg=COR_FUNDO,fg=COR_TITULO ).pack(pady=15)

    #....... NOME
    tk.Label(janela,text="Nome:",bg=COR_FUNDO,font=("Inter", 12, "bold"),width=35, anchor="w").pack()
    entrada_nome = tk.Entry(janela, width=35,bg=COR_PREENCHER, font=("Inter", 15))
    entrada_nome.pack(pady=5)

    #....... USERNAME
    tk.Label(janela,text="Username:",bg=COR_FUNDO,font=("Inter", 12, "bold"),width=35,anchor="w").pack()
    entrada_username =tk.Entry(janela, width=35,bg=COR_PREENCHER, font=("Inter", 15))
    entrada_username.pack(pady=5)

    #....... PASSWORD
    tk.Label(janela,text="Password:",bg=COR_FUNDO,font=("Inter", 12, "bold"),width=35,anchor="w").pack()
    entrada_password = tk.Entry(janela, width=35,bg=COR_PREENCHER, font=("Inter", 15))
    entrada_password.pack(pady=5)

    #.......CONFIRMAR PASSWORD
    tk.Label(janela, text="Confirmar Password:", bg=COR_FUNDO,font=("Inter", 12, "bold"), width=35,anchor="w").pack()
    entrada_confirmacao = tk.Entry(janela, width=35,bg=COR_PREENCHER, font=("Inter", 15))
    entrada_confirmacao.pack(pady=5)

    #----- Criar utilizador na JSON 
    def criar():
        nome = entrada_nome.get().strip()
        username = entrada_username.get().strip()
        password = entrada_password.get()
        confirmacao = entrada_confirmacao.get()

        #Possiveis erros:

        #.......NOME
        if nome == "":
            messagebox.showerror("Erro","O nome não pode estar vazio.",parent=janela)
            return
        if not nome.replace(" ", "").isalpha():
            messagebox.showerror("Erro","O nome não pode conter números ou caracteres especiais.",parent=janela)
            return

        #.......USERNAME
        if username == "":
            messagebox.showerror("Erro","O username não pode estar vazio.", parent=janela)
            return
        for utilizador in dados["utilizadores"]:
            if utilizador.get("username", "").lower() == username.lower():
                messagebox.showerror("Erro","Esse username já está registado.", parent=janela)
                return
            
        #.......PASSWORD
        if password == "":
            messagebox.showerror("Erro","A password não pode estar vazia.", parent=janela)
            return
        if len(password) < 6:
            messagebox.showerror("Erro","A password deve ter pelo menos 6 caracteres.",parent=janela)
            return
        if password != confirmacao:
            messagebox.showerror("Erro","As passwords não coincidem.",parent=janela)
            return

        #.......GERAR ID
        novo_id = obter_novo_id_utilizador(dados) # Chama a funcao

        #.......CRIAR UTILIZADOR
        utilizador = {
            "id": novo_id,
            "nome": nome,
            "username": username,
            "password": password
        }

        #.......Depois de validar os erros - guarda no JSON
        dados["utilizadores"].append(utilizador)
        if guardar_dados(dados):
            messagebox.showinfo("Cuidado de Plantas", f"A conta de {username} foi criada com sucesso!", parent=janela)
            janela.destroy()

    #----- 4 Botones
    frame_botoes = tk.Frame(janela, bg=COR_FUNDO)
    frame_botoes.pack(side="bottom", pady=15)

    # BOTÃO CRIAR
    botao_criar = criar_botao(frame_botoes,"Criar conta",criar,25)
    botao_criar.pack(pady=10)

    # BOTÃO CANCELAR
    botao_cancelar = criar_botao_saida(frame_botoes,"Cancelar",janela.destroy,25)
    botao_cancelar.pack(pady=10)

# =======================================================================================================================
# 5 - ENTRAR NA CONTA
# =======================================================================================================================

def janela_entrar_conta(dados):
    #----- 1 parte Janela
    janela = tk.Toplevel()
    janela.title("Entrar na conta")
    janela.geometry("500x400")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)

    #----- 2 parte titulo Principal:
    tk.Label(janela, text="ENTRAR NA CONTA",font=("Inter", 18, "bold"),bg=COR_FUNDO,fg=COR_TITULO ).pack(pady=15)

    #....... Username
    tk.Label(janela,text="Username:",bg=COR_FUNDO,font=("Inter", 12, "bold"),width=35,anchor="w").pack()
    entrada_username =  tk.Entry(janela, width=35,bg=COR_PREENCHER, font=("Inter", 15))
    entrada_username.pack(pady=5)

    #....... Password
    tk.Label(janela,text="Password:",bg=COR_FUNDO,font=("Inter", 12, "bold"),width=35,anchor="w").pack()
    entrada_password =  tk.Entry(janela, width=35,bg=COR_PREENCHER, font=("Inter", 15))
    entrada_password.pack(pady=5)

    #....... Funcao: Entrar
    def entrar():
        username = entrada_username.get().strip()
        password = entrada_password.get()

        for utilizador in dados["utilizadores"]:
            if utilizador.get("username", "").lower() == username.lower():
                if password == utilizador.get("password", ""):
                    janela.destroy()
                    janela_conta(dados,utilizador)
                    return
                else:
                    messagebox.showerror("Erro","Password incorreta.",parent=janela)
                    return
        messagebox.showerror("Erro","Não existe nenhuma conta registada com esse username.",parent=janela)

        #.......Possiveis erros:
        if username == "":
            messagebox.showerror("Erro","O username não pode estar vazio.",parent=janela)
            return

        if password == "":
            messagebox.showerror("Erro","A password não pode estar vazia.",parent=janela)
            return
        
    #----- 4 Botones:
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
    #----- 1 parte Janela
    janela = tk.Toplevel()
    janela.title("Minha conta")
    janela.geometry("500x650")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)

    #----- 2 parte titulo Principal:
    tk.Label(janela,text="Gestor de Cuidado de Plantas",font=("Inter", 18, "bold"),bg=COR_FUNDO,fg=COR_TITULO).pack(pady=20)

    #....... Texto a saludar
    label_bem_vindo = tk.Label(janela,text=f"Bem-vindo, {utilizador['nome']}!",font=("Inter", 13,"bold"),bg=COR_FUNDO,fg=COR_TEXTO)
    label_bem_vindo.pack(pady=5)

    #....... ADICIONAR
    botao = criar_botao(janela,"Adicionar planta",lambda: janela_adicionar_planta(dados, utilizador),30)
    botao.pack(pady=7)

    #....... LISTAR
    botao = criar_botao(janela,"Listar plantas",lambda: janela_listar_plantas(dados, utilizador),30)
    botao.pack(pady=7)

    #....... ATUALIZAR
    botao = criar_botao(janela,"Atualizar planta",lambda: janela_atualizar_planta(dados, utilizador),30)
    botao.pack(pady=7)

    #....... REMOVER
    botao = criar_botao(janela,"Remover planta",lambda: janela_remover_planta(dados, utilizador),30)
    botao.pack(pady=7)

    #....... REGA URGENTE
    if existem_plantas_para_regar(dados, utilizador):
        botao = criar_botao_base(janela,"Rega urgente",lambda: janela_rega_urgente(dados, utilizador),COR_BOTAO_SAIDA,COR_BOTAO_SAIDA_HOVER,30 )
    else:
        botao = criar_botao(janela,"Rega urgente",lambda: janela_rega_urgente(dados, utilizador),30)

    botao.pack(pady=7)

    #....... EDITAR PERFIL
    botao = criar_botao(janela,"Editar o meu perfil",lambda: janela_editar_perfil(dados, utilizador, label_bem_vindo),30)
    botao.pack(pady=7)

    #----- 4 Botones:
    botao = criar_botao_saida(janela,"Fechar",janela.destroy,30)
    botao.pack(pady=15)

# =======================================================================================================================
# 7 - ADICIONAR PLANTA
# =======================================================================================================================

def janela_adicionar_planta(dados, utilizador):
    #----- 1 parte Janela
    janela = tk.Toplevel()
    janela.title("Adicionar planta")
    janela.geometry("600x700")
    janela.resizable(False, False)
    foto_planta = None
    janela.configure(bg=COR_FUNDO)

    #----- 2 parte titulo Principal:
    tk.Label(janela,text="ADICIONAR PLANTA",font=("Inter", 18, "bold"),bg=COR_FUNDO).pack(pady=20)

    #....... NOME
    tk.Label(janela,text="Nome da planta:",bg=COR_FUNDO,font=("Inter", 12, "bold"),width=35,anchor="w").pack()
    entrada_nome = tk.Entry(janela, width=35,bg=COR_PREENCHER, font=("Inter", 15))
    entrada_nome.pack(pady=5)

    #....... TIPO
    tk.Label(janela,text="Tipo de planta:",bg=COR_FUNDO,font=("Inter", 12, "bold"),width=35,anchor="w").pack()
    entrada_tipo = tk.Entry(janela, width=35,bg=COR_PREENCHER, font=("Inter", 15))
    entrada_tipo.pack(pady=5)

    #....... CUIDADOS
    tk.Label(janela,text="Cuidados específicos:",bg=COR_FUNDO,font=("Inter", 12, "bold"),width=35,anchor="w").pack()
    entrada_cuidados = tk.Entry(janela, width=35,bg=COR_PREENCHER, font=("Inter", 15))
    entrada_cuidados.pack(pady=5)

    #....... DATA
    tk.Label(janela,text="Data da última rega (AAAA-MM-DD):",bg=COR_FUNDO,font=("Inter", 12, "bold"),width=35,anchor="w").pack()
    entrada_data = tk.Entry(janela, width=35,bg=COR_PREENCHER, font=("Inter", 15))
    entrada_data.pack(pady=5)

    #....... FREQUÊNCIA
    tk.Label(janela,text="Frequência de rega (dias):",bg=COR_FUNDO,font=("Inter", 12, "bold"),width=35,anchor="w").pack()
    entrada_frequencia = tk.Entry(janela, width=35,bg=COR_PREENCHER, font=("Inter", 15))
    entrada_frequencia.pack(pady=5)

    #....... FOTO
    tk.Label(janela, text="Foto da planta:",bg=COR_FUNDO,font=("Inter", 12, "bold"),width=35,anchor="w").pack()

    label_foto = tk.Label(janela, text="Nenhuma foto selecionada", bg=COR_FUNDO)
    label_foto.pack(pady=5)

    def escolher_foto():
        nonlocal foto_planta
        caminho = filedialog.askopenfilename(
            title="Escolher foto da planta",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg"),("PNG", "*.png"),("JPG", "*.jpg"),("JPEG", "*.jpeg")])
        if caminho:
            foto_planta = caminho
            label_foto.config(text=os.path.basename(caminho))

    botao_foto = criar_botao(janela, "Escolher foto", escolher_foto, 15)
    botao_foto.pack(pady=5)

    #....... adiconar ao JSON
    def adicionar():
        nome = entrada_nome.get().strip()
        tipo = entrada_tipo.get().strip()
        cuidados = entrada_cuidados.get().strip()
        ultima_rega = entrada_data.get().strip()
        frequencia_texto = entrada_frequencia.get().strip()

        #....... NOME
        if nome == "":
            messagebox.showerror("Erro","O nome da planta não pode estar vazio.",parent=janela)
            return

        #....... Verificar nome repetido
        for planta in dados["plantas"]:
            if (planta.get("user_id") == utilizador["id"]and planta.get("nome", "").lower() == nome.lower()):
                messagebox.showerror("Erro","Já tens uma planta com esse nome.",parent=janela)
                return

        #.......ERRROS POSSIVEIS:
        #.......TIPO
        if tipo == "":
            messagebox.showerror("Erro! O tipo da planta não pode estar vazio.",parent=janela)
            return

        #....... DATA
        if ultima_rega == "":
            messagebox.showerror("Erro","A data da última rega não pode estar vazia.",parent=janela)
            return
        try:
            data = datetime.strptime(ultima_rega,"%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Erro","Data inválida. Utiliza o formato AAAA-MM-DD.",parent=janela)
            return
        if data > date.today():
            messagebox.showerror("Erro","A data não pode ser futura.",parent=janela
            )
            return

        #....... FREQUÊNCIA
        try:
            frequencia_rega = int(frequencia_texto)
        except ValueError:
            messagebox.showerror("Erro","A frequência deve ser um número inteiro.",parent=janela )
            return
        if frequencia_rega <= 0:
            messagebox.showerror("Erro","A frequência deve ser superior a 0.",parent=janela)
            return

        #....... CRIAR PLANTA
        nova_planta = {
            "id": obter_novo_id_plantas(dados),
            "user_id": utilizador["id"],
            "nome": nome,
            "tipo": tipo,
            "cuidados": cuidados,
            "ultima_rega": ultima_rega,
            "frequencia_rega": frequencia_rega,
            "estado": "ativo",
            "foto": foto_planta
        }
        dados["plantas"].append(nova_planta)

        if guardar_dados(dados):
            messagebox.showinfo("Cuidado de Plantas", f"A planta '{nome}' foi adicionada com sucesso!", parent=janela)
            janela.destroy()

    #----- 4 Botones:
    frame_botoes = tk.Frame(janela, bg=COR_FUNDO)
    frame_botoes.pack(side="bottom")

    botao_entrar = criar_botao(frame_botoes, "Adicionar planta", adicionar, 25)
    botao_entrar.pack(pady=10)

    botao_cancelar = criar_botao_saida(frame_botoes,"Cancelar",janela.destroy,25)
    botao_cancelar.pack(pady=10)

# =======================================================================================================================
# 8 - LISTAR PLANTAS
# =======================================================================================================================

def janela_listar_plantas(dados, utilizador):
    #----- 1 parte Janela
    janela = tk.Toplevel()
    janela.title("Minhas plantas")
    janela.geometry("650x600")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)

    #----- 2 parte titulo Principal:
    tk.Label(janela, text="MINHAS PLANTAS", font=("Inter", 18, "bold"), bg=COR_FUNDO, fg=COR_TITULO).pack(pady=15)

    #.......Obter as plantas do utilizador
    minhas_plantas = obter_minhas_plantas(dados, utilizador)
    
    #.......Se nao tem plantas
    if not minhas_plantas:
        tk.Label(janela, text="Não tens nenhuma planta registada.", font=("Inter", 13), bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=50)

        botao_fechar = criar_botao_saida(janela, "Fechar", janela.destroy, 15)
        botao_fechar.pack(pady=10)
        return
    
    #.......chama funcao auxiliar para a area com scroll
    frame_plantas = criar_area_scroll(janela)

    #....... Para cada planta das mihas criar a tabelita
    for planta in minhas_plantas:
        frame = tk.Frame(frame_plantas, bg=COR_PREENCHER, padx=15, pady=10)
        frame.pack(fill="x", padx=5, pady=8)

        tk.Label(frame, text=planta.get("nome", "Sem nome"), font=("Inter", 13, "bold"), bg=COR_PREENCHER, fg=COR_TITULO, anchor="w").pack(fill="x", pady=(0, 10))

        frame_conteudo = tk.Frame(frame, bg=COR_PREENCHER)
        frame_conteudo.pack(fill="x")

        caminho_foto = planta.get("foto")

        #.......Verifica se existe a foto
        if caminho_foto and os.path.exists(caminho_foto):
            try:
                imagem = tk.PhotoImage(file=caminho_foto)
                largura = imagem.width()
                altura = imagem.height()
                if largura > 180 or altura > 180:
                    fator = max(largura // 180, altura // 180)
                    if fator < 1:
                        fator = 1
                    imagem = imagem.subsample(fator, fator)

                label_imagem = tk.Label(frame_conteudo, image=imagem, bg=COR_PREENCHER)
                label_imagem.image = imagem
                label_imagem.pack(side="left", padx=(0, 20))

            except tk.TclError:
                tk.Label(frame_conteudo, text="Imagem inválida", bg=COR_PREENCHER, fg=COR_TITULO).pack(side="left", padx=(0, 20))

        else:
            tk.Label(frame_conteudo, text="Sem foto", width=15, height=7, bg=COR_PREENCHER, fg=COR_TITULO).pack(side="left", padx=(0, 20))

        #....... texto nas tabelas
        texto_widget = tk.Text(frame_conteudo,bg=COR_PREENCHER,fg=COR_TEXTO,font=("Inter", 10), wrap="word", height=5,width=45, bd=0, highlightthickness=0  )
        texto_widget.pack(side="left", fill="both", expand=True)

        #....... Definir estilo bold
        texto_widget.tag_configure("bold", font=("Inter", 10, "bold"))

        ##.......Tipo
        texto_widget.insert("end", "Tipo:", "bold")
        texto_widget.insert("end", f" {planta.get('tipo', '')}\n")

        #.......Cuidados
        texto_widget.insert("end", "Cuidados:", "bold")
        texto_widget.insert("end", f" {planta.get('cuidados', '')}\n")

        #.......Última rega
        texto_widget.insert("end", "Última rega:", "bold")
        texto_widget.insert("end", f" {planta.get('ultima_rega', '')}\n")

        #....... Frequência de rega
        texto_widget.insert("end", "Frequência de rega:", "bold")
        texto_widget.insert("end", f" {planta.get('frequencia_rega', '')} dias\n")

        # Impedir edição
        texto_widget.config(state="disabled")

    #----- 4 Botones:
    frame_botoes = tk.Frame(janela, bg=COR_FUNDO)
    frame_botoes.pack(side="bottom")

    botao_fechar = criar_botao_saida(janela, "Fechar", janela.destroy, 20)
    botao_fechar.pack(pady=10)

# =======================================================================================================================
# 9 - ATUALIZAR PLANTA
# =======================================================================================================================

def janela_atualizar_planta(dados, utilizador):
    #----- 1 parte Janela
    janela=tk.Toplevel()
    janela.title("Atualizar planta")
    janela.geometry("550x650")
    janela.resizable(False,False)
    janela.configure(bg=COR_FUNDO)

    #----- 2 parte titulo Principal:
    tk.Label(janela,text="ATUALIZAR PLANTA",font=("Inter",18,"bold"),bg=COR_FUNDO).pack(pady=15)

    #....... Obter as plantas do utilizador
    minhas_plantas=obter_minhas_plantas(dados,utilizador)

    #.......Se não tiver plantas
    if not minhas_plantas: 
        messagebox.showinfo("Aviso","Não tens nenhuma planta registada.",parent=janela) 
        janela.destroy() 
        return

    #.......Escolher planta
    tk.Label(janela,text="Escolhe a planta:",bg=COR_FUNDO).pack()

    #....... Lista apenas com os nomes
    nomes_plantas=[planta["nome"] for planta in minhas_plantas]
    variavel_planta=tk.StringVar()
    menu_plantas=tk.OptionMenu(janela,variavel_planta,*nomes_plantas) #menu dezplasable
    menu_plantas.config(width=35)
    menu_plantas.pack(pady=5)

    #.......Atualizar novo nome 
    tk.Label(janela,text="Novo nome:",bg=COR_FUNDO,font=("Inter",12,"bold"),width=35,anchor="w").pack() 
    entrada_nome=tk.Entry(janela,width=35,bg=COR_PREENCHER,font=("Inter",15))
    entrada_nome.pack(pady=5)

    #.......Atualizar novo tipo 
    tk.Label(janela,text="Novo tipo:",bg=COR_FUNDO,font=("Inter",12,"bold"),width=35,anchor="w").pack()
    entrada_tipo=tk.Entry(janela,width=35,bg=COR_PREENCHER,font=("Inter",15))
    entrada_tipo.pack(pady=5)

    #.......Atualizar novo cuidados 
    tk.Label(janela,text="Novos cuidados:",bg=COR_FUNDO,font=("Inter",12,"bold"),width=35,anchor="w").pack()
    entrada_cuidados=tk.Entry(janela,width=35,bg=COR_PREENCHER,font=("Inter",15))
    entrada_cuidados.pack(pady=5)

    #.......Atualizar novo data 
    tk.Label(janela,text="Nova data da última rega:",bg=COR_FUNDO,font=("Inter",12,"bold"),width=35,anchor="w").pack()
    entrada_data=tk.Entry(janela,width=35,bg=COR_PREENCHER,font=("Inter",15))
    entrada_data.pack(pady=5)

    #.......Atualizar novo frequência 
    tk.Label(janela,text="Nova frequência de rega:",bg=COR_FUNDO,font=("Inter",12,"bold"),width=35,anchor="w").pack()
    entrada_frequencia=tk.Entry(janela,width=35,bg=COR_PREENCHER,font=("Inter",15))
    entrada_frequencia.pack(pady=5)

    #.......Prencher os campos despois de ter escolhido a planta
    def preencher_campos(*args):
        nome_escolhido=variavel_planta.get()

        planta=None
        for p in minhas_plantas:
            if p["nome"]==nome_escolhido: planta=p
            break
        if planta is None: 
            return
        
        #....... Apaga antigo nome e coloca o novo
        entrada_nome.delete(0,tk.END)
        entrada_nome.insert(0,planta["nome"])
        #....... o mesmo mas em tipos
        entrada_tipo.delete(0,tk.END)
        entrada_tipo.insert(0,planta["tipo"])
        #....... o mesmo mas em cuidados      
        entrada_cuidados.delete(0,tk.END)
        entrada_cuidados.insert(0,planta["cuidados"])
        #....... o mesmo mas em data
        entrada_data.delete(0,tk.END)
        entrada_data.insert(0,planta["ultima_rega"])
        #....... o mesmo mas em frequencia
        entrada_frequencia.delete(0,tk.END)
        entrada_frequencia.insert(0,planta["frequencia_rega"])

    #....... Sempre que o valor de variavel_planta mudar, executa a função preencher_campos
    variavel_planta.trace_add("write",preencher_campos)

    def atualizar():
        nome_escolhido=variavel_planta.get()

        #.......Possiveis erros:
        if nome_escolhido=="":
            messagebox.showerror("Erro","Seleciona uma planta.",parent=janela)
            return
        
        planta=None
        for p in minhas_plantas:
            if p["nome"]==nome_escolhido:
                planta=p
                break
        if planta is None: 
            messagebox.showerror("Erro","A planta não foi encontrada.",parent=janela)
            return
        
        #.......buscar o utilizador escreveu nas caixas de texto
        novo_nome=entrada_nome.get().strip()
        novo_tipo=entrada_tipo.get().strip()
        novos_cuidados=entrada_cuidados.get().strip()
        nova_data=entrada_data.get().strip()
        nova_frequencia=entrada_frequencia.get().strip()

        #....... erro no nome
        if novo_nome=="":
             messagebox.showerror("Erro","O nome da planta não pode estar vazio.",parent=janela)
             return   
        for outra_planta in minhas_plantas:
            if outra_planta!=planta and outra_planta["nome"].lower()==novo_nome.lower(): 
                messagebox.showerror("Erro","Já tens outra planta com esse nome.",parent=janela)
                return
            
        #....... erro no tipo
        if novo_tipo=="": 
            messagebox.showerror("Erro","O tipo não pode estar vazio.",parent=janela)
            return
        
        #.......erro na data
        try: data=datetime.strptime(nova_data,"%Y-%m-%d").date()
        except ValueError:
             messagebox.showerror("Erro","Data inválida. Utiliza AAAA-MM-DD.",parent=janela)
             return
        if data>date.today(): 
            messagebox.showerror("Erro","A data não pode ser futura.",parent=janela)
            return
        
        #.......erro na frenquencia
        try: frequencia=int(nova_frequencia)
        except ValueError: 
            messagebox.showerror("Erro","A frequência deve ser um número inteiro.",parent=janela)
            return
        if frequencia<=0: 
            messagebox.showerror("Erro","A frequência deve ser superior a 0.",parent=janela)
            return

        #....... altera os dados da planta no JSON
        planta["nome"]=novo_nome
        planta["tipo"]=novo_tipo
        planta["cuidados"]=novos_cuidados
        planta["ultima_rega"]=nova_data
        planta["frequencia_rega"]=frequencia

        if guardar_dados(dados): 
            messagebox.showinfo("Cuidado de Plantas","Planta atualizada com sucesso!",parent=janela)
            janela.destroy()


    #----- 4 Botones:
    frame_botoes = tk.Frame(janela, bg=COR_FUNDO)
    frame_botoes.pack(side="bottom")

    botao_fechar = criar_botao(janela, "Guardar alterações", atualizar, 15)
    botao_fechar.pack(pady=10)

    botao_fechar = criar_botao_saida(janela, "Cancelar",janela.destroy, 15)
    botao_fechar.pack(pady=10)

# =======================================================================================================================
# 10 - REMOVER PLANTA
# =======================================================================================================================

def janela_remover_planta(dados, utilizador):
    #----- 1 parte Janela
    janela = tk.Toplevel()
    janela.title("Remover planta")
    janela.geometry("450x350")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)

    #----- 2 parte titulo Principal:
    tk.Label(janela, text="REMOVER PLANTA", font=("Inter", 18, "bold"), bg=COR_FUNDO).pack(pady=25)

    #-----Se não tiver plantas
    minhas_plantas = obter_minhas_plantas(dados, utilizador)
    if not minhas_plantas:
        messagebox.showinfo("Aviso", "Não tens nenhuma planta registada.")
        return
    
    #-----Escolher planta
    tk.Label(janela, text="Seleciona a planta:", bg=COR_FUNDO).pack()

    #----- Lista apenas com os nomes
    lista_plantas = [f"{planta['id']} - {planta['nome']}" for planta in minhas_plantas]
    variavel_planta = tk.StringVar()
    menu = tk.OptionMenu(janela, variavel_planta, *lista_plantas)
    menu.config(width=30)
    menu.pack(pady=15)

    #----- Funcao de remover
    def remover():
        selecao = variavel_planta.get()
        if selecao == "":
            messagebox.showerror("Erro","Seleciona uma planta.", parent=janela)
            return
        try:
            planta_id = int(selecao.split(" - ")[0])
        except ValueError:
            messagebox.showerror("Erro","Planta inválida.", parent=janela)
            return
        
        planta = procurar_planta_por_id(dados, utilizador, planta_id)

        if planta is None:
            messagebox.showerror("Erro","A planta não foi encontrada.", parent=janela)
            return
        #----- confirmacao
        confirmacao = messagebox.askyesno("Confirmar remoção",f"Tens a certeza que queres remover a planta '{planta['nome']}'?",parent=janela)
        if not confirmacao:
            return
        
        #----- altera os dados da planta no JSON
        dados["plantas"].remove(planta)
        if guardar_dados(dados):
            messagebox.showinfo("Cuidado de Plantas", f"A planta '{planta['nome']}' foi removida com sucesso!", parent=janela)
            janela.destroy()

    #----- 4 Botones:
    frame_botoes = tk.Frame(janela, bg=COR_FUNDO)
    frame_botoes.pack(side="bottom")

    botao_fechar = criar_botao(janela, "Remover", remover, 15)
    botao_fechar.pack(pady=10)

    botao_fechar = criar_botao_saida(janela, "Cancelar",janela.destroy, 15)
    botao_fechar.pack(pady=10)

# =======================================================================================================================
# 11 - EDITAR PERFIL
# =======================================================================================================================

def janela_editar_perfil(dados, utilizador, label_bem_vindo=None):
    #----- 1 parte Janela
    janela = tk.Toplevel()
    janela.title("Editar perfil")
    janela.geometry("500x500")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)

    #----- 2 parte titulo Principal:
    tk.Label(janela, text="EDITAR O MEU PERFIL", font=("Inter", 18, "bold"), bg=COR_FUNDO).pack(pady=20)

    #.......NOME
    tk.Label(janela,text="Nome:",bg=COR_FUNDO,font=("Inter", 12, "bold"),width=35,anchor="w").pack()
    entrada_nome = tk.Entry(janela, width=35, bg=COR_ENTRADA)
    entrada_nome.insert(0, utilizador.get("nome", ""))
    entrada_nome.pack(pady=5)

    #.......USERNAME
    tk.Label(janela,text="Username:",bg=COR_FUNDO,font=("Inter", 12, "bold"),width=35,anchor="w").pack()
    entrada_username = tk.Entry(janela, width=35, bg=COR_ENTRADA)
    entrada_username.insert(0, utilizador.get("username", ""))
    entrada_username.pack(pady=5)

    #.......PASSWORD
    tk.Label(janela,text="Password:",bg=COR_FUNDO,font=("Inter", 12, "bold"),width=35,anchor="w").pack()
    entrada_password = tk.Entry(janela, width=35, show="*", bg=COR_ENTRADA)
    entrada_password.pack(pady=5)
    tk.Label(janela, text="Deixa a password vazia para manter a atual.", font=("Inter", 9, "italic"), bg=COR_FUNDO).pack(pady=5)

    #....... funcion para guardar perfil
    def guardar_perfil():
        novo_nome = entrada_nome.get().strip()
        novo_username = entrada_username.get().strip()
        nova_password = entrada_password.get()

        #....... NOME
        if novo_nome == "":
            messagebox.showerror("Erro","O nome não pode estar vazio.", parent=janela)
            return
        if not novo_nome.replace(" ", "").isalpha():
            messagebox.showerror("Erro","O nome não pode conter números ou caracteres especiais.", parent=janela)
            return

        #....... USERNAME
        if novo_username == "":
            messagebox.showerror("Erro","O username não pode estar vazio.", parent=janela)
            return
        for outro_utilizador in dados["utilizadores"]:
            if (outro_utilizador.get("id") != utilizador.get("id") and outro_utilizador.get("username", "").lower() == novo_username.lower()):
                messagebox.showerror("Erro","Esse username já está registado.", parent=janela)
                return

        #....... PASSWORD
        if nova_password != "":
            if len(nova_password) < 6:
                messagebox.showerror("Erro","A password deve ter pelo menos 6 caracteres.", parent=janela)
                return
            utilizador["password"] = nova_password

        #....... atualizar no JSON
        utilizador["nome"] = novo_nome
        utilizador["username"] = novo_username

        if guardar_dados(dados):
            if label_bem_vindo is not None:
                label_bem_vindo.config(text=f"Bem-vindo, {novo_nome}!")

            messagebox.showinfo("Cuidado de Plantas", "Perfil atualizado com sucesso!", parent=janela)
            janela.destroy()

    #----- 4 Botones
    frame_botoes = tk.Frame(janela, bg=COR_FUNDO)
    frame_botoes.pack(side="bottom", pady=15)

    # BOTÃO CRIAR
    botao_criar = criar_botao(frame_botoes,"Guardar alterações",guardar_perfil,25)
    botao_criar.pack(pady=10)

    # BOTÃO CANCELAR
    botao_cancelar = criar_botao_saida(frame_botoes,"Cancelar",janela.destroy,25)
    botao_cancelar.pack(pady=10)

# =======================================================================================================================
# 12 - REGA URGENTE
# =======================================================================================================================

def janela_rega_urgente(dados, utilizador):
    #----- 1 parte Janela
    janela = tk.Toplevel()
    janela.title("Rega urgente")
    janela.geometry("650x600")
    janela.resizable(False, False)
    janela.configure(bg=COR_FUNDO)

    #----- 2 parte titulo Principal:
    tk.Label(janela, text="REGA DAS PLANTAS", font=("Inter", 18, "bold"), bg=COR_FUNDO).pack(pady=15)

    #.......Obter as plantas do utilizador
    minhas_plantas = obter_minhas_plantas(dados, utilizador)

    #.......Se nao tem plantas
    if not minhas_plantas:
        tk.Label(janela, text="Não tens nenhuma planta registada.", font=("Inter", 13), bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=50)

        botao_fechar = criar_botao_saida(janela, "Fechar", janela.destroy, 15)
        botao_fechar.pack(pady=10)
        return

    #.......chama funcao auxiliar para a area com scroll
    frame_resultados = criar_area_scroll(janela)

    #....... calcula a rega
    for planta in minhas_plantas:

        frame = tk.Frame(frame_resultados,bg=COR_PREENCHER,padx=15, pady=10)
        frame.pack(fill="x", padx=5, pady=8)

        tk.Label(frame,text=planta.get("nome", "Sem nome"), font=("Inter", 13, "bold"),bg=COR_PREENCHER, fg=COR_TITULO, anchor="w").pack(fill="x", pady=(0, 10))

        frame_conteudo = tk.Frame(frame,bg=COR_PREENCHER)
        frame_conteudo.pack(fill="x")

        caminho_foto = planta.get("foto")

        if caminho_foto and os.path.exists(caminho_foto):

            try:
                imagem = tk.PhotoImage(file=caminho_foto)

                largura = imagem.width()
                altura = imagem.height()

                if largura > 180 or altura > 180:
                    fator = max(largura // 180, altura // 180)

                    if fator < 1:
                        fator = 1

                    imagem = imagem.subsample(fator, fator)

                label_imagem = tk.Label(frame_conteudo,image=imagem,bg=COR_PREENCHER)
                label_imagem.image = imagem
                label_imagem.pack(side="left", padx=(0, 20))

            except tk.TclError:

                tk.Label(frame_conteudo,text="Imagem inválida",bg=COR_PREENCHER,fg=COR_TITULO).pack(side="left", padx=(0, 20))

        else:
            tk.Label(frame_conteudo,text="Sem foto",width=15,height=7,bg=COR_PREENCHER,fg=COR_TITULO).pack(side="left", padx=(0, 20))

        try:
            ultima_rega = datetime.strptime(planta["ultima_rega"],"%Y-%m-%d").date()
            frequencia = int(planta["frequencia_rega"])
            proxima_rega = ultima_rega + timedelta(days=frequencia)
            diferenca = (date.today() - proxima_rega).days

            #.......Informação da planta
            info = tk.Text(
                frame_conteudo,
                bg=COR_PREENCHER,
                fg=COR_TEXTO,
                font=("Inter", 10),
                wrap="word",
                height=2,
                width=35,
                bd=0,
                highlightthickness=0
            )
            info.pack(side="left",fill="both",expand=True)
            #.......Estilo a negrito
            info.tag_configure("bold",font=("Inter", 10, "bold"))

            #.......Tipo
            info.insert("end","Tipo:","bold")
            info.insert("end",f" {planta.get('tipo', '')}\n")

            #.......Mensage do Estado da rega
            if diferenca > 0:
                mensagem = (f"A rega está atrasada há "f"{diferenca} dias!")
            elif diferenca == 0:
                mensagem = "Precisa de ser regada hoje!"
            else:
                mensagem = (f"Faltam {abs(diferenca)} dias " f"para a próxima rega.")

            info.insert("end","Estado:","bold")
            info.insert("end",f" {mensagem}")

            #.......Impedir edição
            info.config(state="disabled")

        except (ValueError, KeyError, TypeError):
            tk.Label(frame_conteudo,text="Erro nos dados desta planta.",bg=COR_PREENCHER,fg=COR_TITULO,font=("Inter", 10, "bold")
            ).pack(side="left",padx=(0, 20))       
            
    #----- 4 Botones:
    frame_botoes = tk.Frame(janela, bg=COR_FUNDO)
    frame_botoes.pack(side="bottom")

    botao_fechar = criar_botao_saida(janela, "Cancelar",janela.destroy, 15)
    botao_fechar.pack(pady=10)

# =======================================================================================================================
# PROGRAMA PRINCIPAL
# =======================================================================================================================

if __name__ == "__main__":
    dados = carregar_dados()
    menu_inicial(dados)
