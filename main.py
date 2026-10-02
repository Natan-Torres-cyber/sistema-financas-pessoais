from modelos.pessoa import Pessoas
from modelos.banco import Bancos
from modelos.categoria import Categorias
from modelos.conta import ContasBancarias
from modelos.transacao import Transacoes

pessoas = Pessoas()
bancos = Bancos()
categorias = Categorias()
contas = ContasBancarias(bancos, pessoas)
transacoes = Transacoes(categorias, contas)

while True:
    print("\n==============================")
    print("   SISTEMA DE FINANÇAS PESSOAIS")
    print("==============================")
    print("1. Incluir Pessoa")
    print("2. Incluir Banco")
    print("3. Incluir Categoria")
    print("4. Incluir Conta Bancária")
    print("5. Lançar Transação")
    print("6. Consultar Conta")
    print("7. Listar Saldos de Todas as Contas")
    print("8. Transações por Período")
    print("9. Excluir Transação")
    print("0. Sair")

    opcao = input("\nDigite a opção desejada: ")

    if opcao == "0":
        print("Encerrando programa...")
        break

    elif opcao == "1":
        codigo = int(input("Código: "))
        nome = input("Nome: ")
        sucesso = pessoas.incluir(codigo, nome)
        if sucesso:
            print("Pessoa incluída com sucesso!")
        else:
            print("Erro ao incluir pessoa.")

    elif opcao == "2":
        cod_banco = int(input("Código do Banco: "))
        descricao = input("Descrição: ")
        sucesso = bancos.incluir(cod_banco, descricao)
        if sucesso:
            print("Banco incluído com sucesso!")
        else:
            print("Erro ao incluir banco.")

    elif opcao == "3":
        cod_cat = int(input("Código da Categoria: "))
        descricao = input("Descrição: ")
        sucesso = categorias.incluir(cod_cat, descricao)
        if sucesso:
            print("Categoria incluída com sucesso!")
        else:
            print("Erro ao incluir categoria.")

    elif opcao == "4":
        cod_conta = int(input("Código da Conta: "))
        cod_banco = int(input("Código do Banco: "))
        cod_pessoa = int(input("Código da Pessoa: "))
        descricao = input("Descrição: ")
        saldo = float(input("Saldo inicial: "))
        sucesso = contas.incluir(cod_conta, cod_banco, cod_pessoa, descricao, saldo)
        if sucesso:
            print("Conta incluída com sucesso!")
        else:
            print("Erro ao incluir conta.")

    elif opcao == "5":
        codigo_trans = int(input("Código da Transação: "))
        cod_cat = int(input("Código da Categoria: "))
        cod_conta = int(input("Código da Conta: "))
        data = input("Data (dd/mm/aaaa): ")
        valor = float(input("Valor: "))
        tipo = input("Tipo (C = Crédito / D = Débito): ").strip().upper()
        while tipo not in ("C", "D"):
            print("Tipo inválido. Digite C ou D.")
            tipo = input("Tipo (C = Crédito / D = Débito): ").strip().upper()
        debito_credito = "Credito" if tipo == "C" else "Debito"
        sucesso = transacoes.incluir(codigo_trans, cod_cat, cod_conta, data, valor, debito_credito)
        if sucesso:
            print("Transação lançada com sucesso!")
        else:
            print("Erro ao lançar transação.")

    elif opcao == "6":
        cod_conta = int(input("Código da Conta a consultar: "))
        resultado = contas.buscar(cod_conta)
        if resultado is not None:
            print(f"Conta: {resultado[0]} | Banco: {resultado[1]} | Pessoa: {resultado[2]} | Descrição: {resultado[3]} | Saldo: {resultado[4]}")
        else:
            print("Conta não encontrada.")

    elif opcao == "7":
        contas.listar_saldos()

    elif opcao == "8":
        data_inicial = input("Data inicial (dd/mm/aaaa): ")
        data_final = input("Data final (dd/mm/aaaa): ")
        transacoes.listar_por_periodo(data_inicial, data_final)

    elif opcao == "9":
        codigo_trans = int(input("Código da Transação a excluir: "))
        sucesso = transacoes.excluir(codigo_trans)
        if sucesso:
            print("Transação excluída com sucesso!")
        else:
            print("Transação não encontrada ou já excluída.")

    else:
        print("Opção inválida.")