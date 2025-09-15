import pandas as pd
import re
import os
from Normalizador import adjust_column_to_zero_mean


filepath = 'C:/Users/Gabri/OneDrive/Área de Trabalho/Orbital Effects/OHE graphene/YIG-Pt(10)-SLG/medida angular/'
Final_path = filepath + "I_X_Angulo.txt"

angle = 0

while angle <= 360:
    input_file = "{0}{1}".format(filepath,
                                 '-800 mA {} graus'.format(str(angle)))  # Substitua pelo caminho do seu arquivo de entrada
    output_file = input_file + "_ajustado.txt"  # Substitua pelo caminho do arquivo de saída

    # Chama a função e captura os valores retornados
    results = adjust_column_to_zero_mean(input_file, output_file)

    # Write the measured values on a file
    with open(Final_path, 'a') as file:
        if os.stat(Final_path).st_size == 0:
            file.write("Angle(°)   I(H>0)   SD(H>0)   I(H<0)   SD(H<0)\n")
        file.write("{:10.1f} {:18.8f} {:18.8f} {:18.8f} {:18.8f}\n".format(angle,
                                                                           results['mean_y_greater_than_100'],
                                                                           results['std_y_greater_than_100'],
                                                                           results['mean_y_less_than_neg_100'],
                                                                           results['std_y_less_than_neg_100']
                                                                           ).replace('.', ','))
    file.close()
    angle += 15
