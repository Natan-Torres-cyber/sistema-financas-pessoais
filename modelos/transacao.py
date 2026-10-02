import csv
from datetime import datetime
import os
from arvore.arvore_binaria import ArvoreBinaria

class Transacoes:
    def __init__(self, categorias, contas):
        self.arvore = ArvoreBinaria()
        self.arquivo = "dados/transacoes.dat"
        self.categorias = categorias
        self.contas = contas
        self._garantir_arquivo()
        self._reconstruir_arvore()

    def _garantir_arquivo(self):
            if not os.path.exists(self.arquivo) or os.path.getsize(self.arquivo) == 0:
                with open(self.arquivo, mode="w", newline="") as arquivo:
                    escritor = csv.writer(arquivo)
                    escritor.writerow(["cod_trans", "cod_cat", "cod_conta", "data", "valor", "debito_credito"])    

    def _reconstruir_arvore(self):
        with open(self.arquivo, mode="r") as arquivo:
            leitor = csv.reader(arquivo)
            linhas = list(leitor)
            for posicao, linha in enumerate(linhas[1:]):
                if linha [0] == '0':
                    continue
                self.arvore.inserir(int(linha[0]), posicao)

    def incluir(self, codigo_trans, cod_cat, cod_conta, data, valor, debito_credito):
        if self.arvore.buscar(codigo_trans) is not None:
            return False
        
        conta_encontrada = self.contas.buscar(cod_conta)
        if conta_encontrada is None:
            return False
        
        with open(self.arquivo, mode="r") as arquivo:
            leitor = csv.reader(arquivo)
            linhas = list(leitor)
        posicao = len(linhas) - 1

        with open(self.arquivo, mode="a", newline="") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow([codigo_trans, cod_cat, cod_conta, data, valor, debito_credito])
        self.arvore.inserir(codigo_trans, posicao)
        
        # conta_encontrada = [cod_conta, nome_banco, nome_pessoa, descricao, saldo]
        saldo_atual = float(conta_encontrada[4])
        if debito_credito == "Credito":
            novo_saldo = saldo_atual + float(valor)
        else:
            novo_saldo = saldo_atual - float(valor)
        self.contas.atualizar_saldo(cod_conta, novo_saldo)
        return True
    
    def buscar(self, codigo_trans):
        resultado = self.arvore.buscar(codigo_trans)
        if resultado is None:
            return None

        posicao = resultado.posicao

        with open(self.arquivo, mode="r") as arquivo:
            leitor = csv.reader(arquivo)
            linhas = list(leitor)

        linha = linhas[posicao + 1]
        cod_cat = int(linha[1])
        cod_conta = int(linha[2])

        categoria_encontrada = self.categorias.buscar(cod_cat)
        conta_encontrada = self.contas.buscar(cod_conta)
        if categoria_encontrada is not None:
            descricao_categoria = categoria_encontrada[1]
        else:
            descricao_categoria = "Categoria não encontrada"

        if conta_encontrada is not None:
            nome_banco = conta_encontrada[1]
        else:
            nome_banco = "Conta não encontrada"       
        return [linha[0], descricao_categoria, nome_banco, linha[3], linha[4], linha[5]]  
           
    def listar_por_periodo(self, data_inicial, data_final):
        inicio = datetime.strptime(data_inicial, "%d/%m/%Y")
        fim = datetime.strptime(data_final, "%d/%m/%Y")

        with open(self.arquivo, mode="r") as arquivo:
            leitor = csv.reader(arquivo)
            linhas = list(leitor)

        saldo_periodo = 0

        for linha in linhas[1:]:
            if linha[0] == '0': # pula linhas com transacoes de codigo 0 (excluido)
                continue
            data_transacao = datetime.strptime(linha[3], "%d/%m/%Y")

            if inicio <= data_transacao <= fim:
                # mostrar a transação e somar/subtrair do saldo_periodo
                print(f"Transação: {linha[0]}, Categoria: {linha[1]}, Conta: {linha[2]}, Data: {linha[3]}, Valor: {linha[4]}, Tipo: {linha[5]}")
                if linha[5].strip().lower() == "credito":
                    saldo_periodo += float(linha[4])
                else:
                    saldo_periodo -= float(linha[4])
        print(f"Saldo do período: R$ {saldo_periodo}")

    def excluir(self, codigo_trans):
        resultado = self.arvore.buscar(codigo_trans)
        if resultado is None:
            return False  # não existe, nada a excluir

        posicao = resultado.posicao

        with open(self.arquivo, mode="r") as arquivo:
            leitor = csv.reader(arquivo)
            linhas = list(leitor)

        linha = linhas[posicao + 1]

        # se já foi excluída antes, não faz nada (evita estornar duas vezes)
        if linha[0] == "0":
            return False

        # estorna o valor no saldo da conta: faz o contrário do lançamento
        cod_conta = int(linha[2])
        valor = float(linha[4])
        tipo = linha[5].strip().lower()

        conta = self.contas.buscar(cod_conta)
        if conta is not None:
            saldo_atual = float(conta[4])
            if tipo == "credito":
                novo_saldo = saldo_atual - valor   # crédito excluído: tira o valor
            else:
                novo_saldo = saldo_atual + valor   # débito excluído: devolve o valor
            self.contas.atualizar_saldo(cod_conta, novo_saldo)

        # exclusão lógica: marca o código da transação como "0"
        linha[0] = "0"

        with open(self.arquivo, mode="w", newline="") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerows(linhas)

        return True                        