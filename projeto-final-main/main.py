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
        "limite_credito": 1000,
        "movimentacoes": []
    })


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
    try:
      categoria = int(input(f'\nClassifique sua categoria com uma das acima: '))

      if tipo == 'receita' and 1 <= categoria <= len(categorias_receitas):
        return categoria
      elif tipo == 'despesa' and 1 <= categoria <= len(categorias_despesas):
        return categoria
    
      print('Categoria inválida')

    except ValueError:
      print("Digite apenas números")


def cadastrar(tipo):
  mostrar_categorias(tipo)
  categoria_escolhida = escolher_categoria(tipo)

  descricao = input(f'Digite a descrição da {tipo}: ').lower()
  
  while True:
    try:
      valor = float(input(f'Digite o valor da {tipo}: '))

      if valor > 0:
        break

      print('\nO valor não pode ser menor ou igual a zero')

    except ValueError:
      print('\nValor inválido. Por favor, digite um número.')

  categoria = converter_categoria(categoria_escolhida, tipo)
  
  return {
    "tipo": tipo,
    "categoria": categoria,
    "descricao": descricao,
    "valor": valor
  }


def alterar_limite():
  dados = carregar_dados()
  print(f'\nLimite atual: R$ {dados["limite_credito"]:.2f}')

  while True:
    try:
      novo_limite = float(input('Digite o novo limite de crédito: '))

      if novo_limite > 0:
        break
      print('\nO limite de crédito deve ser maior que zero.')

    except ValueError:
      print('\nValor inválido. Por favor, digite um número.')

  dados['limite_credito'] = novo_limite

  salvar_dados(dados)
  print("Limite alterado com sucesso!")


def calcular_saldo():
  dados = carregar_dados()
  saldo_atual = 0
  for movimentacao in dados['movimentacoes']:
    if movimentacao['tipo'] == 'receita':
      saldo_atual += movimentacao['valor']
    elif movimentacao['tipo'] == 'despesa':
      saldo_atual -= movimentacao['valor']
  return saldo_atual


def consultar_saldo():
  saldo = calcular_saldo()
  print(f'\nSaldo Atual: R$ {saldo:.2f}\n')


def validar_cadastro(movimentacao):
  saldo_atual = calcular_saldo()
  dados = carregar_dados()
  limite_credito = dados['limite_credito']

  if movimentacao['tipo'] == 'receita':
    saldo_futuro = saldo_atual + movimentacao['valor']

  else:
    saldo_futuro = saldo_atual - movimentacao['valor']

  if saldo_futuro < -limite_credito:
    print("\nEssa operação ultrapassa seu limite de crédito! Cadastro cancelado!")
    return False

  elif saldo_futuro < 0:
    print("\nAtenção! Esta operação deixará seu saldo negativo.")
    return True

  elif saldo_atual < 0 and saldo_futuro >= 0:
    print("\nParabéns! Seu saldo voltou ao positivo.")
    return True
  
  else:
    return True
      

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
    print('\nNão foi encontrada nenhuma transação com esta categoria')
  print('\n')


while opcao != 0:
  print('===== ASSISTENTE FINANCEIRO =====\n')
  print('1 - Cadastrar receita')
  print('2 - Cadastrar despesa')
  print('3 - Consultar resumo do saldo')
  print('4 - Ver histórico de transações')
  print('5 - Consulta de transação por categoria')
  print('6 - Alterar limite de crédito')
  print('0 - Sair\n')

  try:
    opcao = int(input('Escolha uma opção: '))

  except ValueError:
    print('Opção inválida. Por favor, digite um número.')
    continue

  if opcao == 1:
    movimentacao = cadastrar('receita')
    transacao_permitida = validar_cadastro(movimentacao)

    if transacao_permitida:
      dados = carregar_dados()
      dados['movimentacoes'].append(movimentacao)
      salvar_dados(dados)
      print('\nReceita cadastrada com sucesso')

    else:
      print('Receita não cadastrada')

    consultar_saldo()

  elif opcao == 2:
    movimentacao = cadastrar('despesa')
    transacao_permitida = validar_cadastro(movimentacao)

    if transacao_permitida:
      dados = carregar_dados()
      dados['movimentacoes'].append(movimentacao)
      salvar_dados(dados)
      print('\nDespesa cadastrada com sucesso')

    else:
      print('Despesa não cadastrada')

    consultar_saldo()

  elif opcao == 3:
    consultar_saldo()

  elif opcao == 4:
    consultar_historico()

  elif opcao == 5:
    tipo = input('Você deseja buscar uma receita ou despesa? ').lower().replace(" ", "")
    mostrar_categorias(tipo)
    categoria_escolhida = escolher_categoria(tipo)
    categoria = converter_categoria(categoria_escolhida, tipo)
    consultar_transacao_por_categoria(categoria)

  elif opcao == 6:
    alterar_limite()

  else:
    print('Opção inválida. Por favor, escolha uma opção válida.')
    continue