from vendas import ESTADOS, brl, inteiro, pct, OURO_CANAL, INDIGO

FONTES = "https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700&display=swap"

CSS = """
.lv, .lv * {box-sizing: border-box; font-family: "Open Sans", system-ui, sans-serif;}
.lv {color: #1c1917;}
.lv .serif, .lv h1, .lv h3 {font-family: "Open Sans", system-ui, sans-serif;}
.lv .hdr {position: relative; overflow: hidden; background: #fff; border: 1px solid #e7e5e4; border-radius: 16px; padding: 26px 24px 22px; box-shadow: 0 1px 2px rgba(0,0,0,.05);}
.lv .hdr .bar {position: absolute; top: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #D4AF37, #E8A598, #B8860B);}
.lv .brand {display: flex; align-items: center; gap: 16px;}
.lv .gem {width: 48px; height: 48px; border-radius: 12px; background: #1c1917; color: #D4AF37; display: flex; align-items: center; justify-content: center; font-size: 24px;}
.lv .meta {display: flex; align-items: center; gap: 8px; flex-wrap: wrap;}
.lv .badge {font-size: 11px; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; color: #B8860B; background: #FFF8EE; padding: 2px 10px; border-radius: 99px; border: 1px solid #E8D09E;}
.lv .mono {font-size: 12px; color: #57534e; font-family: ui-monospace, monospace;}
.lv h1 {font-size: 30px; line-height: 1.15; margin: 4px 0 0; color: #1c1917; font-weight: 700; letter-spacing: -.01em;}
.lv h1 span {font-family: "Open Sans", sans-serif; font-weight: 300; color: #B8860B;}
.lv .kpi {background: #fff; border: 1px solid #e7e5e4; border-radius: 12px; padding: 20px; box-shadow: 0 1px 2px rgba(0,0,0,.05); min-height: 150px;}
.lv .kpi .top {display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;}
.lv .kpi .rot {font-size: 11px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: #57534e;}
.lv .kpi .ico {width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px;}
.lv .kpi .val {font-family: "Open Sans", system-ui, sans-serif; font-size: 28px; font-weight: 700; color: #1c1917;}
.lv .kpi .val small {font-family: "Open Sans", sans-serif; font-size: 13px; font-weight: 400; color: #57534e;}
.lv .kpi .nome {font-size: 14px; font-weight: 700; color: #1c1917; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;}
.lv .kpi .pe {font-size: 12px; color: #57534e; margin-top: 8px;}
.lv .kpi .pe b {color: #1c1917;}
.lv .kpi .ok {color: #059669; font-weight: 500;}
.lv h3 {font-size: 17px; margin: 0; color: #1c1917;}
.lv .sub {font-size: 12px; color: #57534e; margin: 2px 0 8px;}
.lv .tag {display: inline-block; font-size: 12px; font-weight: 500; color: #92400e; background: #FFFBEB; padding: 4px 10px; border-radius: 6px; border: 1px solid #FDE68A;}
.lv .uf {margin-bottom: 12px;}
.lv .uf .l {display: flex; justify-content: space-between; font-size: 12px; font-weight: 500; color: #44403c; margin-bottom: 4px;}
.lv .uf .t {height: 8px; background: #f5f5f4; border-radius: 99px; overflow: hidden;}
.lv .uf .t i {display: block; height: 100%; background: #D4AF37; border-radius: 99px;}
.lv .leg {display: flex; justify-content: center; gap: 24px; padding-top: 8px; border-top: 1px solid #f5f5f4; font-size: 12px; font-weight: 500; color: #44403c;}
.lv .leg i {display: inline-block; width: 12px; height: 12px; border-radius: 99px; margin-right: 6px; vertical-align: -1px;}
.lv .tw {overflow-x: auto;}
.lv table {width: 100%; border-collapse: collapse; font-size: 12px; color: #44403c;}
.lv th {background: #fafaf9; text-transform: uppercase; font-weight: 600; color: #78716c; text-align: left; padding: 12px 14px; border-bottom: 1px solid #e7e5e4; white-space: nowrap;}
.lv td {padding: 11px 14px; border-bottom: 1px solid #f5f5f4; white-space: nowrap;}
.lv td.id {font-family: ui-monospace, monospace; font-weight: 600; color: #1c1917;}
.lv td.pr {font-weight: 500; color: #1c1917;}
.lv td.c {text-align: center;}
.lv td.r, .lv th.r {text-align: right;}
.lv th.c {text-align: center;}
.lv .pill {display: inline-block; padding: 2px 8px; font-size: 11px; font-weight: 500; border-radius: 4px; background: #f5f5f4; color: #44403c;}
.lv .ch {display: inline-block; padding: 2px 9px; font-size: 11px; font-weight: 500; border-radius: 99px;}
.lv .ch.loja {background: #FFFBEB; color: #92400e; border: 1px solid #FDE68A;}
.lv .ch.web {background: #EEF2FF; color: #4338ca; border: 1px solid #C7D2FE;}
.lv .insight {background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 10px; padding: 12px 14px; font-size: 13px; color: #78350f; margin: 12px 0;}
.lv .mb {display: inline-block; width: 80px; height: 8px; background: #f5f5f4; border-radius: 99px; vertical-align: middle; margin-right: 8px; overflow: hidden;}
.lv .mb i {display: block; height: 100%; background: #D4AF37;}
.lv .vazio {padding: 32px; text-align: center; color: #a8a29e;}
.lv .rodape {text-align: center; font-size: 12px; color: #57534e; border-top: 1px solid #e7e5e4; padding-top: 20px; margin-top: 24px;}
"""


def cabecalho():
    return (
        '<div class="lv"><div class="hdr"><div class="bar"></div><div class="brand">'
        '<div class="gem">💎</div><div><div class="meta">'
        '<span class="badge">Official Retail Analytics</span><span class="mono">Ano Base: 2025</span></div>'
        '<h1>Life by Vivara <span>— Vendas &amp; Performance</span></h1></div></div></div></div>'
    )


def _kpi(rotulo, corpo, pe, icone, fundo, cor):
    return (
        f'<div class="lv"><div class="kpi"><div class="top"><span class="rot">{rotulo}</span>'
        f'<div class="ico" style="background:{fundo};color:{cor}">{icone}</div></div>{corpo}{pe}</div></div>'
    )


def cartoes_kpi(k):
    return [
        _kpi("Faturamento Total", f'<div class="val">{brl(k["receita"])}</div>',
             '<div class="pe ok">+18.4% vs meta projetada</div>', "📈", "#FFFBEB", "#B8860B"),
        _kpi("Volume Vendido", f'<div class="val">{inteiro(k["itens"])} <small>peças</small></div>',
             f'<div class="pe">Em <b>{inteiro(k["pedidos"])}</b> pedidos realizados</div>', "🛍️", "#FFF1F2", "#E11D48"),
        _kpi("Ticket Médio por Venda", f'<div class="val">{brl(k["ticket"])}</div>',
             '<div class="pe">Preço médio por carrinho consolidado</div>', "💳", "#EEF2FF", "#4F46E5"),
        _kpi("Campeão de Vendas", f'<div class="nome" title="{k["campeao"]}">{k["campeao"]}</div>',
             f'<div class="pe">Total de <b>{inteiro(k["campeao_qtd"])} un.</b> comercializadas</div>', "🏅", "#FAF5FF", "#9333EA"),
    ]


def titulo(texto, sub, extra=""):
    return f'<div class="lv"><h3>{texto}</h3><div class="sub">{sub}</div>{extra}</div>'


def etiqueta_picos():
    return '<div class="lv"><span class="tag">Picos em Maio (Mães), Nov (Black Friday) e Dez (Natal)</span></div>'


def barras_estados(estados):
    if not estados:
        return '<div class="lv"><div class="vazio">Sem dados para os filtros atuais.</div></div>'
    nomes = {e[0]: e[1] for e in ESTADOS}
    maximo = estados[0][1] or 1
    itens = "".join(
        f'<div class="uf"><div class="l"><span>{uf} — {nomes[uf]}</span><span>{brl(v)}</span></div>'
        f'<div class="t"><i style="width:{round(v / maximo * 100)}%"></i></div></div>'
        for uf, v in estados
    )
    return f'<div class="lv">{itens}</div>'


def legenda_canais(canais):
    total = sum(v for _, v in canais) or 1
    cores = [OURO_CANAL, INDIGO]
    itens = "".join(
        f'<span><i style="background:{cores[i]}"></i>{nome} ({round(v / total * 100)}%)</span>'
        for i, (nome, v) in enumerate(canais)
    )
    return f'<div class="lv"><div class="leg">{itens}</div></div>'


def tabela(df):
    if df.empty:
        return '<div class="lv"><div class="vazio">Nenhuma venda encontrada para os filtros selecionados.</div></div>'
    cab = "".join(f'<th class="{c}">{t}</th>' for t, c in [
        ("ID Pedido", ""), ("Data", ""), ("Produto Life", ""), ("Categoria", ""),
        ("Canal", ""), ("UF", ""), ("Qtd", "c"), ("Valor Total", "r")])
    linhas = ""
    for r in df.itertuples():
        d = r.data
        classe, icone = ("web", "🌐") if r.canal == "E-commerce" else ("loja", "🏬")
        linhas += (
            f'<tr><td class="id">{r.pedido}</td><td>{d[8:10]}/{d[5:7]}/{d[:4]}</td><td class="pr">{r.produto}</td>'
            f'<td><span class="pill">{r.categoria}</span></td>'
            f'<td><span class="ch {classe}">{icone} {r.canal}</span></td>'
            f'<td><b>{r.uf}</b></td><td class="c">{r.qtd}</td><td class="r pr">{brl(r.total)}</td></tr>'
        )
    return f'<div class="lv"><div class="tw"><table><thead><tr>{cab}</tr></thead><tbody>{linhas}</tbody></table></div></div>'


def rodape():
    return (
        '<div class="lv"><div class="rodape">Dashboard de Análise de Desempenho Varejo — Life by Vivara'
        '<br>Base sintética calibrada com itens e ticket médio do catálogo Vivara.</div></div>'
    )


def cartoes_lucro(r):
    return [
        _kpi("Lucro Bruto Estimado", f'<div class="val">{brl(r["lucro"])}</div>',
             f'<div class="pe">Receita {brl(r["receita"])} − custo estimado {brl(r["custo"])}</div>', "💰", "#ECFDF5", "#059669"),
        _kpi("Margem Bruta", f'<div class="val">{pct(r["margem"])}</div>',
             '<div class="pe">Lucro bruto sobre o faturamento</div>', "📊", "#FFFBEB", "#B8860B"),
        _kpi("Categoria Mais Lucrativa", f'<div class="nome">{r["lider"]}</div>',
             f'<div class="pe">Margem de <b>{pct(r["margem_lider"])}</b> nesta categoria</div>', "🏆", "#FAF5FF", "#9333EA"),
    ]


def insight(texto):
    return f'<div class="lv"><div class="insight">💡 {texto}</div></div>'


def tabela_rentabilidade(rent):
    ativo = rent[rent["receita"] > 0].sort_values("lucro", ascending=False)
    if ativo.empty:
        return '<div class="lv"><div class="vazio">Sem dados para os filtros atuais.</div></div>'
    rank_receita = rent["receita"].rank(ascending=False, method="min").astype(int)
    rank_lucro = rent["lucro"].rank(ascending=False, method="min").astype(int)
    total_lucro = ativo["lucro"].sum() or 1
    cab = "".join(f'<th class="{c}">{t}</th>' for t, c in [
        ("Categoria", ""), ("Receita", "r"), ("Custo estimado", "r"), ("Lucro bruto", "r"),
        ("Margem", ""), ("% do lucro", "r"), ("Rank receita → lucro", "c")])
    linhas = ""
    for nome, r in ativo.iterrows():
        linhas += (
            f'<tr><td class="pr">{nome}</td><td class="r">{brl(r.receita)}</td><td class="r">{brl(r.custo)}</td>'
            f'<td class="r pr">{brl(r.lucro)}</td><td><span class="mb"><i style="width:{min(r.margem, 100):.0f}%"></i></span>{pct(r.margem)}</td>'
            f'<td class="r">{pct(r.lucro / total_lucro * 100)}</td><td class="c">{rank_receita[nome]}º → {rank_lucro[nome]}º</td></tr>'
        )
    return f'<div class="lv"><div class="tw"><table><thead><tr>{cab}</tr></thead><tbody>{linhas}</tbody></table></div></div>'
