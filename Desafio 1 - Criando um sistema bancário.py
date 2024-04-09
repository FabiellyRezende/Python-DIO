#operações depósito, saque e extrato
def menu():
    print("MENU".center(12," "))
    print ("1- DEPÓSITO\n2- SAQUE\n3- EXTRATO\n4- SAIR\n")


saldo = 1000
limite = 500
opcao = -1
extrato = ""
numero_saques = 0
limite_saques = 3

print("\nBem vindo ao Banco Banco\n")

while True:
    menu()
    opcao = int(input("\nSelecione uma opção: "))

    if opcao==1:
        valor = float(input("\nInforme o valor do depósito: "))
        if valor<0:
            print("Quantia Inválida!\n")
        else:
            print("Depósito realizado!\n")
            saldo += valor
            extrato+= f"Depósito: R$ {valor: .2f}\n"

    elif opcao==2:
        valor = float(input("\nInforme o valor do saque: "))
        if saldo<valor:
            print("Saldo insuficiente!\n")
        elif valor>limite:
            print("Valor superior ao limite do saque!\n")
        elif numero_saques>=limite_saques:
            print("Limite diário de saques atingido!\n")
        elif valor>0:
            numero_saques += 1
            print("Saque realizado!\n")
            saldo -= valor
            extrato+= f"Saque: R$ {valor: .2f}\n"
        else:
            print("Quantia inválida!")

    elif opcao==3:
        print("\n")
        print("EXTRATO".center(21,"="))
        print(extrato)
        print(f"Saldo: R${saldo: .2f}")
        print("=====================\n")
    
    elif opcao==4:
        print("\nSistema encerrado")
        break

    else:
        print("\nOpção Inválida!\n")
