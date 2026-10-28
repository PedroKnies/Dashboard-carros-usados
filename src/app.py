import streamlit as st

import dados

# Nomes legíveis para as colunas da tabela
NOMES_COLUNAS = {
    "nome": "Modelo",
    "ano": "Ano",
    "preco": "Preço (₹)",
    "faixa_preco": "Faixa de preço",
    "km_rodados": "Km rodados",
    "combustivel": "Combustível",
    "vendedor": "Vendedor",
    "transmissao": "Transmissão",
    "proprietario": "Proprietário",
    "consumo": "Consumo (kmpl)",
    "motor_cc": "Motor (cc)",
    "potencia_bhp": "Potência (bhp)",
    "assentos": "Assentos",
}


def formatar(valor, sufixo=""):
    """Formata números para exibir nas métricas."""
    if valor is None:
        return "—"
    return f"{valor:,.0f}{sufixo}".replace(",", ".")


def mostrar_metricas(carros):
    metricas = dados.calcular_metricas(carros)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de carros", formatar(metricas["total"]))
    col2.metric("Preço médio", formatar(metricas["preco_medio"], " ₹"))
    col3.metric("Preço mediano", formatar(metricas["preco_mediano"], " ₹"))

    col4, col5, col6 = st.columns(3)
    col4.metric("Km médio", formatar(metricas["km_medio"], " km"))
    col5.metric("Ano médio", f"{metricas['ano_medio']:.0f}" if metricas["ano_medio"] else "—")
    col6.metric("Combustível mais comum", metricas["combustivel_mais_comum"] or "—")


def montar_tabela(carros):
    """Troca os nomes das colunas pelos nomes legíveis."""
    linhas = []
    for carro in carros:
        linha = {}
        for campo, nome_legivel in NOMES_COLUNAS.items():
            linha[nome_legivel] = carro[campo]
        linhas.append(linha)
    return linhas


def mostrar_formulario(carros):
    """Formulário para adicionar um novo carro."""
    with st.expander("➕ Adicionar novo carro"):
        with st.form("form_novo_carro", clear_on_submit=True):
            nome = st.text_input("Modelo")
            col1, col2 = st.columns(2)
            ano = col1.number_input("Ano", min_value=1980, max_value=2030, value=2015)
            preco = col2.number_input("Preço (₹)", min_value=0, value=300000, step=10000)
            km = col1.number_input("Km rodados", min_value=0, value=50000, step=1000)
            assentos = col2.number_input("Assentos", min_value=1, max_value=14, value=5)
            combustivel = col1.selectbox("Combustível", dados.listar_categorias(carros, "combustivel"))
            vendedor = col2.selectbox("Vendedor", dados.listar_categorias(carros, "vendedor"))
            transmissao = col1.selectbox("Transmissão", dados.listar_categorias(carros, "transmissao"))
            proprietario = col2.selectbox("Proprietário", dados.listar_categorias(carros, "proprietario"))
            consumo = col1.number_input("Consumo (kmpl)", min_value=0.0, value=18.0)
            motor = col2.number_input("Motor (cc)", min_value=0, value=1200, step=50)
            potencia = col1.number_input("Potência (bhp)", min_value=0.0, value=80.0)

            enviado = st.form_submit_button("Salvar carro")

        if enviado:
            if nome.strip() == "":
                st.error("Informe o modelo do carro.")
            else:
                novo_carro = {
                    "nome": nome.strip(),
                    "ano": ano,
                    "preco": preco,
                    "km_rodados": km,
                    "combustivel": combustivel,
                    "vendedor": vendedor,
                    "transmissao": transmissao,
                    "proprietario": proprietario,
                    "consumo": consumo,
                    "motor_cc": motor,
                    "potencia_bhp": potencia,
                    "assentos": assentos,
                }
                dados.salvar_carro(novo_carro)
                st.success(f"{nome} adicionado com sucesso!")
                st.rerun()


def main():
    st.set_page_config(page_title="Carros usados na Índia", layout="wide")
    st.title("🚗 Carros usados na Índia")
    st.caption("Dataset CarDekho (Kaggle)")

    carros = dados.tratar_carros(dados.ler_carros())
    if len(carros) == 0:
        st.error("Não foi possível carregar os dados. Confira o arquivo carros-usados.csv.")
        return

    mostrar_formulario(carros)

    st.subheader("Métricas")
    mostrar_metricas(carros)

    st.subheader("Carros")
    col_busca, col_filtro = st.columns([2, 1])
    termo = col_busca.text_input("Buscar pelo modelo", placeholder="Ex.: swift, honda, i20...")
    opcoes = ["Todos"] + dados.listar_categorias(carros, "combustivel")
    combustivel = col_filtro.selectbox("Combustível", opcoes)

    resultado = dados.buscar_e_filtrar(carros, termo, combustivel)
    st.write(f"{len(resultado)} de {len(carros)} carros")

    if len(resultado) == 0:
        st.warning("Nenhum carro encontrado para essa busca e esse filtro.")
    else:
        st.dataframe(montar_tabela(resultado), hide_index=True)


if __name__ == "__main__":
    main()