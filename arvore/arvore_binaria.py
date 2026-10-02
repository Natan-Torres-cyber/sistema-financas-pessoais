class No:
    def __init__(self, chave, posicao):
        self.chave = chave
        self.posicao = posicao
        self.esquerda = None
        self.direita = None

class ArvoreBinaria: 
    def __init__(self):
        self.raiz = None

    def inserir(self, chave, posicao):
        novo_no = No(chave, posicao)
        if self.raiz is None:
            self.raiz = novo_no
            return
        atual = self.raiz
        pai = None
        while atual is not None:
            pai = atual
            if chave < atual.chave:
                atual = atual.esquerda
            else:
                atual = atual.direita
        if chave < pai.chave:
            pai.esquerda = novo_no
        else:
            pai.direita = novo_no  
             
    def buscar(self, chave):
        atual = self.raiz
        while atual is not None:
            if chave == atual.chave:
                return atual
            elif chave < atual.chave:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return None

