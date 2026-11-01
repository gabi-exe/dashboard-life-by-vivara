import numpy as np
import pandas as pd
import plotly.graph_objects as go

CATALOGO = [
    ("P01", "Pulseira Life Sua História Prata 925", "Pulseiras", 590),
    ("P02", "Pulseira Life Rigid Fecho Coração", "Pulseiras", 490),
    ("P03", "Pulseira Life Malha Veneziana", "Pulseiras", 650),
    ("P04", "Pingente Life Coração Esmaltado Vermelho", "Pingentes", 180),
    ("P05", "Pingente Life Signos Prata", "Pingentes", 150),
    ("P06", "Pingente Life Letra Inicial Zircônia", "Pingentes", 130),
    ("P07", "Pingente Trava de Segurança Ponto de Luz", "Pingentes", 220),
    ("P08", "Pingente Life Árvore da Vida", "Pingentes", 190),
    ("P09", "Anel Life Solitário Prata 925", "Anéis", 290),
    ("P10", "Anel Life Wish Infinito Zircônias", "Anéis", 250),
    ("P11", "Anel Life Aliança Cravejada", "Anéis", 340),
    ("P12", "Brinco Life Argola Ponto de Luz", "Brincos", 320),
    ("P13", "Brinco Life Ear Cuff Zircônia Prata", "Brincos", 390),
    ("P14", "Brinco Life Segundo Furo Coração", "Brincos", 160),
]

ESTADOS = [
    ("SP", "São Paulo", 0.38),
    ("RJ", "Rio de Janeiro", 0.20),
    ("MG", "Minas Gerais", 0.14),
    ("PR", "Paraná", 0.10),
    ("RS", "Rio Grande do Sul", 0.08),
    ("BA", "Bahia", 0.06),
]

MESES = [
    ("2025-01", "Jan 2025", 0.80, ""),
    ("2025-02", "Fev 2025", 0.85, ""),
    ("2025-03", "Mar 2025", 0.90, "Lançamento Coleção"),
    ("2025-04", "Abr 2025", 0.95, ""),
    ("2025-05", "Mai 2025", 1.75, "Dia das Mães"),
    ("2025-06", "Jun 2025", 1.60, "Dia dos Namorados"),
    ("2025-07", "Jul 2025", 1.00, ""),
    ("2025-08", "Ago 2025", 1.10, ""),
    ("2025-09", "Set 2025", 0.95, "Semana do Brasil"),
    ("2025-10", "Out 2025", 1.05, ""),
    ("2025-11", "Nov 2025", 1.85, "Black Friday"),
    ("2025-12", "Dez 2025", 2.30, "Natal"),
]

CATEGORIAS = ["Pulseiras", "Pingentes", "Anéis", "Brincos"]
CANAIS = ["Loja Física", "E-commerce"]

OURO = "#D4AF37"
OURO_ESCURO = "#B8860B"
OURO_CANAL = "#C5A059"
INDIGO = "#4F46E5"
INDIGO_CLARO = "#6366F1"
CARVAO = "#1A1A1E"
CINZA = "#6B7280"
GRADE = "#E5E7EB"


def brl(valor):
    texto = f"{valor:,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def inteiro(valor):
    return f"{int(valor):,}".replace(",", ".")


def rotulo_mes(ref):
    if ref == "Todos":
        return "Todo o Ano (2025)"
    for r, rotulo, _, evento in MESES:
        if r == ref:
            return f"{rotulo} ({evento})" if evento else rotulo
    return ref


def gerar_dados(semente=2025):
    rng = np.random.default_rng(semente)
    acumulado = np.cumsum([e[2] for e in ESTADOS])
    linhas = []
    contador = 10001
    for ref, rotulo, fator, evento in MESES:
        for _ in range(int(140 * fator)):
            _, nome, categoria, preco = CATALOGO[rng.integers(len(CATALOGO))]
            sorteio_qtd = rng.random()
            qtd = 3 if sorteio_qtd > 0.85 else 2 if sorteio_qtd > 0.65 else 1
            posicao = int(np.searchsorted(acumulado, rng.random()))
            uf = ESTADOS[posicao][0] if posicao < len(ESTADOS) else "SP"
            linhas.append({
                "pedido": f"LIV-{contador}",
                "data": f"{ref}-{rng.integers(1, 29):02d}",
                "mes": ref,
                "rotulo_mes": rotulo,
                "produto": nome,
                "categoria": categoria,
                "preco_unit": preco,
                "qtd": qtd,
                "total": preco * qtd,
                "canal": "Loja Física" if rng.random() < 0.68 else "E-commerce",
                "uf": uf,
            })
            contador += 1
    return pd.DataFrame(linhas)


def calcular_kpis(df):
    receita = float(df["total"].sum())
    pedidos = len(df)
    if pedidos:
        por_produto = df.groupby("produto")["qtd"].sum()
        campeao, campeao_qtd = por_produto.idxmax(), int(por_produto.max())
    else:
        campeao, campeao_qtd = "Nenhum", 0
    return {
        "receita": receita,
        "itens": int(df["qtd"].sum()),
        "pedidos": pedidos,
        "ticket": receita / pedidos if pedidos else 0.0,
        "campeao": campeao,
        "campeao_qtd": campeao_qtd,
    }


def dados_estados(df):
    serie = df.groupby("uf")["total"].sum().sort_values(ascending=False)
    return list(serie.items())


def dados_canais(df):
    serie = df.groupby("canal")["total"].sum().reindex(CANAIS, fill_value=0)
    return list(serie.items())


def _base(fig, altura):
    fig.update_layout(
        height=altura,
        margin=dict(l=0, r=8, t=8, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Open Sans, system-ui, sans-serif", color=CINZA, size=12),
        showlegend=False,
        hoverlabel=dict(bgcolor=CARVAO, font=dict(color="#FFFFFF"), bordercolor=CARVAO),
    )
    fig.update_xaxes(showgrid=False, tickfont=dict(size=11), automargin=True)
    fig.update_yaxes(gridcolor=GRADE, griddash="dash", zeroline=False, tickprefix="R$ ", ticksuffix="k", tickformat=".0f")
    return fig


def fig_evolucao(df):
    serie = df.groupby("mes")["total"].sum().reindex([m[0] for m in MESES], fill_value=0)
    fig = go.Figure(go.Scatter(
        x=[m[1] for m in MESES],
        y=serie.values / 1000,
        customdata=[brl(v) for v in serie.values],
        mode="lines",
        line=dict(color=OURO_ESCURO, width=3, shape="spline"),
        fill="tozeroy",
        fillcolor="rgba(212,175,55,0.25)",
        hovertemplate="%{x}: %{customdata}<extra></extra>",
    ))
    _base(fig, 290)
    fig.update_xaxes(range=[-0.4, 11.4])
    return fig


def fig_top_produtos(df):
    serie = df.groupby("produto")["total"].sum().nlargest(6).iloc[::-1]
    nomes = [n if len(n) <= 22 else n[:22] + "..." for n in serie.index]
    cores = [INDIGO_CLARO] * len(serie)
    if cores:
        cores[-1] = OURO_ESCURO
    fig = go.Figure(go.Bar(
        x=serie.values / 1000,
        y=nomes,
        orientation="h",
        marker_color=cores,
        customdata=[brl(v) for v in serie.values],
        hovertemplate="%{y}: %{customdata}<extra></extra>",
    ))
    _base(fig, 290)
    fig.update_layout(bargap=0.45)
    fig.update_xaxes(showgrid=True, gridcolor=GRADE, griddash="dash", tickprefix="R$ ", ticksuffix="k", tickformat=".0f")
    fig.update_yaxes(showgrid=False, tickprefix="", ticksuffix="", tickformat=None)
    return fig


def fig_categorias(df):
    serie = df.groupby("categoria")["total"].sum().reindex(CATEGORIAS, fill_value=0)
    fig = go.Figure(go.Bar(
        x=serie.index,
        y=serie.values / 1000,
        marker_color=OURO_CANAL,
        customdata=[brl(v) for v in serie.values],
        hovertemplate="%{x}: %{customdata}<extra></extra>",
    ))
    _base(fig, 230)
    fig.update_layout(bargap=0.4)
    return fig


def fig_canais(df):
    canais = dados_canais(df)
    fig = go.Figure(go.Pie(
        labels=[c[0] for c in canais],
        values=[c[1] for c in canais],
        hole=0.68,
        sort=False,
        textinfo="none",
        marker=dict(colors=[OURO_CANAL, INDIGO], line=dict(color="#FFFFFF", width=3)),
        hovertemplate="%{label}: R$ %{value:,.2f}<extra></extra>",
    ))
    fig.update_layout(
        height=210,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        hoverlabel=dict(bgcolor=CARVAO, font=dict(color="#FFFFFF")),
    )
    return fig


CUSTO_PERCENTUAL = {
    "P01": 0.46, "P02": 0.42, "P03": 0.50,
    "P04": 0.30, "P05": 0.38, "P06": 0.28, "P07": 0.33, "P08": 0.31,
    "P09": 0.44, "P10": 0.36, "P11": 0.47,
    "P12": 0.35, "P13": 0.42, "P14": 0.27,
}
CUSTOS = {nome: round(preco * CUSTO_PERCENTUAL[codigo], 2) for codigo, nome, _, preco in CATALOGO}


def pct(valor):
    return f"{valor:.1f}".replace(".", ",") + "%"


def com_lucro(df, variacao=0.0):
    df = df.copy()
    df["custo_total"] = df["produto"].map(CUSTOS) * (1 + variacao) * df["qtd"]
    df["lucro"] = df["total"] - df["custo_total"]
    return df


def rentabilidade_categorias(df):
    g = df.groupby("categoria").agg(receita=("total", "sum"), custo=("custo_total", "sum"), lucro=("lucro", "sum"), itens=("qtd", "sum"))
    g = g.reindex(CATEGORIAS, fill_value=0.0)
    g["margem"] = np.where(g["receita"] > 0, g["lucro"] / g["receita"].replace(0, np.nan) * 100, 0.0)
    return g


def _insight(rent):
    receita_total = rent["receita"].sum()
    if receita_total <= 0 or (rent["receita"] > 0).sum() < 2:
        return ""
    lider_receita = rent["receita"].idxmax()
    lider_margem = rent["margem"].idxmax()
    lider_lucro = rent["lucro"].idxmax()
    parte = rent.loc[lider_receita, "receita"] / receita_total * 100
    if lider_receita != lider_margem:
        texto = (
            f"{lider_receita} lidera em faturamento ({pct(parte)} da receita), mas {lider_margem} tem a maior margem "
            f"({pct(rent.loc[lider_margem, 'margem'])} contra {pct(rent.loc[lider_receita, 'margem'])})."
        )
        if lider_lucro != lider_receita:
            texto += f" Em lucro bruto absoluto, quem lidera é {lider_lucro}."
        return texto
    return f"{lider_receita} lidera tanto em faturamento ({pct(parte)} da receita) quanto em margem ({pct(rent.loc[lider_receita, 'margem'])})."


def resumo_lucro(df, rent):
    receita = float(df["total"].sum())
    lucro = float(df["lucro"].sum())
    lider = rent["lucro"].idxmax() if receita > 0 else "Nenhuma"
    return {
        "receita": receita,
        "custo": float(df["custo_total"].sum()),
        "lucro": lucro,
        "margem": lucro / receita * 100 if receita else 0.0,
        "lider": lider,
        "margem_lider": float(rent.loc[lider, "margem"]) if receita > 0 else 0.0,
        "insight": _insight(rent),
    }


def fig_rentabilidade(rent):
    fig = go.Figure([
        go.Bar(name="Receita", x=rent.index, y=rent["receita"] / 1000, marker_color="#E6D9B5",
               customdata=[brl(v) for v in rent["receita"]], hovertemplate="%{x}: %{customdata}<extra>Receita</extra>"),
        go.Bar(name="Lucro bruto", x=rent.index, y=rent["lucro"] / 1000, marker_color=OURO_ESCURO,
               text=[pct(m) if r > 0 else "" for m, r in zip(rent["margem"], rent["receita"])], textposition="outside",
               customdata=[brl(v) for v in rent["lucro"]], hovertemplate="%{x}: %{customdata}<extra>Lucro bruto</extra>"),
    ])
    _base(fig, 300)
    fig.update_layout(barmode="group", bargap=0.3, showlegend=True, legend=dict(orientation="h", y=1.12, x=0))
    return fig


def fig_margem_produtos(df):
    g = df.groupby("produto").agg(receita=("total", "sum"), lucro=("lucro", "sum"))
    g = g[g["receita"] > 0]
    g["margem"] = g["lucro"] / g["receita"] * 100
    g = g.sort_values("margem")
    nomes = [n if len(n) <= 30 else n[:30] + "..." for n in g.index]
    cores = [INDIGO_CLARO] * len(g)
    if cores:
        cores[-1] = OURO_ESCURO
    fig = go.Figure(go.Bar(
        x=g["margem"], y=nomes, orientation="h", marker_color=cores,
        text=[pct(m) for m in g["margem"]], textposition="outside", cliponaxis=False,
        hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
    ))
    _base(fig, 300)
    fig.update_layout(bargap=0.35, margin=dict(l=0, r=40, t=8, b=0))
    fig.update_xaxes(showgrid=True, gridcolor=GRADE, griddash="dash", tickprefix="", ticksuffix="%", tickformat=".0f", range=[0, 100])
    fig.update_yaxes(showgrid=False, tickprefix="", ticksuffix="", tickformat=None, tickfont=dict(size=10))
    return fig
