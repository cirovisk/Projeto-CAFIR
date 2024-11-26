import csv
import os
from datetime import datetime
from tqdm import tqdm

# O CSV original se dividia por tamanho fixo, não por delimitador.
# O separador escolhido foi ; devido a presença de vírgulas em alguns campos.
# A intenção desse script é separar essas colunas, retirar espaços em branco extras e converter a data para o formato correto.
# Assim o arquivo estará pronto para ser inserido em BDs e otimizado para visualização.

tamanho_campo = [(0, 8), (8, 17), (17, 30), (30, 85), (85, 87), (87, 143), (143, 183), (183, 185), (185, 225), (225, 233), (233, 241), (241, 244), (244, 255)]
cabecalho = ["NIRF", "hectares", "codigo_incra", "nome", "situacao", "logradouro", "distrito", "UF", "municipio", "CEP", "data_att_cadastro", "imunte_isento", "SNCR"]

def adicionar_separadores(linha):
    campos = [linha[start:end].strip() for start, end in tamanho_campo]
    return campos

def remover_espaços_extras(campo):
    return campo.strip()

def converter_data(data_str):
    try:
        return datetime.strptime(data_str, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        return data_str

def limpar_linha(linha):
    linha = adicionar_separadores(linha)
    linha = [remover_espaços_extras(campo) for campo in linha]
    if len(linha) >= 11:
        linha[10] = converter_data(linha[10])
    if len(linha) >= 12:
        if linha[11] == "SIM":
            linha[11] = 1
        elif linha[11] == "NAO":
            linha[11] = 0
    return linha

def limpar_csv(input_arquivo, output_arquivo):
    print(f'Iniciando processamento do arquivo: {input_arquivo}')
    with open(input_arquivo, 'r', encoding='latin1') as entrada, open(output_arquivo, 'w', encoding='latin1', newline='') as saida:
        reader = csv.reader(entrada, delimiter=';')
        writer = csv.writer(saida, delimiter=';')
        writer.writerow(cabecalho)
        for linha in tqdm(reader):
            linha_limpa = limpar_linha(linha[0])
            writer.writerow(linha_limpa)
    os.remove(input_arquivo)
    print(f'Arquivo de input {input_arquivo} deletado.')

input_arquivo = 'CSV_CAFIR.csv'
output_arquivo = 'CSV_CAFIR_limpo.csv'
limpar_csv(input_arquivo, output_arquivo)
