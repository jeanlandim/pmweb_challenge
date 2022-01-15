
# O QUE DEVE SER FEITO

Você deverá implementar o fluxo de tratamento de dados descrito abaixo,
utilizando o dataset a seguir como base:
https://oto-public.s3.amazonaws.com/natal2021.zip

## Sua tarefa:
Com o objetivo de realizar uma campanha especial de final de ano,
recebemos o arquivo natal2021.csv do cliente. Você recebeu o desafio de
realizar a limpeza deste arquivo CSV para que possamos posteriormente
importá-lo em nosso banco de dados. Pensando em um cenário no qual o
arquivo CSV seja muito maior e não entre na memória de uma só vez, temos
os seguintes problemas para serem resolvidos:

1. Identificar o encoding do arquivo;
2. Processar o arquivo de 1000 em 1000 linhas;
3. Remover os espaços das colunas. Ex. ' Porto Alegre ' -> 'Porto Alegre';
4. Criar uma coluna CITY_ASCII no arquivo, a qual deve ser construída com
base na coluna CITY. Esta coluna não pode conter acentos, minúsculas e
caracteres especiais. Apenas letras, números e hífen são permitidos. Ex. 'São
Paulo - abç' -> 'SAO PAULO - ABC'
5. Remover os caracteres não numéricos da coluna PHONE;
6. Salvar o arquivo .csv com a nova coluna em UTF-8;

## Como executar o código

### Requerimentos:
- Python +3.9
- Poetry

O código deve ser executado dentro de um ambiente virtual do poetry, para instalar o [poetry](https://python-poetry.org/), utilize o pip:

		pip3 install poetry
		
Depois é só entrar nesse repositório e executar:

		poetry install && poetry install
		
Uma vez instalada as dependências do projeto, executar o arquivo *challenge.py*:

		./challenge.py

Há o arquivo de _tests.py_ disponível e caso queira execute-o para testar os principais componentes do código.

O projeto foi desenvolvido utilizando Linux. Em máquinas Windows, verifique como instalar o `pip`e/ou `poetry`.
Sob quaisquer dúvidas, favor entrar em contato.

## Arquivo finalizado

O arquivo em [natal2021_finalizada.csv](https://github.com/jeanlandim/pmweb_challenge/blob/main/data/natal2021_finalizada.csv) já foi tratado pelo o script,
e pode ser útil para atestar a usabilidade do script, sem precisar executá-lo.



