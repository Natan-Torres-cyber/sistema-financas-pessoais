import csv
import os
from arvore.arvore_binaria import ArvoreBinaria

class Categorias:

    def __init__(self):
        self.arvore = ArvoreBinaria()
        self.arquivo = "dados/categorias.dat"
        self._garantir_arquivo()
        self._reconstruir_arvore()

    def _garantir_arquivo(self):
        if not os.path.exists(self.arquivo) or os.path.getsize(self.arquivo) == 0:
            with open(self.arquivo, mode="w", newline="") as arquivo:
                escritor = csv.writer(arquivo)
                escritor.writerow(["cod_cat", "descricao"])  

    def _reconstruir_arvore(self):
        with open(self.arquivo, mode="r") as arquivo:
            leitor = csv.reader(arquivo)
            linhas = list(leitor)
            for posicao, linha in enumerate(linhas[1:]):
                self.arvore.inserir(int(linha[0]), posicao)

    def incluir(self, cod_cat, descricao):
        if self.buscar(cod_cat) is not None:
            print("Erro: já existe uma categoria com esse código.")
            return False
        with open(self.arquivo, mode="r") as arquivo:
            leitor = csv.reader(arquivo)
            linhas = list(leitor)
        posicao = len(linhas) - 1  

        with open(self.arquivo, mode="a", newline="") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow([cod_cat, descricao])   
        self.arvore.inserir(cod_cat, posicao)    
        return True
    
    def buscar(self, cod_cat):
        resultado = self.arvore.buscar(cod_cat)
        if resultado is None:
            return None
        
        posicao = resultado.posicao

        with open(self.arquivo, mode="r") as arquivo:
            leitor = csv.reader(arquivo)
            linhas = list(leitor)

            linha = linhas[posicao + 1]  
            return linha