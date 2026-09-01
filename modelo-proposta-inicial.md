# Proposta Inicial do Projeto Final

Este documento deve ser preenchido e entregue **antes de iniciar o
desenvolvimento**. O objetivo é confirmar que o problema está claro, que o MVP
pode ser concluído no tempo disponível e que a equipa organizou o trabalho.

## Requisitos da proposta

- Entregar **uma proposta por equipa**. Nos projetos individuais, entregar uma
  proposta por formando.
- Escrever respostas curtas e concretas. O conteúdo produzido pela equipa deve
  ocupar aproximadamente **uma página**, sem contar com estas instruções.
- Identificar claramente o que pertence ao **MVP obrigatório** e o que é apenas
  uma extensão opcional.
- Incluir um exemplo da estrutura dos dados em Python.
- Indicar a divisão inicial de tarefas quando o projeto for realizado em equipa.
- Submeter a proposta à aprovação do formador antes de desenvolver o programa.
- Atualizar a proposta quando o formador pedir uma redução ou clarificação do
  âmbito.

A proposta é um plano inicial. Pode ser ajustada durante o desenvolvimento,
desde que as alterações sejam justificadas e o MVP aprovado continue a ser
cumprido.

---

## 1. Identificação

**Título do projeto:**  

- Gestor de Cuidado de Plantas

**Elementos da equipa:**

- Nome: Anny Santos (8371435)


## 2. Problema e utilizador

**Que problema concreto pretendem resolver?**

> Ajudara as pessoas que têm prolemas em  se organizarem em relação aos cuidados das suas plantas. 
> Como também permitirá registar e consultar informação sobre o cuidado de cada planta de acordo com as necesidades que o dono lhes atribuiu.


**Quem utilizará a aplicação?**

> Pessoas que possuem plantas.


**Que resultado útil deverá obter esse utilizador?**

> Registar as suas plantas
> Consultar as informações de cada uma 
> Verificar quais precisam de ser regadas.

## 3. MVP

Indicar quatro ou cinco operações essenciais. Estas operações devem funcionar
antes de serem desenvolvidas extensões.

1.Adicionar uma nova planta.
2.Listar todas as plantas registadas.
3.Procurar uma planta pelo nome.
4.Atualizar as informações de uma planta, incluindo a data da última rega.
5.Remover uma planta.

**Resumo ou cálculo que a aplicação apresentará:**

- A aplicação apresentará o número total de plantas registadas e identificará quantas plantas precisam de ser regadas, com base na data da última rega e na frequência de rega definida.

## 4. Estrutura inicial dos dados

Apresentar um exemplo de um registo. Adaptar as chaves ao tema escolhido.

```python
registo = { 
    "nome": "Orquídea", 
    "tipo": "Flor",
    "ultima_rega": "2026-08-20", 
    "frequencia_rega": 7, 
    "estado": "ativo" }
```

**Como serão guardados vários registos?**

```python
dados = [registo]
```

**Nome previsto para o ficheiro JSON:**

> plantas.json

## 5. Organização inicial do código

Indicar as principais funções previstas. Os nomes podem ser alterados durante o
desenvolvimento.

```python
def menu(dados):
    pass

def adicionar_planta(dados):
    pass


def listar_plantas(dados):
    pass


def procurar_planta(dados):
    pass


def atualizar_planta(dados):
    pass


def remover_planta():
    pass
```

**Classes previstas, quando aplicável:**

> 


## 6. Tecnologias e extensões opcionais

**Bibliotecas, frameworks ou outras tecnologias que pretendem experimentar:**

> json: Guardar e carregar os dados
> datetime : para calcular há quantos dias cada planta foi regada.

(sem dependências externas)

**Extensões a realizar apenas depois de o MVP estar funcional:**

-Permitir ordenar as plantas por nome.
-Apresentar uma lista separada das plantas que precisam de ser regadas com urgência.

## 7. Divisão inicial de tarefas

Preencher apenas quando o projeto for realizado em equipa. Todos os elementos
devem participar no planeamento, implementação, testes e demonstração.

| Elemento | Responsabilidades iniciais |
|----------|----------------------------|
| | |
| | |
| | |

## Checklist para aprovação

Antes de entregar, confirmar:

- [✓] O problema e o utilizador estão identificados.
- [✓] O MVP contém quatro ou cinco operações concretas.
- [✓] O MVP pode ser concluído nas 10 horas disponíveis.
- [✓] Existe um exemplo da estrutura dos dados.
- [✓] Está prevista a utilização de funções.
- [✓] Está prevista a persistência em JSON.
- [✓] As extensões estão separadas do MVP.
- [✓] As tarefas estão distribuídas, quando o projeto é realizado em equipa.
- [✓] Não foram incluídos dados pessoais reais, palavras-passe ou chaves de API.

## Validação do formador

**Estado:** [ ] Aprovada  [ ] Aprovada com alterações  [ ] Reformular

**Alterações ou observações:**


**Data:**