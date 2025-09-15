import pandas as pd
import re
import os


def adjust_column_to_zero_mean(input_file_path, output_file_path):
    # Lê o arquivo como texto bruto
    with open(input_file_path, 'r') as file:
        data = file.read()

    # Divide o texto em linhas
    lines = data.strip().split('\n')

    # Divide cada linha em colunas usando múltiplos espaços como delimitador
    data_rows = [re.split(r'\s{10,}', line.strip()) for line in lines]

    # Cria um DataFrame a partir dos dados processados
    df = pd.DataFrame(data_rows)

    # Verifica as primeiras linhas para entender a estrutura dos dados
    print("Dados lidos do arquivo:")
    print(df.head())

    # Função para substituir vírgulas por pontos e converter para float
    def convert_to_float(value):
        try:
            # Substitui vírgulas por pontos
            value = value.replace(',', '.')
            return float(value)
        except ValueError:
            return float('nan')

    # Converte as colunas para float, tratando notação científica armazenada como string
    df[0] = df[0].apply(convert_to_float)  # Converte a coluna x para float
    df[1] = df[1].apply(convert_to_float)  # Converte a coluna y para float

    # Remove os dois primeiros pontos das colunas (se houver pelo menos duas linhas)
    if len(df) > 2:
        df = df.iloc[2:].reset_index(drop=True)

    # Verifique se há valores NaN e imprima uma mensagem se houver
    if df[0].isna().any() or df[1].isna().any():
        print("Aviso: Alguns valores não puderam ser convertidos para números e foram definidos como NaN.")

    # Filtra os dados
    y_less_than_neg_100 = df[df[0] < -100][1]
    y_greater_than_100 = df[df[0] > 100][1]

    # Calcula os valores médios
    mean_y_less_than_neg_100 = y_less_than_neg_100.mean() if not y_less_than_neg_100.empty else float('nan')
    mean_y_greater_than_100 = y_greater_than_100.mean() if not y_greater_than_100.empty else float('nan')

    # Calcula o valor médio geral de y para os intervalos considerados
    mean_y = (mean_y_greater_than_100 + mean_y_less_than_neg_100)/2

    # Subtrai o valor médio de todos os pontos da coluna y
    df[1] = df[1] - mean_y

    # Filtra os dados
    y_less_than_neg_100 = df[df[0] < -100][1]
    y_greater_than_100 = df[df[0] > 100][1]

    # Calcula os valores médios
    mean_y_less_than_neg_100 = y_less_than_neg_100.mean() if not y_less_than_neg_100.empty else float('nan')
    std_y_less_than_neg_100 = y_less_than_neg_100.std() if not y_less_than_neg_100.empty else float('nan')

    mean_y_greater_than_100 = y_greater_than_100.mean() if not y_greater_than_100.empty else float('nan')
    std_y_greater_than_100 = y_greater_than_100.std() if not y_greater_than_100.empty else float('nan')

    # Função para converter float para string com vírgula
    def convert_to_comma_string(value):
        try:
            return '{:.8f}'.format(value).replace('.', ',')
        except ValueError:
            return 'nan'

    # Converte as colunas de volta para string com vírgula
    df[0] = df[0].apply(convert_to_comma_string)  # Converte a coluna x para string
    df[1] = df[1].apply(convert_to_comma_string)  # Converte a coluna y para string

    # Salvar o DataFrame ajustado em um novo arquivo de texto
    df.to_csv(output_file_path, sep=' ', index=False, header=False, float_format='%s')

    print(f"Coluna ajustada para média zero e salva em '{output_file_path}'.")
    return {
        'mean_y_less_than_neg_100': mean_y_less_than_neg_100,
        'std_y_less_than_neg_100': std_y_less_than_neg_100,
        'mean_y_greater_than_100': mean_y_greater_than_100,
        'std_y_greater_than_100': std_y_greater_than_100,
    }
