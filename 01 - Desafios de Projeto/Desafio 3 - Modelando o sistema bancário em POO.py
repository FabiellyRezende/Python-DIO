import textwrap
from abc import ABC, abstractclassmethod, abstractproperty

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco #recebi essa variável acima, então sempre chamar ela assim
        self.contas = [] #fica vazio pois não recebi no construtor

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta) #chamando o registrar do transacao

    def adicionar_conta(self, conta):
        self.contas.append(conta) #adiciona a conta na lista

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco) #chamando o endereco da classe pai
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod #Recebe a classe como 1º argumento em vez do objeto
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property #criado para poder visualizar os dados privados
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = saldo < valor

        if excedeu_saldo:
            print("Saldo insuficiente!\n")       

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("Quantia inválida!")

        return False

    def depositar(self, valor):
        if valor > 0:
            print("\n=== Depósito realizado com sucesso! ===")
            self._saldo += valor
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("Valor superior ao limite do saque!\n")

        elif excedeu_saques:
            print("Limite diário de saques atingido!\n")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:{self.agencia}
            C/C:    {self.numero}
            Titular:{self.cliente.nome}\n"""

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)



def menu():
    print("\n")
    print("MENU CLIENTE".center(20,"="))
    print ("1- DEPÓSITO\n2- SAQUE\n3- EXTRATO\n4- SAIR\n")
    print("MENU ADM".center(21,"="))
    print ("5- NOVO CLIENTE\n6- NOVA CONTA\n7- LISTAR CONTAS\n8- SAIR")
    return int(input("\nSelecione uma opção: "))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print ("Cliente não possui Conta!")
        return

    #não permite cliente escolher a conta
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print ("Cliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print ("Cliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print ("Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("EXTRATO".center(30,"="))
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\tR$ {conta.saldo:.2f}")
    print("="*30)

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Cliente já existente!")
        return

    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    endereco = input("Endereço (logradouro, nº - bairro - Cidade/UF): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente cadastrado com sucesso! ===\n")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("=== Cliente não encontrado! ===\n")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("=== Conta criada com sucesso! ===\n")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def sistema_banco():
    clientes = []
    contas = []
    opcao = -1

    print("\nBem vindo ao Banco Banco\n")

    while True:
        opcao = menu()

        if opcao==1:
            depositar(clientes)

        elif opcao==2:
            sacar(clientes)

        elif opcao==3:
            exibir_extrato(clientes)
        
        elif opcao==4:
            print("\nSistema encerrado")
            break

        elif opcao==5:
            criar_cliente(clientes)
            
        elif opcao==6:
            numero_conta = len(contas)+1
            criar_conta(numero_conta, clientes, contas)

        elif opcao==7:
            listar_contas(contas)
        
        elif opcao==8:
            print("\nSistema encerrado")
            break

        else:
            print("\nOpção Inválida!\n")


sistema_banco()