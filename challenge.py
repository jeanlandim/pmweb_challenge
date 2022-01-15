#!/usr/bin/env python3
"""

    O QUÊ DEVE SER FEITO

    Você deverá implementar o fluxo de tratamento de dados descrito abaixo,
    utilizando o dataset a seguir como base:
    https://oto-public.s3.amazonaws.com/natal2021.zip

    Sua tarefa:

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

"""
import requests, re
from unidecode import unidecode
from loguru import logger
from zipfile import ZipFile
import pandas as dd


class FileGetter:
    """ 
        Downloads a file passed in 'url' variable,
        and write into 'path' variable value. 
    """

    def __init__(self, url: str, path: str):
        self.url = url
        self.path = path
        self.file_content = None
        self.extracted_filename = None
        self.file_encoding = None

    def _download_file(self) -> 'response.content':
        """ Downloads file by url and returns it in byte content. """
        logger.info(f"Downloading {self.url}")
        self.file_content = requests.get(self.url).content

    def _save_to_file(self) -> str: 
        """ Save to file specified in path variable. """

        with open(self.path, 'wb') as file:
            file.write(self.file_content)
            logger.info(f"Wrote to {self.path}")
            file.close()
        return self.path

    def _unzip_file(self) -> None:
        """ Unzip file, by path specified in 'self.path'. """
        output_dir = self.path.split('/')[1]
        with ZipFile(self.path, 'r') as zip_file:
             zip_file.extractall(output_dir)
             filename = zip_file.namelist().pop()
        
        self.extracted_filename = output_dir + '/' + filename 
        logger.info(f"File extracted to {self.extracted_filename}")

    def get_file_properties(self) -> str:
        """ Downloads and unzip it file and
            returns unziped filename full path. """
        self._download_file()
        self._save_to_file()
        self._unzip_file()
        
        with open(self.extracted_filename, 'r') as file:
             self.file_encoding = file.encoding 

        return (self.extracted_filename, self.file_encoding)

    def __str__(self):
        return self.extracted_filename


class StringSanitizer:
    """ Sanitize strings, removing whitespaces, replace UTF-8 chars,
    lower and special chars. """

    @staticmethod
    def remove_ws(func):
        """ Decorator function to remove whitespaces
            from beginning and end of a string.
            Ex: ' Porto Alegre ' -> 'Porto Alegre'.
        """
        def wrapper(self, string: str) -> str:
            string = re.sub('^\s*|\s*$','', string)
            return func(self, string)
        return wrapper
    
    @remove_ws
    def remove_whitespace(self, string):
        """ Remove whitespaces from beginning and end of a string.
            Ex: ' Porto Alegre ' -> 'Porto Alegre'.
        """
        return string
    
    def phone_sanitize(self, string: str) -> str:
        """ Remove non numbers chars from string """
        return re.sub('(?![0-9]).','', string) 

    @remove_ws 
    def to_ascii(self, string: str) -> str:
        """ Transform to ASCII, uppercase and with hiphens. """
        string = unidecode(string)
        string = re.sub('(?![0-9]|[a-zA-Z]|-|\s).','',string)
        string = string.upper()
        return string


def cleanup():
    """
        Cleanups the provided CSV following, requirements as described
        on the top of this file.
    """

    # 'url' is the variable with url containing zip file.
    # 'path' is the path where file must be uncompressed.
    url = 'https://oto-public.s3.amazonaws.com/natal2021.zip'
    path = './data' + '/' +  url.split('/')[-1]
    
    # Gets file from remote and returns the full path filename
    # of file, as file's encoding too.
    file_getter = FileGetter(url, path) 
    filename, file_encoding = file_getter.get_file_properties()
    
    # Initialize and read CSV file.
    string_sanitizer = StringSanitizer()
    csv = dd.read_csv(filename, sep=',',  encoding=file_encoding)
    logger.info(f"Updating {filename}.")
    
    iteration_n = 0
    for number, series in csv.iterrows():
        if iteration_n == 10000: 
            logger.info(f"Updated {iteration_n} rows")
            csv.to_csv(filename)
            iteration_n = 0

        csv.at[number, 'CUSTOMER_ID'] = string_sanitizer.remove_whitespace(
                series['CUSTOMER_ID'])
        csv.at[number, 'CITY'] = string_sanitizer.remove_whitespace(
                series['CITY'])
        csv.at[number, 'PHONE'] = string_sanitizer.phone_sanitize(
                series['PHONE'])
        csv.at[number, 'CITY_ASCII'] = string_sanitizer.to_ascii(
                series['CITY'])

        iteration_n += 1


if __name__ == '__main__':
   cleanup()

