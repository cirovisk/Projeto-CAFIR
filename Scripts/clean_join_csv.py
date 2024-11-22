import os
import re
import csv
from datetime import datetime

#Será necessário fazer a limpeza dos arquivos baixados, pois o CSV original se dividia por tamanho,
#não por delimitador, resultando em um arquivo com várias colunas em uma única coluna.
#O separador escolhido foi ; devido a presença de vírgulas em alguns campos.
#A intenção desse script é separar essas colunas, retirar espaços em branco extras e converter a data para o formato correto.
#Assim o arquivo estará pronto para ser inserido em BDs e utilizável para visualização.

tamanho_campo = [(0, 8), (8, 17), (17, 30), (30, 85), (85, 87), (87, 143), (143, 183), (183, 185), (185, 225), (225, 233), (233, 241), (241, 244), (244, 255)]
cabecalho = ["NIRF - Número do imóvel na Receita Federal", "Área total do imóvel (em hectares)", "Código do imóvel no Incra", "Nome do imóvel rural", "Situação do Imóvel", "Logradouro de localização do imóvel", "Distrito de localização do imóvel", "UF de localização do imóvel", "Município de localização do Imóvel", "CEP de localização do imóvel", "Data de atualização do cadastro", "Imune ou Isento", "Código SNCR"]

def adicionar_separadores(linha):
    return [linha[comeco:fim].strip() for comeco, fim in tamanho_campo]

def remover_espaços_extras(texto):
    return re.sub(r'\s{2,}', ' ', texto)

def converter_data(data_str):
    try:
        return datetime.strptime(data_str, '%Y%m%d').strftime('%Y-%m-%d')
    except ValueError:
        return data_str

def limpar_linha(linha):
    linha = adicionar_separadores(linha.replace(';', ' ').strip())
    linha = [remover_espaços_extras(campo) for campo in linha]
    if len(linha) >= 3:
        linha[-3] = converter_data(linha[-3])
    return [campo.strip() for campo in linha]

def unir_csvs(input_pasta, output_arquivo):
    with open(output_arquivo, 'w', encoding='latin1', newline='') as saida:
        writer = csv.writer(saida, delimiter=';')
        writer.writerow(cabecalho)
        for filename in os.listdir(input_pasta):
            if filename.endswith('.csv'):
                with open(os.path.join(input_pasta, filename), 'r', encoding='latin1', newline='') as entrada:
                    for linha in entrada:
                        writer.writerow(limpar_linha(linha))
                print(f'Processado: {filename}')

input_pasta = 'arquivos CSV'
output_arquivo = 'CSVs_unidos.csv'
unir_csvs(input_pasta, output_arquivo)