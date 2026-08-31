# 🌱 Gestor de Cuidado de Plantas

Este projeto é uma aplicação gráfica desenvolvida em **Python** para gerir o cuidado de plantas.

A aplicação permite criar contas de utilizador e, depois de iniciar sessão, cada utilizador pode gerir as suas próprias plantas.

Os dados são guardados num ficheiro `plantas.json`, permitindo que as contas e plantas continuem disponíveis quando o programa é fechado e aberto novamente.

---

## ✨ Funcionalidades principais

A aplicação possui as seguintes funcionalidades:

### 👤 Gestão de contas

- Criar uma nova conta
- Entrar numa conta existente
- Editar o perfil
- Alterar nome, idade, username e password
- Validação dos dados introduzidos

### 🌿 Gestão de plantas

- Adicionar uma planta
- Listar as plantas do utilizador
- Atualizar uma planta
- Remover uma planta
- Consultar os cuidados específicos de cada planta

### 💧 Sistema de rega

A aplicação calcula automaticamente a próxima data de rega com base em:

- Data da última rega
- Frequência de rega em dias

Depois indica se:

- A rega está atrasada
- A planta precisa de ser regada hoje
- Ainda faltam alguns dias para a próxima rega

---

# 📁 Organização do projeto

O programa está organizado por várias secções dentro do ficheiro Python:

```text
1. Bibliotecas
2. Configurações
3. Funções auxiliares
4. Carregar dados
5. Guardar dados
6. Menu inicial
7. Criar conta
8. Entrar na conta
9. Menu do utilizador
10. Adicionar planta
11. Listar plantas
12. Atualizar planta
13. Remover planta
14. Editar perfil
15. Rega urgente
16. Programa principal