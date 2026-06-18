import json
import os

opcao = None
pasta_projeto = os.path.dirname(os.path.abspath(__file__))
arquivo = os.path.join(pasta_projeto, "dados.json")

categorias_receitas = [
    "Salário",
    "Freelance",
    "Investimentos",
    "Vendas",
    "Presentes",
    "Outros"
]

categorias_despesas = [
    "Alimentação",
    "Transporte",
    "Moradia",
    "Saúde",
    "Educação",
    "Lazer",
    "Vestuário",
    "Contas",
    "Impostos",
    "Outros"
]

def salvar_dados(dados):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_dados():
   with open(arquivo, "r", encoding="utf-8") as f:
    return json.load(f)

if not os.path.exists(arquivo):
    salvar_dados({
        "movimentacoes": []
    })

dados = carregar_dados()


def mostrar_categorias(tipo):
  i = 0
  if tipo == 'receita':
    for categoria in categorias_receitas:
      i += 1
      print(f'{i}. {categoria}')
  elif tipo == 'despesa':
    for categoria in categorias_despesas:
      i += 1
      print(f'{i}. {categoria}')


def converter_categoria(categoria, tipo):
  if tipo == 'receita':
    return categorias_receitas[categoria - 1].lower()
      
  if tipo == 'despesa':
    return categorias_despesas[categoria - 1].lower()
    

def escolher_categoria(tipo):
  while True:
    categoria = int(input(f'\nClassifique sua categoria com uma das acima: '))

    if tipo == 'receita' and 1 <= categoria <= len(categorias_receitas):
      return categoria
    elif tipo == 'despesa' and 1 <= categoria <= len(categorias_despesas):
      return categoria
    
    print('Categoria inválida')


def cadastrar(tipo):
  mostrar_categorias(tipo)
  categoria_escolhida = escolher_categoria(tipo)
  descricao = input(f'Digite a descrição da {tipo}: ').lower()
  valor = float(input(f'Digite o valor da {tipo}: '))

  while valor <= 0:
    print('O valor não pode ser menor ou igual a zero')
    valor = float(input(f'Digite o valor da {tipo}: '))

  categoria = converter_categoria(categoria_escolhida, tipo)

  return {
    "tipo": tipo,
    "categoria": categoria,
    "descricao": descricao,
    "valor": valor
  }


def calcular_saldo():
  dados = carregar_dados()
  saldo_atual = 0
  for movimentacao in dados['movimentacoes']:
    if movimentacao['tipo'] == 'receita':
      saldo_atual += movimentacao['valor']
    elif movimentacao['tipo'] == 'despesa':
      saldo_atual -= movimentacao['valor']
  return saldo_atual

def validar_cadastro(movimentacao):
  saldo_atual = calcular_saldo()

  if saldo_atual <= -1000:
    print("Essa operação ultrapassa seu limite de crédito! Cadastro cancelado!")
    return False

  elif saldo_atual <= -1:
    print("Atenção! Esta operação deixará seu saldo negativo.")

  elif saldo_atual > pre_cadastro and pre_cadastro <= -1:
    print("Parabéns! Seu saldo voltou ao positivo.")


def consultar_saldo():
  dados = carregar_dados()
  saldo = 0
  for movimentacao in dados['movimentacoes']:
    if movimentacao['tipo'] == 'receita':
      saldo += movimentacao['valor']
    elif movimentacao['tipo'] == 'despesa':
      saldo -= movimentacao['valor']
  print(f'Saldo Atual: R$ {saldo:.2f}')
      

def consultar_historico():
  dados = carregar_dados()
  contador = 0
  for movimentacao in dados['movimentacoes']:
    contador += 1
    print(f'\nMovimentação {contador}:')
    for keys, value in movimentacao.items():
      print(f'{keys}: {value}')


def consultar_transacao_por_categoria(categoria):
  dados = carregar_dados()
  contador = 0
  for movimentacao in dados['movimentacoes']:
    if movimentacao['categoria'] == categoria:
      contador += 1
      print(f'\nMovimentação {contador}:')
      for keys, value in movimentacao.items():
        print(f'{keys}: {value}')
  if contador == 0:
    print('Não foi encontrada nenhuma transação com esta categoria')
  print('\n')


def categorias():
  dados = carregar_dados()
  for movimentacao in dados['movimentacoes']:
    print(movimentacao)


while opcao != 0:
  print('===== ASSISTENTE FINANCEIRO =====\n')
  print('1 - Cadastrar receita')
  print('2 - Cadastrar despesa')
  print('3 - Consultar resumo do saldo')
  print('4 - Ver histórico de transações')
  print('5 - Consulta de transação por categoria')
  print('0 - Sair\n')
  opcao = int(input('Escolha uma opção: '))

  if opcao == 1:
    pre_cadastro = calcular_saldo()
    movimentacao = cadastrar('receita')
    validar_cadastro()
    dados['movimentacoes'].append(movimentacao)
    salvar_dados(dados)

    print('Receita cadastrada com sucesso')
    consultar_saldo()

  if opcao == 2:
    pre_cadastro = calcular_saldo()
    movimentacao = cadastrar('despesa')
    validar_cadastro()
    dados['movimentacoes'].append(movimentacao)
    salvar_dados(dados)

    print('Despesa cadastrada com sucesso')
    consultar_saldo()

  if opcao == 3:
    consultar_saldo()

  if opcao == 4:
    consultar_historico()

  if opcao == 5:
    tipo = input('Você deseja buscar uma receita ou despesa? ').lower().replace(" ", "")
    mostrar_categorias(tipo)
    categoria_escolhida = escolher_categoria(tipo)
    categoria = converter_categoria(categoria_escolhida, tipo)
    consultar_transacao_por_categoria(categoria)