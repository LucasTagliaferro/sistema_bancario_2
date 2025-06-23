import textwrap

def menu():
    """Exibe o menu de opções para o usuário."""
    menu_texto = """
    ================== MENU =====================
    Bem vindo ao Cash Bank🪙
    Por gentileza, escolha uma das opções abaixo:

    [d]\tDepositar💰
    [s]\tSacar🤑
    [e]\tExtrato📊
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair❌
    => """
    return input(textwrap.dedent(menu_texto))

def depositar(saldo, valor, extrato, /):
    """
    Realiza a operação de depósito.
    Argumentos são recebidos apenas por posição.
    Retorna o saldo e o extrato atualizados.
    """
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n✅ Depósito realizado com sucesso!")
    else:
        print("\n❌ Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Realiza a operação de saque.
    Argumentos são recebidos apenas por nome (keyword-only).
    Retorna o saldo, extrato e número de saques atualizados.
    """
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n❌ Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print(f"\n❌ Operação falhou! O valor do saque excede o limite de R$ {limite:.2f}.")

    elif excedeu_saques:
        print("\n❌ Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n✅ Saque realizado com sucesso!")

    else:
        print("\n❌ Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    """
    Exibe o extrato da conta.
    Recebe 'saldo' por posição e 'extrato' por nome.
    """
    print("\n================= EXTRATO📊 =================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    """Cria um novo usuário (cliente) no sistema."""
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n❌ Já existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("\n✅ Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    """Filtra um usuário da lista pelo seu CPF."""
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios, contas):
    """Cria uma nova conta corrente no sistema."""
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        contas.append({"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario})
        print("\n✅ Conta criada com sucesso!")
        return numero_conta + 1
    
    print("\n❌ Usuário não encontrado, fluxo de criação de conta encerrado!")
    return numero_conta

def listar_contas(contas):
    """Lista todas as contas cadastradas."""
    if not contas:
        print("\nNenhuma conta cadastrada.")
        return

    print("\n================= LISTA DE CONTAS =================")
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print(textwrap.dedent(linha))
        print("-" * 45)

def main():
    """Função principal que executa o sistema bancário."""
    # Constantes
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    
    # Variáveis de estado
    saldo = 150.0
    limite = 500.0
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    numero_conta_atual = 1

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: R$ "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: R$ "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta_atual = criar_conta(AGENCIA, numero_conta_atual, usuarios, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("\n✅ Obrigado por ser cliente Cash Bank!😍")
            break

        else:
            print("\n❌ Operação inválida, por favor selecione novamente a operação desejada.")

# Ponto de entrada do programa
if __name__ == "__main__":
    main()