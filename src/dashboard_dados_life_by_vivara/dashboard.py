import pandas as pd
import streamlit as st

import componentes as ui
from vendas import (
    CATEGORIAS, CANAIS, com_lucro, fig_margem_produtos, fig_rentabilidade, rentabilidade_categorias, resumo_lucro, MESES, calcular_kpis, dados_canais, dados_estados, gerar_dados,
    fig_canais, fig_categorias, fig_evolucao, fig_top_produtos, rotulo_mes,
)

st.set_page_config(page_title="Life by Vivara · Vendas & Performance", page_icon="💎", layout="wide")

st.html(
    f"""
    <style>
    @import url('{ui.FONTES}');
    .stApp, .stApp p, .stApp label, .stApp input, .stApp button, .stApp textarea, .stApp span:not([data-testid="stIconMaterial"]) {{font-family: "Open Sans", system-ui, sans-serif;}}
    #MainMenu, footer, header {{visibility: hidden;}}
    .stApp {{background: #FAF7F5; color-scheme: light;}}
    .block-container {{max-width: 1280px; padding-top: 2rem;}}
    [data-testid="stVerticalBlockBorderWrapper"] {{background: #fff; border-radius: 12px; border-color: #e7e5e4;}}
    [data-testid="stAppViewContainer"], [data-testid="stMarkdownContainer"] p, [data-testid="stSlider"] * {{color: #1c1917;}}
    [data-testid="stWidgetLabel"] p, [data-testid="stCaptionContainer"] p {{color: #44403c !important;}}
    [data-testid="stSelectbox"] div, [data-testid="stSelectbox"] input,
    [data-testid="stTextInput"] div, [data-testid="stTextInput"] input {{background-color: #fff !important; color: #1c1917 !important; -webkit-text-fill-color: #1c1917 !important;}}
    [data-testid="stSelectbox"] svg {{fill: #1c1917 !important; color: #1c1917 !important;}}
    [data-testid="stSelectboxVirtualDropdown"], [data-testid="stSelectboxVirtualDropdown"] *, [role="listbox"], [role="listbox"] *, [role="option"] {{background-color: #fff !important; color: #1c1917 !important;}}
    [role="option"]:hover, [role="option"][aria-selected="true"] {{background-color: #FFFBEB !important;}}
    button[data-testid^="stBaseButton-"] {{background-color: #fff !important; border: 1px solid #d6d3d1 !important; border-radius: 8px !important;}}
    button[data-testid^="stBaseButton-"], button[data-testid^="stBaseButton-"] * {{color: #1c1917 !important;}}
    button[data-testid^="stBaseButton-"]:hover:not(:disabled) {{border-color: #B8860B !important; background-color: #FFFBEB !important;}}
    button[data-testid^="stBaseButton-"]:disabled {{opacity: .45;}}
    {ui.CSS}
    </style>
    """
)

PADROES = {"categoria": "Todas", "canal": "Todos", "mes": "Todos", "busca": "", "pagina": 1, "ordem": "Data", "sentido": "Decrescente", "variacao_custo": 0}
for chave, valor in PADROES.items():
    st.session_state.setdefault(chave, valor)

COLUNAS_ORDEM = {
    "ID Pedido": "pedido", "Data": "data", "Produto": "produto", "Categoria": "categoria",
    "Canal": "canal", "UF": "uf", "Qtd": "qtd", "Valor Total": "total",
}
POR_PAGINA = 7
CONFIG = {"displayModeBar": False}


def limpar_filtros():
    for chave, valor in PADROES.items():
        st.session_state[chave] = valor


def voltar_pagina():
    st.session_state.pagina = 1


def mudar_pagina(delta):
    st.session_state.pagina += delta


@st.cache_data
def carregar():
    return gerar_dados()


df = carregar()

st.html(ui.cabecalho())
st.write("")

df = com_lucro(df, st.session_state.variacao_custo / 100)


with st.container(border=True):
    topo, botao = st.columns([5, 1])
    topo.markdown("**🔎 Filtros Globais de Visualização**")
    botao.button("Limpar filtros", on_click=limpar_filtros, width="stretch")
    c1, c2, c3, c4 = st.columns(4)
    c1.selectbox("Categoria de Produto", ["Todas"] + CATEGORIAS, key="categoria", on_change=voltar_pagina)
    c2.selectbox("Canal de Venda", ["Todos"] + CANAIS, key="canal", on_change=voltar_pagina)
    c3.selectbox("Período / Mês", ["Todos"] + [m[0] for m in MESES], key="mes", format_func=rotulo_mes, on_change=voltar_pagina)
    c4.text_input("Busca Direta", key="busca", placeholder="Nome do produto, ID ou UF...", on_change=voltar_pagina)

filtrado = df
if st.session_state.categoria != "Todas":
    filtrado = filtrado[filtrado["categoria"] == st.session_state.categoria]
if st.session_state.canal != "Todos":
    filtrado = filtrado[filtrado["canal"] == st.session_state.canal]
if st.session_state.mes != "Todos":
    filtrado = filtrado[filtrado["mes"] == st.session_state.mes]
termo = st.session_state.busca.strip().lower()
if termo:
    alvo = filtrado["produto"].str.lower() + " " + filtrado["pedido"].str.lower() + " " + filtrado["uf"].str.lower()
    filtrado = filtrado[alvo.str.contains(termo, regex=False)]

st.write("")
for coluna, cartao in zip(st.columns(4), ui.cartoes_kpi(calcular_kpis(filtrado))):
    coluna.html(cartao)

st.write("")
esq, dir_ = st.columns([2, 1])
with esq.container(border=True):
    st.html(ui.titulo("📅 Evolução Mensal &amp; Sazonalidade de Vendas", "Curva de faturamento nos principais picos festivos do ano", ui.etiqueta_picos()))
    st.plotly_chart(fig_evolucao(filtrado), width="stretch", config=CONFIG)
with dir_.container(border=True):
    st.html(ui.titulo("✨ Top Produtos por Receita", "Itens com maior rentabilidade financeira"))
    st.plotly_chart(fig_top_produtos(filtrado), width="stretch", config=CONFIG)

a, b, c = st.columns(3)
with a.container(border=True):
    st.html(ui.titulo("Performance por Categoria", "Receita acumulada por tipo de joia"))
    st.plotly_chart(fig_categorias(filtrado), width="stretch", config=CONFIG)
with b.container(border=True):
    st.html(ui.titulo("Participação por Canal", "Loja Física vs. E-commerce Oficial"))
    st.plotly_chart(fig_canais(filtrado), width="stretch", config=CONFIG)
    st.html(ui.legenda_canais(dados_canais(filtrado)))
with c.container(border=True):
    st.html(ui.titulo("Vendas por Estado (UF)", "Principais mercados consumidores"))
    st.html(ui.barras_estados(dados_estados(filtrado)))

rent = rentabilidade_categorias(filtrado)
resumo = resumo_lucro(filtrado, rent)
with st.container(border=True):
    st.html(ui.titulo("💰 Margem de Lucro e Rentabilidade por Categoria", "Lucro bruto = receita − custo estimado de prata, materiais e fabricação (premissas fictícias por produto)"))
    st.slider("Variação no custo de matéria-prima (%)", -20, 40, key="variacao_custo", help="Simula alta ou queda no preço da prata e dos materiais e recalcula lucro e margem")
    for coluna, cartao in zip(st.columns(3), ui.cartoes_lucro(resumo)):
        coluna.html(cartao)
    if resumo["insight"]:
        st.html(ui.insight(resumo["insight"]))
    gl, gr = st.columns(2)
    with gl:
        st.html(ui.titulo("Receita x Lucro bruto", "Rótulo acima da barra = margem da categoria"))
        st.plotly_chart(fig_rentabilidade(rent), width="stretch", config=CONFIG)
    with gr:
        st.html(ui.titulo("Margem por produto", "Quanto sobra de cada R$ 100 vendidos"))
        st.plotly_chart(fig_margem_produtos(filtrado), width="stretch", config=CONFIG)
    st.html(ui.tabela_rentabilidade(rent))

with st.container(border=True):
    st.html(ui.titulo("Registro Detalhado de Vendas", f"Exibindo <b>{len(filtrado)}</b> transações encontradas"))
    o1, o2, _ = st.columns([1, 1, 2])
    o1.selectbox("Ordenar por", list(COLUNAS_ORDEM), key="ordem", on_change=voltar_pagina)
    o2.selectbox("Sentido", ["Decrescente", "Crescente"], key="sentido", on_change=voltar_pagina)

    coluna = COLUNAS_ORDEM[st.session_state.ordem]
    ordenado = filtrado.sort_values(
        coluna,
        ascending=st.session_state.sentido == "Crescente",
        kind="stable",
        key=lambda s: s if pd.api.types.is_numeric_dtype(s) else s.str.lower(),
    )
    paginas = max(1, -(-len(ordenado) // POR_PAGINA))
    st.session_state.pagina = min(max(st.session_state.pagina, 1), paginas)
    pagina = st.session_state.pagina
    inicio = (pagina - 1) * POR_PAGINA

    st.html(ui.tabela(ordenado.iloc[inicio:inicio + POR_PAGINA]))

    r1, r2, r3 = st.columns([3, 2, 1])
    ate = min(pagina * POR_PAGINA, len(ordenado))
    r1.caption(f"Mostrando {inicio + 1 if len(ordenado) else 0} até {ate} de {len(ordenado)} registros")
    anterior, centro, proxima = r2.columns([1, 1, 1])
    anterior.button("‹", on_click=mudar_pagina, args=(-1,), disabled=pagina == 1, key="ant", width="stretch")
    centro.html(f"<div style='text-align:center;padding-top:6px;color:#1c1917'><b>{pagina} / {paginas}</b></div>")
    proxima.button("›", on_click=mudar_pagina, args=(1,), disabled=pagina == paginas, key="prox", width="stretch")

st.html(ui.rodape())
