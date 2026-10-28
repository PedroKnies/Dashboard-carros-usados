Dashboard-carros_usados
Membros: Felipe Domingues, Pedro Knies e Rafael Rosa

Dataset: carros-usados.csv

App publicado: https://dashboard-carros-usados.streamlit.app/

Funcionalidades
Leitura dos dados do arquivo CSV do dataset.
Conversão das colunas para formatos apropriados para os cálculos.
Apresentação de, no mínimo, três métricas sobre o dataset.
Classificação dos registros em faixas a partir de uma coluna numérica, com exibição da faixa na tabela.
Tabela com os dados e nomes de colunas legíveis.
Busca por texto que não diferencia letras maiúsculas de minúsculas.
Filtro por categoria com opções obtidas automaticamente dos dados e opção para mostrar todos os registros.
Funcionamento conjunto da busca por texto e do filtro por categoria.
Exibição de uma mensagem quando nenhum resultado é encontrado.
Código organizado em funções e módulos, com nomes adequados ao tema do grupo.
Aplicação publicada no Streamlit Community Cloud.
Funcionalidade extra

No sistema será possível inserir novos veiculos

Como rodar o projeto
Pré-requisitos
Python instalado no computador.
Git, caso deseje clonar o repositório.
Instalação e execução

Os comandos abaixo consideram o uso do PowerShell no Windows.

Clone o repositório e entre na pasta do projeto, caso ainda não esteja nela:
   git clone URL_DO_REPOSITORIO
   cd NOME_DA_PASTA

Crie o ambiente virtual:
   python -m venv .venv

Libere a execução do script de ativação apenas na janela atual do PowerShell:
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Ative o ambiente virtual:
   .venv\Scripts\Activate.ps1

Instale as dependências do projeto:
   pip install -r requirements.txt

Execute o aplicativo Streamlit:
   streamlit run src/app.py
