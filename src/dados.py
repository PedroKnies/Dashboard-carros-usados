import csv
from pathlib import Path
from statistics import mean, median

CAMINHO_DADOS = Path(__file__).parent / "carros-usados.csv"

# Números escritos por extenso que podem aparecer no arquivo
NUMEROS_EXTENSO = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
}


# ---------------------------------------------------------------
# 1. Leitura do CSV
# ---------------------------------------------------------------
def ler_carros():
    """Lê o CSV e devolve uma lista de dicionários (tudo ainda como texto)."""
    carros = []
    try:
        with open(CAMINHO_DADOS, "r", encoding="utf-8-sig", newline="") as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                carros.append(linha)
    except FileNotFoundError:
        print("O arquivo carros-usados.csv não foi encontrado")
    except Exception as erro:
        print("Algum erro aconteceu na leitura do arquivo", erro)

    return carros


# ---------------------------------------------------------------
# 2. Conversão das colunas
# ---------------------------------------------------------------
def converter_numero(texto):
    """Transforma '23.4 kmpl', '1,248 CC', '₹4.5 Lakh' ou 'five' em número.

    Se não der para converter, devolve None.
    """
    if texto is None:
        return None

    texto = texto.strip().lower()
    if texto == "":
        return None

    if texto in NUMEROS_EXTENSO:
        return NUMEROS_EXTENSO[texto]

    multiplicador = 1
    if "lakh" in texto:
        multiplicador = 100000
    elif "crore" in texto:
        multiplicador = 10000000

    texto = texto.replace(",", "").replace("₹", "")
    primeira_parte = texto.split()[0]  # pega só o número, sem a unidade

    try:
        return float(primeira_parte) * multiplicador
    except ValueError:
        return None


def classificar_faixa_preco(preco):
    """Classifica o carro em uma faixa a partir do preço (em rúpias)."""
    if preco is None:
        return "Sem preço"
    if preco <= 300000:
        return "Econômico (até 3 lakh)"
    if preco <= 600000:
        return "Intermediário (3 a 6 lakh)"
    if preco <= 1000000:
        return "Alto (6 a 10 lakh)"
    return "Premium (acima de 10 lakh)"


def tratar_carro(carro_bruto):
    """Cria um carro novo com os números já convertidos e a faixa de preço."""
    preco = converter_numero(carro_bruto["preco_rupias"])

    carro = {
        "nome": carro_bruto["nome"].strip(),
        "ano": converter_numero(carro_bruto["ano"]),
        "preco": preco,
        "faixa_preco": classificar_faixa_preco(preco),
        "km_rodados": converter_numero(carro_bruto["km"]),
        "combustivel": carro_bruto["combustivel"].strip(),
        "vendedor": carro_bruto["vendedor"].strip(),
        "transmissao": carro_bruto["cambio"].strip(),
        "proprietario": carro_bruto["dono"].strip(),
        "consumo": converter_numero(carro_bruto["consumo"]),
        "motor_cc": converter_numero(carro_bruto["motor"]),
        "potencia_bhp": converter_numero(carro_bruto["potencia"]),
        "assentos": converter_numero(carro_bruto["assentos"]),
    }
    return carro


def tratar_carros(carros_brutos):
    carros = []
    for carro_bruto in carros_brutos:
        carros.append(tratar_carro(carro_bruto))
    return carros


# ---------------------------------------------------------------
# 3. Métricas
# ---------------------------------------------------------------
def calcular_metricas(carros):
    """Calcula as métricas do conjunto de carros recebido."""
    precos = [c["preco"] for c in carros if c["preco"] is not None]
    kms = [c["km_rodados"] for c in carros if c["km_rodados"] is not None]
    anos = [c["ano"] for c in carros if c["ano"] is not None]

    contagem = {}
    for carro in carros:
        tipo = carro["combustivel"]
        contagem[tipo] = contagem.get(tipo, 0) + 1

    metricas = {
        "total": len(carros),
        "preco_medio": mean(precos) if precos else None,
        "preco_mediano": median(precos) if precos else None,
        "km_medio": mean(kms) if kms else None,
        "ano_medio": mean(anos) if anos else None,
        "combustivel_mais_comum": max(contagem, key=contagem.get) if contagem else None,
    }
    return metricas


# ---------------------------------------------------------------
# 4. Busca e filtro
# ---------------------------------------------------------------
def listar_categorias(carros, campo):
    """Pega as opções direto dos dados, sem repetir e em ordem alfabética."""
    categorias = []
    for carro in carros:
        if carro[campo] != "" and carro[campo] not in categorias:
            categorias.append(carro[campo])
    return sorted(categorias)


def buscar_por_nome(carros, termo):
    """Busca texto no nome do carro, sem diferenciar maiúsculas de minúsculas."""
    termo = termo.strip().lower()
    encontrados = []
    for carro in carros:
        if termo in carro["nome"].lower():
            encontrados.append(carro)
    return encontrados


def filtrar_por_categoria(carros, campo, valor):
    """Filtra pela categoria escolhida. 'Todos' devolve todos os carros."""
    if valor == "Todos":
        return carros
    encontrados = []
    for carro in carros:
        if carro[campo] == valor:
            encontrados.append(carro)
    return encontrados


def buscar_e_filtrar(carros, termo, combustivel):
    """Usa a busca e o filtro juntos."""
    resultado = buscar_por_nome(carros, termo)
    resultado = filtrar_por_categoria(resultado, "combustivel", combustivel)
    return resultado


# ---------------------------------------------------------------
# 5. Adicionar novo carro (função extra do professor)
# ---------------------------------------------------------------
def salvar_carro(carro):
    """Adiciona um carro no final do CSV, no mesmo formato dos outros."""
    with open(CAMINHO_DADOS, "r", encoding="utf-8-sig", newline="") as arquivo:
        colunas = csv.DictReader(arquivo).fieldnames

    linha = {
        "nome": carro["nome"],
        "ano": carro["ano"],
        "preco_rupias": carro["preco"],
        "km": carro["km_rodados"],
        "combustivel": carro["combustivel"],
        "vendedor": carro["vendedor"],
        "cambio": carro["transmissao"],
        "dono": carro["proprietario"],
        "consumo": f"{carro['consumo']} kmpl",
        "motor": f"{carro['motor_cc']} CC",
        "potencia": f"{carro['potencia_bhp']} bhp",
        "assentos": carro["assentos"],
    }

    # garante que o novo carro não fique colado na última linha
    with open(CAMINHO_DADOS, "rb") as arquivo:
        conteudo = arquivo.read()
    precisa_quebra = len(conteudo) > 0 and not conteudo.endswith(b"\n")

    with open(CAMINHO_DADOS, "a", encoding="utf-8", newline="") as arquivo:
        if precisa_quebra:
            arquivo.write("\n")
        escritor = csv.DictWriter(
            arquivo, fieldnames=colunas, restval="", lineterminator="\n"
        )
        escritor.writerow(linha)


if __name__ == "__main__":
    carros = tratar_carros(ler_carros())
    print(f"{len(carros)} carros carregados")
    print(f"Primeiro carro: {carros[0]}")