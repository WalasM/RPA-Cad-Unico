from datetime import datetime
import pandas as pd
import os
from pathlib import Path
import sqlite3
from src.services.services import (
    return_links,
    return_coluns_to_format
)

class CadastroUnico():
    def __init__(self):
        self.current_year = self.return_current_year() + 1
        self.dictionary_of_years_links = self.return_dictionary_of_years_links()
        self.list_bases = []
        self.base_main = None

    def return_current_year(self) -> int:
        """
        retorna o ano em que estamos
        """
        return datetime.now().year
    
    def return_dictionary_of_years_links(self) -> dict:
        """
        retorna um dicionario com todos os links disponiveis a partir de 2006
        """
        dict_links = {}
        for year in range(2006, self.current_year):
            dict_links.update({
                year: return_links(year)
            })
        return dict_links

    def generate_bases(self):
        """
        extrai a base de cada ano, a partir de 2006 até o ano atual(se disponivel) e salva os arquivos na pasta data/every_years
        """
        for link in self.dictionary_of_years_links:
            df = pd.read_csv(self.dictionary_of_years_links[link], sep=',')
            if len(df) == 0:
                continue
            self.list_bases.append(df)
            df.to_csv(Path(os.getcwd() + f"\data\every_years\{link}.csv"), sep=';', index=False)

    def generate_base_main(self):
        """
        gera um unico arquivo contendo todas as informações
        """
        file_main = pd.concat(self.list_bases)
        file_main.reset_index()
        file_main.to_csv(Path(os.getcwd() + rf"\data\file_main\todas_as_bases.csv"), sep=';', index=False)

        df = pd.read_csv(Path(os.getcwd() + rf"\data\file_main\todas_as_bases.csv"), sep=';', encoding='utf-8')
        df.fillna(0, inplace = True)
        colunas = return_coluns_to_format()
        for coluna in colunas:
            df[coluna] = df[coluna].astype(int)
        self.base_main = pd.read_csv(Path(os.getcwd() + rf"\data\file_main\todas_as_bases.csv"), sep=';', encoding='utf-8')

    def generate_database(self):
        """
        gera o banco e a tabela final para utilização da analise de dados
        """
        conexao = sqlite3.connect("BD_CAD_UNICO.db")
        self.base_main.to_sql(name='TBL_RENDA_PER_CAPITA', con=conexao, index=False)