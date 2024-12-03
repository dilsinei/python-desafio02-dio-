import textwrap


def exibir_menu():
    menu = """\n
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Conta
    [lc]\tListar Contas
    [nu]\tNovo Usuário
    [q]\tSair
    => """

    return input(textwrap.dedent(menu))


def realizar_deposito(saldo, valor_depositado, extrato, /):
    if valor_depositado > 0:
        saldo += valor_depositado
        extrato += f"Depósito:\tR${valor_depositado: .2f}\n"
        print("\nOperação concluida.")
    else:
        print("Valor inválido.")
    return saldo, extrato


def realizar_saque(*, saldo, valor_sacado, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor_sacado > saldo
    excedeu_limite = valor_sacado > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n Saldo insuficiente.")
    elif excedeu_limite:
        print("\n Valor de saque excedeu o limite diario.")
    elif excedeu_saques:
        print("\n Número máximo de saques excedido. ")
    elif valor_sacado > 0:
        saldo -= valor_sacado
        extrato += f"Saque:\t\tR$ {valor_sacado:.2f}\n"
        numero_saques += 1
        print("\nSaque realizado com sucesso!")
    else:
        print("\n O valor informado é inválido.")
    return saldo, extrato


def exibir_extrato(saldo, extrato):
    print("\n=========== EXTRATO ===========")
    if extrato == "":
        print("Não foram realizadas movimentações.")
    else:
        print(extrato)
        print(f"Saldo: R${saldo: .2f}\n")
    return extrato


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n CPF já cadastrado.")
        return
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("Usuário criado com sucesso!")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n Conta criada com sucesso! ")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuário": usuario}
    print("\n Usuario não encontrado.")


def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agência:\t{conta['agencia']}
            C/C\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = exibir_menu()

        if opcao == "d":
            valor_depositado = float(input("Digite o valor depositado: "))
            saldo, extrato = realizar_deposito(saldo, valor_depositado, extrato)

        elif opcao == "s":
            valor_sacado = float(input("Digite o valor para saque: "))

            saldo, extrato = realizar_saque(
                saldo=saldo,
                valor_sacado=valor_sacado,
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
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada")


main()
