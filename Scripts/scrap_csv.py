import os
import csv
import requests
from bs4 import BeautifulSoup

class CSVDownloader:
    def __init__(self, base_url, pasta_download, arquivo_unido):
        self.base_url = base_url
        self.pasta_download = pasta_download
        self.arquivo_unido = arquivo_unido
        os.makedirs(self.pasta_download, exist_ok=True)

    def fetch_page(self):
        resposta = requests.get(self.base_url)
        if resposta.status_code == 200:
            return BeautifulSoup(resposta.content, 'html.parser')
        else:
            print(f'Falha ao acessar a página. Código: {resposta.status_code}')
            return None

    def pegar_links_csv(self, soup):
        links = soup.find_all('a')
        csv_links = [link.get('href') for link in links if link.get('href') and '.csv' in link.get('href')]
        return csv_links

    def download_csv(self, csv_url):
        resposta = requests.get(csv_url)
        if resposta.status_code == 200:
            file_name = os.path.join(self.pasta_download, os.path.basename(csv_url))
            with open(file_name, 'wb') as file:
                file.write(resposta.content)
            print(f'Arquivo salvo: {file_name}')
            return file_name
        else:
            print(f'Falha ao baixar {csv_url}. Código: {resposta.status_code}')
            return None

    def unir_csvs(self, arquivos_csv):
        with open(self.arquivo_unido, 'w', encoding='latin1', newline='') as saida:
            writer = csv.writer(saida, delimiter=';')
            cabecalho_escrito = False
            for arquivo in arquivos_csv:
                with open(arquivo, 'r', encoding='latin1', newline='') as entrada:
                    reader = csv.reader(entrada, delimiter=';')
                    cabecalho = next(reader)
                    if not cabecalho_escrito:
                        writer.writerow(cabecalho)
                        cabecalho_escrito = True
                    for linha in reader:
                        writer.writerow(linha)
                os.remove(arquivo)  # Deletando o arquivo de input após o processamento
                print(f'Arquivo deletado: {arquivo}')

    def run(self):
        soup = self.fetch_page()
        if soup:
            csv_links = self.pegar_links_csv(soup)
            arquivos_csv = []
            for link in csv_links:
                csv_url = link if link.startswith('http') else self.base_url + link
                arquivo = self.download_csv(csv_url)
                if arquivo:
                    arquivos_csv.append(arquivo)
            self.unir_csvs(arquivos_csv)

base_url = 'https://dadosabertos.rfb.gov.br/CAFIR/'
pasta_download = 'CSV_CAFIR'
arquivo_unido = 'CSV_CAFIR.csv'

downloader = CSVDownloader(base_url, pasta_download, arquivo_unido)
downloader.run()