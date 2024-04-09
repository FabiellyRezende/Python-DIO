# TODO: Crie uma Função: recomendar_plano para receber o consumo médio mensal:
def recomendar_plano(consumo):

# TODO: Crie uma Estrutura Condicional para verifica o consumo médio mensal 
# TODO: Retorne o plano de internet adequado:

    if consumo<=10:
        return("Seu plano ideal é: Plano Essencial Fibra - 50Mbps")
    elif consumo<=20:
        return("Seu plano ideal é: Plano Prata Fibra - 100Mbps")
    else:
        return("Seu plano ideal é Plano Premium Fibra - 300Mbps")
    return

# Solicita ao usuário que insira o consumo médio mensal de dados:
print("Informe seu consumo médio mensal (em GB): ")
consumo = float(input())
    
# Chama a função recomendar_plano com o consumo inserido e imprime o plano recomendado:

recomendar_plano(consumo)