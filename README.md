# Sistema de Finanças Pessoais

Sistema de terminal em Python para controlar contas bancárias e transações (crédito e débito), com os dados gravados em arquivos e um índice em **árvore binária de busca** implementada do zero.

Projeto individual, desenvolvido na disciplina de Algoritmos e Estruturas de Dados II do curso de Análise e Desenvolvimento de Sistemas (FEMA).

## Funcionalidades

- Cadastro de pessoas, bancos, categorias e contas bancárias
- Lançamento de transações de crédito ou débito, com atualização automática do saldo da conta
- Consulta de conta (com nome do banco e do titular)
- Listagem de saldos de todas as contas e saldo geral
- Extrato de transações por período, com o saldo do período
- Exclusão lógica de transações, com estorno do valor no saldo

## Tecnologias e conceitos

- Python 3 (somente biblioteca padrão: `csv`, `os`, `datetime`)
- Programação Orientada a Objetos: uma classe por entidade
- Persistência em arquivos CSV (`dados/*.dat`)
- Árvore binária de busca como índice

## Como funciona o índice

Cada cadastro (pessoas, bancos, contas etc.) tem uma árvore binária de busca em memória. Cada nó guarda o **código** do registro e a **posição** da linha dele no arquivo.

- Quando o programa abre, as árvores são montadas a partir dos arquivos.
- Para buscar um registro pelo código, o programa percorre a árvore, e não a lista inteira, até achar a posição da linha.
- Excluir uma transação é uma **exclusão lógica**: o código dela vira `0` no arquivo. Ela deixa de aparecer nos relatórios e o valor volta para o saldo da conta.

**Limitações conhecidas:** a árvore não é balanceada. Com códigos em sequência (1, 2, 3...), ela vira uma lista e a busca fica O(n). Além disso, depois de achar a posição, o programa ainda lê o arquivo inteiro para pegar a linha.

## Como executar

```bash
cd sistema-financas-pessoais
python main.py
```

Execute o comando a partir da pasta do projeto, porque os arquivos de dados ficam em `dados/`.

## Estrutura

```
main.py                 # menu principal
arvore/arvore_binaria.py
modelos/                # Pessoas, Bancos, Categorias, ContasBancarias, Transacoes
dados/                  # arquivos CSV (.dat)
```

## Autor

Natan Torres · [LinkedIn](https://www.linkedin.com/in/natan-torres-248367364)
