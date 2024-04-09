#Desafio 2
import textwrap

def menu():
    print("\n")
    print("MENU CLIENTE".center(20,"="))
    print ("1- DEPÓSITO\n2- SAQUE\n3- EXTRATO\n4- SAIR\n")
    print("MENU ADM".center(21,"="))
    print ("5- NOVO USUÁRIO\n6- NOVA CONTA\n7- LISTAR CONTAS\n8- SAIR")
    return int(input("\nSelecione uma opção: "))

def deposito(saldo, valor, extrato, /):
    if valor<0:
        print("Quantia Inválida!\n")
    else:
        print("Depósito realizado!\n")
        saldo += valor
        extrato+= f"Depósito: R$ {valor: .2f}\n"

    return saldo, extrato

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques, ):
    excedeu_saldo = saldo<valor
    excedeu_limite = valor>limite
    excedeu_saques = numero_saques>=limite_saques

    if excedeu_saldo:
        print("Saldo insuficiente!\n")
    elif excedeu_limite:
        print("Valor superior ao limite do saque!\n")
    elif excedeu_saques:
        print("Limite diário de saques atingido!\n")
    elif valor>0:
        numero_saques += 1
        saldo -= valor
        extrato+= f"Saque: R$ {valor: .2f}\n"
        print("Saque realizado!\n")
    else:
        print("Quantia inválida!")

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\n")
    print("EXTRATO".center(21,"="))
    print(extrato)
    print(f"Saldo: R${saldo: .2f}")
    print("=====================\n")    

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario ["cpf"]==cpf]
    return usuarios_filtrados [0] if usuarios_filtrados else None

def novo_usuario(usuarios):
    cpf = input("CPF (somente números): ")

    usuario = filtrar_usuario(cpf,usuarios)
    if usuario: 
        print("Usuário já existente!")
        return

    else:
        nome = input("Nome Completo: ")
        data_nascimento =  input("Data de Nascimento (DD/MM/AAAA): ") 
        endereco = input("Endereço (logradouro, nº - bairro - Cidade/UF): ")  
        usuarios.append({"cpf": cpf, "nome": nome, "data_nascimento": data_nascimento, "endereco": endereco})

        print("\n=== Usuário criado com sucesso! ===\n")

def nova_conta(agencia, conta, usuarios):
    cpf = input("CPF (somente números): ")
    usuario = filtrar_usuario(cpf,usuarios)

    if usuario:
        print("=== Conta criada com sucesso! ===\n")
        return {"agencia": agencia, "conta": conta, "usuario": usuario}
    else:
        print("=== Usuário não encontrado! ===\n")

def listar_contas(contas):
    for conta in contas:
        CC = f"""\
            Agência: {conta['agencia']}
            Conta:   {conta['conta']}
            Titular: {conta['usuario']['nome']}\n"""
        print("="*50)
        print(textwrap.dedent(CC))
        print("="*50)

def sistema_banco():
    saldo = 1000
    limite = 500
    opcao = -1
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    usuarios = []
    contas = []

    print("\nBem vindo ao Banco Banco\n")

    while True:
        opcao = menu()

        if opcao==1:
            valor = float(input("\nInforme o valor do depósito: "))
            saldo, extrato = deposito(saldo, valor, extrato)

        elif opcao==2:
            valor = float(input("\nInforme o valor do saque: "))
            saldo, extrato = saque(saldo=saldo, valor=valor, extrato=extrato, 
                            limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES,)
            
        elif opcao==3:
            exibir_extrato(saldo, extrato=extrato)
        
        elif opcao==4:
            print("\nSistema encerrado")
            break

        elif opcao==5:
            novo_usuario(usuarios)
            
        elif opcao==6:
            numero_conta = len(contas)+1
            conta = nova_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao==7:
            listar_contas(contas)
        
        elif opcao==8:
            print("\nSistema encerrado")
            break

        else:
            print("\nOpção Inválida!\n")

sistema_banco()