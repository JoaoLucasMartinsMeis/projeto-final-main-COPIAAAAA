import json
import os

opcao = None
pasta_projeto = os.path.dirname(os.path.abspath(__file__))
arquivo = os.path.join(pasta_projeto, "dados.json")

categorias_receitas = [
    "Salário",
    "Freelance",
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
        "saldo_minimo": 1000,
        "movimentacoes": [],
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

  if tipo == 'receita':
    while True:
      try:
        investir = int(input(f'Você deseja destinar uma parte desse valor para os investimentos?\n1 para sim 2 para não: '))
        if investir in (1, 2):
          break
        print('\nDigite 1 ou 2.')
      except ValueError:
        print('\nDigite apenas números.')

    if investir == 1:
      while True:
        try:
          porcentagem = float(input('Qual a porcentagem desse valor que você deseja investir? '))
          if 0 <= porcentagem <= 100:
            break
          print('\nA porcentagem deve estar entre 0 e 100.')
        except ValueError:
          print('\nDigite apenas números.')

      valor_investido = (valor / 100) * porcentagem
      valor = valor - valor_investido

      dados = carregar_dados()
      dados['movimentacoes'].append({
          "tipo": "investimento",
          "categoria": "investimentos",
          "descricao": f'investido através da receita {descricao}',
          "valor": valor_investido
      })
      print(f'\nDe um total de R${valor + valor_investido:.2f}, R${valor:.2f} ficou disponível e R${valor_investido:.2f} foi investido.')

      salvar_dados(dados)

  return {
    "tipo": tipo,
    "categoria": categoria,
    "descricao": descricao,
    "valor": valor
  }


def alterar_saldo_minimo():
  dados = carregar_dados()

  print(f'\nSaldo mínimo atual: R$ {dados["saldo_minimo"]:.2f}')

  while True:
    try:
      novo_saldo_minimo = float(input('Digite o novo saldo mínimo: '))

      if novo_saldo_minimo >= 0:
        break
      print('\nO saldo mínimo deve ser maior ou igual a zero.')

    except ValueError:
      print('\nValor inválido. Por favor, digite um número.')

  dados['saldo_minimo'] = novo_saldo_minimo

  salvar_dados(dados)
  print("Saldo mínimo alterado com sucesso!\n")

def calcular_valor_investido():
  dados = carregar_dados()
  valor_investido = 0
  for movimentacao in dados['movimentacoes']:
    if movimentacao['tipo'] == 'investimento':
      valor_investido += movimentacao['valor']
  return valor_investido

def calcular_saldo():
  dados = carregar_dados()
  saldo_atual = 0
  for movimentacao in dados['movimentacoes']:
    if movimentacao['tipo'] == 'receita':
      saldo_atual += movimentacao['valor']
    elif movimentacao['tipo'] == 'despesa':
      saldo_atual -= movimentacao['valor']
  return saldo_atual

def consultar_saldo(tipo):
  saldo = calcular_saldo()
  print(f'\nSaldo Atual: R$ {saldo:.2f}\n')

  if tipo == 'completo':
    dados = carregar_dados()
    categorias = {}

    for movimentacao in dados['movimentacoes']:
      if movimentacao['tipo'] == 'despesa':
        categoria = movimentacao['categoria']

        if categoria not in categorias:
          categorias[categoria] = 0

        categorias[categoria] += movimentacao['valor']

    print('Gastos por categoria:')

    for categoria, valor in sorted(categorias.items()):
      print(f'- {categoria}: R$ {valor:.2f}')


def validar_cadastro(movimentacao):
  saldo_atual = calcular_saldo()
  dados = carregar_dados()
  saldo_minimo = dados['saldo_minimo']

  if movimentacao['tipo'] == 'receita':
    saldo_futuro = saldo_atual + movimentacao['valor']
  else:
    saldo_futuro = saldo_atual - movimentacao['valor']

  if saldo_futuro < 0:
    print(f"\nAtenção! Esta operação deixará seu saldo negativo (R${saldo_futuro:.2f}).")

  elif saldo_futuro < saldo_minimo:
    diferenca = saldo_minimo - saldo_futuro
    print(f"\nSeu saldo ficará R${diferenca:.2f} abaixo da sua meta de saldo mínimo.")

  else:
    diferenca = saldo_futuro - saldo_minimo
    print(f"\nParabéns! Seu saldo ficará R${diferenca:.2f} acima da sua meta de saldo mínimo.")

  if saldo_atual < 0 and saldo_futuro >= 0:
    print("Seu saldo voltou ao positivo!")

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
  print('6 - Alterar saldo mínimo')
  print('7 - Verificar total investido')
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

    consultar_saldo("simplificado")

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

    consultar_saldo("simplificado")

  elif opcao == 3:
    consultar_saldo("completo")

  elif opcao == 4:
    consultar_historico()

  elif opcao == 5:
    tipo = input('Você deseja buscar uma receita ou despesa? ').lower().replace(" ", "")
    if tipo not in ('receita', 'despesa'):
      print('Opção inválida.')
      continue
    mostrar_categorias(tipo)
    categoria_escolhida = escolher_categoria(tipo)
    categoria = converter_categoria(categoria_escolhida, tipo)
    consultar_transacao_por_categoria(categoria)

  elif opcao == 6:
    alterar_saldo_minimo()
  
  elif opcao == 7:
    valor_investido = calcular_valor_investido()
    print(f'O total investido é de R${valor_investido:.2f}')

  elif opcao == 0:
    print("Encerrando programa.")

  else:
    print('Opção inválida. Por favor, escolha uma opção válida.')
    continue
