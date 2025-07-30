import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import functools

# ===================================================================
# DECORATOR DE LOG (NOVO)
# ===================================================================

def log_transacao(func):
    """
    Decorator que registra informações sobre a execução de uma função em log.txt.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """
        Função interna (wrapper) que adiciona a funcionalidade de log.
        """
        # Requisito 1: Data e hora atuais
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Requisito 3: Argumentos da função
        # Tenta criar uma representação legível dos argumentos
        try:
            argumentos_str = f"Args: {args}, Kwargs: {kwargs}"
        except Exception:
            argumentos_str = "Args: (não foi possível representar os argumentos)"
        
        # Executa a função original e captura seu retorno
        try:
            resultado = func(*args, **kwargs)
            # Requisito 4: Valor retornado pela função
            resultado_str = f"Retorno: {resultado}"
        except Exception as e:
            resultado = f"Erro: {e}"
            resultado_str = f"Retorno: {resultado}"
            raise # Re-levanta a exceção para não alterar o comportamento do programa

        # Requisito 2: Nome da função
        nome_funcao = func.__name__

        # Monta a entrada de log completa
        log_entry = f"[{timestamp}] - Função '{nome_funcao}' | {argumentos_str} | {resultado_str}\n"

        # Requisito 5 e 6: Escreve no arquivo log.txt em modo de "append"
        with open("log.txt", "a", encoding="utf-8") as f:
            # Requisito 7: Cada entrada em uma nova linha
            f.write(log_entry)
            
        return resultado
    return wrapper


# ===================================================================
# BLOCO DE CLASSES (A ESTRUTURA ORIENTADA A OBJETOS)
# ===================================================================

class Cliente:
    """Classe base para um cliente do banco."""
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        """Registra uma transação para uma conta do cliente."""
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """Adiciona uma nova conta para o cliente."""
        self.contas.append(conta)


class PessoaFisica(Cliente):
    """Classe que representa um cliente do tipo Pessoa Física."""
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    """Classe base para uma conta bancária."""
    def __init__(self, numero, cliente):
        self._saldo = 150.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        """Método de fábrica para criar uma nova conta."""
        return cls(numero, cliente)

    @property
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
        """Realiza a lógica de saque da conta."""
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n❌ Operação falhou! Você não tem saldo suficiente.")
        elif valor > 0:
            self._saldo -= valor
            print("\n✅ Saque realizado com sucesso!")
            return True
        else:
            print("\n❌ Operação falhou! O valor informado é inválido.")
        
        return False

    def depositar(self, valor):
        """Realiza a lógica de depósito na conta."""
        if valor > 0:
            self._saldo += valor
            print("\n✅ Depósito realizado com sucesso!")
            return True
        else:
            print("\n❌ Operação falhou! O valor informado é inválido.")
            return False


class ContaCorrente(Conta):
    """Classe que representa uma Conta Corrente, com regras específicas."""
    def __init__(self, numero, cliente, limite=500.0, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        """Sobrescreve o método sacar para incluir regras da conta corrente."""
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print(f"\n❌ Operação falhou! O valor do saque excede o limite de R$ {self._limite:.2f}.")
        elif excedeu_saques:
            print("\n❌ Operação falhou! Número máximo de saques excedido.")
        else:
            return super().sacar(valor)

        return False

    def definir_novo_limite_saque(self, novo_limite):
        """Permite ao cliente alterar o limite máximo por saque."""
        if novo_limite > 0:
            self._limite = novo_limite
            print(f"\n✅ Limite de saque alterado para R$ {novo_limite:.2f} com sucesso!")
            return True
        else:
            print("\n❌ Operação falhou! O valor do limite deve ser positivo.")
            return False
    
    def __str__(self):
        """Retorna uma representação em string do objeto ContaCorrente."""
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    """Classe para gerenciar o histórico de transações de uma conta."""
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """Adiciona uma nova transação ao histórico."""
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    """Classe abstrata para representar uma Transação."""
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    """Classe para representar uma transação de Saque."""
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    """Classe para representar uma transação de Depósito."""
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

# ===================================================================
# BLOCO DE FUNÇÕES (AGORA ELAS ORQUESTRARAM OS OBJETOS)
# ===================================================================

def menu():
    """Exibe o menu de opções para o usuário."""
    menu_texto = """
    ================== MENU =====================
    Bem vindo ao Cash Bank🪙
    Por gentileza, escolha uma das opções abaixo:

    [d]\tDepositar💰
    [s]\tSacar🤑
    [e]\tExtrato📊
    [al]\tAlterar limite de saque 🛠️
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair❌
    => """
    return input(textwrap.dedent(menu_texto))


def filtrar_cliente(cpf, clientes):
    """Filtra um cliente da lista pelo seu CPF."""
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    """Recupera a primeira conta de um cliente."""
    if not cliente.contas:
        print("\n❌ Cliente não possui conta!")
        return None
    return cliente.contas[0]


@log_transacao
def depositar(clientes):
    """Função para orquestrar a operação de depósito."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n❌ Cliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: R$ "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, transacao)


@log_transacao
def sacar(clientes):
    """Função para orquestrar a operação de saque."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n❌ Cliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: R$ "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, transacao)


@log_transacao
def exibir_extrato(clientes):
    """Função para orquestrar a exibição do extrato."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n❌ Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================= EXTRATO📊 =================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            tipo_transacao = transacao['tipo'].ljust(8)
            extrato += f"{tipo_transacao}:\tR$ {transacao['valor']:.2f}\n"

    print(extrato)
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    """Função para criar um novo cliente (usuário)."""
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n❌ Já existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\n✅ Usuário criado com sucesso!")


def criar_conta(numero_conta, clientes, contas):
    """Função para criar uma nova conta."""
    cpf = input("Informe o CPF do usuário: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n❌ Usuário não encontrado, fluxo de criação de conta encerrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\n✅ Conta criada com sucesso!")


def listar_contas(contas):
    """Lista todas as contas cadastradas."""
    if not contas:
        print("\nNenhuma conta cadastrada.")
        return
        
    print("\n================= LISTA DE CONTAS =================")
    for conta in contas:
        print(textwrap.dedent(str(conta)))
        print("-" * 45)


@log_transacao
def alterar_limite_saque(clientes):
    """Função para orquestrar a alteração do limite de saque."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n❌ Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    if not isinstance(conta, ContaCorrente):
        print("\n❌ Operação não disponível para este tipo de conta.")
        return

    novo_limite = float(input("Informe o novo valor para o limite de saque: R$ "))
    conta.definir_novo_limite_saque(novo_limite)

# ===================================================================
# BLOCO PRINCIPAL (MAIN)
# ===================================================================

def main():
    """Função principal que executa o sistema bancário."""
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)
        
        elif opcao == "al":
            alterar_limite_saque(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("\n✅ Obrigado por ser cliente Cash Bank!😍")
            break

        else:
            print("\n❌ Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()