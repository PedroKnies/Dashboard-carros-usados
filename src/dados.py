import csv 
from pathlib import Path

CAMINHO_DADOS = "carros-usados.csv"

def ler_carros():
    """Lê o CSV de carros e devolve uma lista de dicionários.

    Os valores vêm do jeito que estão no arquivo, ou seja, como texto:
    {"titulo": "Sharp Objects", "preco": "£47.82", "nota": "Four", ...}
    """
    carros = []
    try:
        with open(CAMINHO_DADOS, "r", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                carros.append(linha)
    except FileNotFoundError:
        print("O arquivo livros.csv não foi encontrado")
    except Exception as error:
        print("Algum erro aconteceu na leitura do arquivo", error)

    return carros


if __name__ == "__main__":
    carros = ler_carros()
    print(f"{len(carros)} livros carregados")
    print(f"Primeiro carro: {carros[0]}")