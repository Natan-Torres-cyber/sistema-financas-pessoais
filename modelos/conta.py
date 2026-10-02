import csv
import os
from arvore.arvore_binaria import ArvoreBinaria

class ContasBancarias:
    def __init__(self, bancos, pessoas):
        self.arvore = ArvoreBinaria()
        self.arquivo = "dados/contas.dat"
        self.bancos = bancos      
        self.pessoas = pessoas    
        self._garantir_arquivo()
        self._reconstruir_arvore()

    def _garantir_arquivo(self):
        if not os.path.exists(self.arquivo) or os.path.getsize(self.arquivo) == 0:
            with open(self.arquivo, mode="w", newline="") as arquivo:
                escritor = csv.writer(arquivo)
                escritor.writerow(["cod_conta", "cod_banco", "cod_pessoa", "descricao", "saldo"])

    def _reconstruir_arvore(self):
        with open(self.arquivo, mode="r") as arquivo:
            leitor = csv.reader(arquivo)
            linhas = list(leitor)
            for posicao, linha in enumerate(linhas[1:]):
                self.arvore.inserir(int(linha[0]), posicao) 

    def incluir(self, cod_conta, cod_banco, cod_pessoa, descricao, saldo):
        if self.buscar(cod_conta) is not None:
            print("Erro: já existe uma conta com esse código.")
            return False
        with open(self.arquivo, mode="r") as arquivo:
            leitor = csv.reader(arquivo)
            linhas = list(leitor)
        posicao = len(linhas) - 1
        with open(self.arquivo, mode="a", newline="") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow([cod_conta, cod_banco, cod_pessoa, descricao, saldo])
        self.arvore.inserir(cod_conta, posicao) 
        return True  
    
    def buscar(self, cod_conta):
        resultado = self.arvore.buscar(cod_conta)
        if resultado is None:
            return None
        posicao = resultado.posicao
        
        with open(self.arquivo, mode="r") as arquivo:
            leitor = csv.reader(arquivo)
            linhas = list(leitor)

        linha = linhas[posicao + 1]
        cod_banco = int(linha[1])
        cod_pessoa = int(linha[2])

        banco_encontrado = self.bancos.buscar(cod_banco)
        pessoa_encontrada = self.pessoas.buscar(cod_pessoa)

        if banco_encontrado is not None:
            nome_banco = banco_encontrado[1]
        else:
            nome_banco = "Banco não encontrado" 

        if pessoa_encontrada is not None:
            nome_pessoa = pessoa_encontrada[1]
        else:
            nome_pessoa = "Pessoa não encontrada" 
        return [linha[0], nome_banco, nome_pessoa, linha[3], linha[4]] 

    def atualizar_saldo(self, cod_conta, novo_saldo):
        resultado = self.arvore.buscar(cod_conta)
        if resultado is None:
            return False  # conta não existe, não há o que atualizar

        posicao = resultado.posicao

        with open(self.arquivo, mode="r") as arquivo:
            leitor = csv.reader(arquivo)

            linhas = list(leitor)
            linhas[posicao + 1][4] = str(novo_saldo)
        with open(self.arquivo, mode="w", newline="") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerows(linhas)  
        return True  # atualização bem-sucedida  

    def listar_saldos(self):
        with open(self.arquivo, mode="r") as arquivo:
            leitor = csv.reader(arquivo)
            linhas = list(leitor)

        saldo_geral = 0

        for linha in linhas[1:]:  # pula o cabeçalho
            cod_conta = int(linha[0])
            saldo = float(linha[4])
            print(f"Conta {cod_conta}: saldo R$ {saldo}")
            saldo_geral += saldo

        print(f"Saldo geral: R$ {saldo_geral}")                                      