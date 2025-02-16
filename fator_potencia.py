import csv
import random
import os

CORRENTE_MINIMA=0.1
CORRENTE_MAXIMA=20
FATOR_POTENCIA_MINIMO=0.5
FATOR_POTENCIA_MAXIMO=0.97


def random_weighted(min_value, max_value):
    random_factor = random.random() ** (1/4)
    weighted_value = min_value + random_factor * (max_value - min_value)
    return round(weighted_value, 2)

   

def gerar_dados_fator_potencia(num_linhas):
    dados = []
    for _ in range(num_linhas):
        medidores = []
        soma_correntes = 0
        soma_fator_potencia = 0
        
        # Gerar dados para os 8 medidores
        for _ in range(8):
            corrente = round(random.uniform(CORRENTE_MINIMA, CORRENTE_MAXIMA), 2) 
            fator_potencia = random_weighted(FATOR_POTENCIA_MINIMO, FATOR_POTENCIA_MAXIMO)
            medidores.append({"corrente": corrente, "fator_potencia": fator_potencia})
            soma_correntes += corrente
            soma_fator_potencia += fator_potencia * corrente
        

        # Calcular o fator de potência do medidor central
        fator_potencia_central = soma_fator_potencia / soma_correntes if soma_correntes != 0 else 0
        
        proporcoes = [(1 - medidor["fator_potencia"]) * medidor["corrente"] for medidor in medidores]
        impacto_total = sum(proporcoes)
        impactos = [(100 * proporcao) / impacto_total for proporcao in proporcoes]


        # Determina se e qual medidor está impactando negativamente
        maior_impacto = max(impactos)
        if maior_impacto > 30 or fator_potencia_central < 0.92:
            label = f"MEDIDOR{impactos.index(maior_impacto) + 1}"
        else:
            label = "SEM_PROBLEMAS"

        # Adicionar os dados à lista
        linha = [medidor["corrente"] for medidor in medidores] + \
                [medidor["fator_potencia"] for medidor in medidores] + \
                [soma_correntes, fator_potencia_central, label]
        dados.append(linha)

    return dados

def salvar_csv(dados, nome_arquivo="../data/dados_fator_potencia.csv"):
    # Criar o diretório se não existir
    os.makedirs(os.path.dirname(nome_arquivo), exist_ok=True)

    cabecalhos = [f"corrente_{i+1}" for i in range(8)] + \
                 [f"fator_potencia_{i+1}" for i in range(8)] + \
                 ["corrente_central", "fator_potencia_central", "classe"]

    with open(nome_arquivo, mode="w", newline="") as arquivo:
        escritor_csv = csv.writer(arquivo)
        escritor_csv.writerow(cabecalhos)
        for linha in dados:
            escritor_csv.writerow([f"{valor:.2f}" if isinstance(valor, float) else valor for valor in linha])


num_linhas = int(input("Digite o número de linhas de dados a serem geradas: "))
dados = gerar_dados_fator_potencia(num_linhas)

salvar_csv(dados)
print(f"{num_linhas} linhas de dados foram salvas no arquivo 'dados_fator_potencia.csv'")