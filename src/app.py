import streamlit as st
import dados 


def main():
    carros = dados.ler_carros()
    st.title("Dataset de carros")
    st.write("Ambiente inicial pronto")

    st.dataframe(carros)

if __name__ == "__main__":
    main()