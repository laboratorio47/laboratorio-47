import streamlit as st
import pandas as pd
import os

# -----------------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Elaborador para traços de concreto - Laboratorio 47", layout="wide")

col_logo, col_titulo = st.columns([1, 5])
with col_logo:
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=140)
with col_titulo:
    st.title("Elaborador para traços de concreto - Laboratorio 47")
    st.write("Modifique os parâmetros na barra lateral esquerda. O recálculo ocorrerá automaticamente.")

# -----------------------------------------------------------------------------
# CARREGAMENTO DOS DADOS (arquivos gerados a partir de "tabelas completas.xlsx")
# -----------------------------------------------------------------------------
@st.cache_data
def carregar_dados():
    tracos = pd.read_csv("dados_tracos.csv")
    massas = pd.read_csv("massas.csv")
    umidade_inchamento = pd.read_csv("umidade_inchamento.csv")
    sacos = pd.read_csv("sacos_cimento.csv")
    # O teor de argamassa deve ser sempre tratado como número inteiro
    tracos["teor_argamassa"] = tracos["teor_argamassa"].round(0).astype(int)
    return tracos, massas, umidade_inchamento, sacos

df_tracos, df_massas, df_umid, df_sacos = carregar_dados()

lista_mu_areia = df_massas["mu_areia"].dropna().tolist()
lista_me_brita = df_massas["me_brita"].dropna().tolist()
lista_mu_brita = df_massas["mu_brita"].dropna().tolist()
lista_me_areia = df_massas["me_areia"].dropna().tolist()
lista_me_cimento = df_massas["me_cimento"].dropna().tolist()
lista_umidade = df_umid["umidade"].dropna().tolist()
lista_inchamento = df_umid["inchamento"].dropna().tolist()
lista_sacos = df_sacos["sacos"].dropna().astype(int).tolist()
lista_dmax = sorted(df_tracos["dmax"].unique().tolist())
lista_teor_argamassa = sorted(df_tracos["teor_argamassa"].unique().tolist())

lista_me_aditivo = [round(x * 0.01, 2) for x in range(90, 141)]  # sem tabela própria enviada

def indice_mais_proximo(lista, valor):
    return min(range(len(lista)), key=lambda i: abs(lista[i] - valor))

FCK_MIN = float(round(df_tracos["fck"].min()))
FCK_MAX = float(round(df_tracos["fck"].max()))

# -----------------------------------------------------------------------------
# CONTROLES DA BARRA LATERAL (ENTRADAS DO USUÁRIO)
# -----------------------------------------------------------------------------
st.sidebar.header("📥 Parâmetros Gerais")
fck = st.sidebar.number_input(
    "fck Desejado (MPa)", min_value=FCK_MIN, max_value=FCK_MAX, value=FCK_MIN + 10.0, step=5.0
)
sd = 4.0
fcj = fck + 1.65 * sd

st.sidebar.markdown("---")
st.sidebar.subheader("💧 Consumo de Água (Slump)")
slump_escolhido = st.sidebar.number_input("Abatimento / Slump (mm)", min_value=70, max_value=140, value=100, step=10)
dmax_escolhido = st.sidebar.selectbox("Diâmetro Máximo Brita Dmáx (mm)", options=lista_dmax, index=min(2, len(lista_dmax) - 1))

st.sidebar.markdown("---")
st.sidebar.subheader("🧱 Teor de Argamassa")
teor_escolhido = st.sidebar.selectbox(
    "Teor de Argamassa (%)",
    options=lista_teor_argamassa,
    index=len(lista_teor_argamassa) - 1,
    help="Define a proporção de argamassa usada na busca do traço. Valores sempre inteiros (45% a 60%).",
)

st.sidebar.markdown("---")
st.sidebar.subheader("📐 Propriedades Físicas dos Materiais")
me_cimento_sel = st.sidebar.selectbox(
    "Massa Específica Cimento (kg/m³)", options=lista_me_cimento,
    index=indice_mais_proximo(lista_me_cimento, 3100)
)
me_areia_sel = st.sidebar.selectbox(
    "Massa Específica Areia (kg/m³)", options=lista_me_areia,
    index=indice_mais_proximo(lista_me_areia, 2630)
)
me_brita_sel = st.sidebar.selectbox(
    "Massa Específica Brita (kg/m³)", options=lista_me_brita,
    index=indice_mais_proximo(lista_me_brita, 2750)
)
mu_areia_sel = st.sidebar.selectbox(
    "Massa Unitária Areia (kg/m³)", options=lista_mu_areia,
    index=indice_mais_proximo(lista_mu_areia, 1650)
)
mu_brita_sel = st.sidebar.selectbox(
    "Massa Unitária Brita (kg/m³)", options=lista_mu_brita,
    index=indice_mais_proximo(lista_mu_brita, 1700)
)
me_aditivo_sel = st.sidebar.selectbox("Massa Específica Aditivo (kg/m³)", options=lista_me_aditivo, index=20)

st.sidebar.markdown("---")
st.sidebar.subheader("🪨 Divisão dos Agregados (%)")
p_brita_a = st.sidebar.slider("% Brita A", 0, 100, 100)
p_brita_b = st.sidebar.slider("% Brita B", 0, 100, 0)
p_brita_c = st.sidebar.slider("% Brita C", 0, 100, 0)
p_areia_a = st.sidebar.slider("% Areia A", 0, 100, 100)
p_areia_b = st.sidebar.slider("% Areia B", 0, 100, 0)

erro_brita = (p_brita_a + p_brita_b + p_brita_c) != 100
erro_areia = (p_areia_a + p_areia_b) != 100

st.sidebar.markdown("---")
st.sidebar.subheader("🪣 Parâmetros de Obra")
umidade_areia = st.sidebar.selectbox("Umidade da Areia (%)", options=lista_umidade, index=0)
inchamento_areia = st.sidebar.selectbox("Inchamento da Areia (%)", options=lista_inchamento, index=0)
qtd_sacos = st.sidebar.selectbox("Quantidade de Sacos de Cimento (50kg)", options=lista_sacos, index=0)

# -----------------------------------------------------------------------------
# PAINEL CENTRAL DE RESULTADOS
# -----------------------------------------------------------------------------
col_fck, col_fcj = st.columns(2)
with col_fck:
    st.metric(label="fck Selecionado", value=f"{fck:.1f} MPa")
with col_fcj:
    st.metric(label="fcj 28 Dias Calculado", value=f"{fcj:.1f} MPa", delta="sd = 4.0")

st.markdown("---")


def buscar_e_calcular_traco(tipo_cimento):
    dados_cimento = df_tracos[df_tracos["cimento"] == tipo_cimento]

    # Procura o fcj mais próximo dentro do banco de dados fornecido
    fcj_proximo = min(dados_cimento["fcj"].unique().tolist(), key=lambda x: abs(x - fcj))
    slump_ajustado = int(round(slump_escolhido / 10.0)) * 10
    slump_ajustado = max(70, min(140, slump_ajustado))
    dmax_ajustado = float(dmax_escolhido)

    linha = dados_cimento[
        (abs(dados_cimento["fcj"] - fcj_proximo) < 0.1)
        & (dados_cimento["slump"] == slump_ajustado)
        & (dados_cimento["dmax"] == dmax_ajustado)
        & (dados_cimento["teor_argamassa"] == int(teor_escolhido))
    ]

    if linha.empty:
        linha = dados_cimento[
            (abs(dados_cimento["fcj"] - fcj_proximo) < 0.1)
            & (dados_cimento["slump"] == slump_ajustado)
            & (dados_cimento["dmax"] == dmax_ajustado)
        ]
    if linha.empty:
        linha = dados_cimento.iloc[[0]]
    linha = linha.iloc[0]

    # Dados exatos da tabela cruzada (já corretos por fcj e por tipo de cimento)
    ac = linha["ac"]
    cc = linha["consumo_cimento"]
    ca_inicial = linha["agua"]
    c_adit = cc * 0.007

    brita_total_seca = linha["consumo_brita"]
    areia_total_seca = linha["consumo_areia"]
    teor_argamassa_tabela = int(round(linha["teor_argamassa"]))

    # Ajuste de Umidade na Massa da Areia e Desconto na Água Efetiva
    agua_na_areia = areia_total_seca * (umidade_areia / 100.0)
    areia_total_umida = areia_total_seca + agua_na_areia
    ca_ajustada = max(0.0, ca_inicial - agua_na_areia)

    cb_a = brita_total_seca * (p_brita_a / 100.0)
    cb_b = brita_total_seca * (p_brita_b / 100.0)
    cb_c = brita_total_seca * (p_brita_c / 100.0)

    ca_a = areia_total_umida * (p_areia_a / 100.0)
    ca_b = areia_total_umida * (p_areia_b / 100.0)

    peso_total = cc + areia_total_umida + brita_total_seca + ca_ajustada + c_adit

    traco_unit = {
        "Cimento": 1.0,
        "Areia A": ca_a / cc if cc > 0 else 0,
        "Areia B": ca_b / cc if cc > 0 else 0,
        "Brita A": cb_a / cc if cc > 0 else 0,
        "Brita B": cb_b / cc if cc > 0 else 0,
        "Brita C": cb_c / cc if cc > 0 else 0,
        "Água": ca_ajustada / cc if cc > 0 else 0,
        "Aditivo": c_adit / cc if cc > 0 else 0,
    }

    fator_inchamento = 1.0 + (inchamento_areia / 100.0)
    massa_saco = 50 * qtd_sacos  # kg de cimento totais a partir da qtde de sacos escolhida

    vol_areia_a = ((traco_unit["Areia A"] * massa_saco) * fator_inchamento) / (mu_areia_sel / 1000) if ca_a > 0 else 0
    vol_areia_b = ((traco_unit["Areia B"] * massa_saco) * fator_inchamento) / (mu_areia_sel / 1000) if ca_b > 0 else 0
    vol_brita_a = (traco_unit["Brita A"] * massa_saco) / (mu_brita_sel / 1000) if cb_a > 0 else 0
    vol_brita_b = (traco_unit["Brita B"] * massa_saco) / (mu_brita_sel / 1000) if cb_b > 0 else 0
    vol_brita_c = (traco_unit["Brita C"] * massa_saco) / (mu_brita_sel / 1000) if cb_c > 0 else 0
    vol_agua = max(0.0, traco_unit["Água"] * massa_saco)
    vol_aditivo = (traco_unit["Aditivo"] * massa_saco) / me_aditivo_sel

    return {
        "ac": ac, "ca": ca_ajustada, "cc": cc, "c_adit": c_adit, "peso_total": peso_total,
        "ca_a": ca_a, "ca_b": ca_b, "cb_a": cb_a, "cb_b": cb_b, "cb_c": cb_c, "fcj_proximo": fcj_proximo,
        "teor_argamassa": teor_argamassa_tabela,
        "unitario": traco_unit,
        "obra_litros": {
            "Areia A": vol_areia_a, "Areia B": vol_areia_b,
            "Brita A": vol_brita_a, "Brita B": vol_brita_b, "Brita C": vol_brita_c,
            "Água": vol_agua, "Aditivo": vol_aditivo,
        },
    }


res_32 = buscar_e_calcular_traco("CP II 32")
res_40 = buscar_e_calcular_traco("CP II 40")

if erro_brita or erro_areia:
    st.error("🚨 Ajuste a barra lateral: As somas das Britas e Areias precisam dar exatamente 100% para liberar os resultados.")
else:
    st.header("Seção 1: Traço dos Materiais em Massa (kg/m³)")
    col_m32, col_m40 = st.columns(2)

    with col_m32:
        st.subheader("Cimento CP II-32")
        st.caption(f"fcj Buscado: {res_32['fcj_proximo']:.1f} MPa | Relação a/c: {res_32['ac']:.2f}")
        df_32_massa = pd.DataFrame({
            "Material": ["Cimento", "Areia A", "Areia B", "Brita A", "Brita B", "Brita C", "Água", "Aditivo"],
            "Massa Corrigida (kg)": [int(round(res_32['cc'])), int(round(res_32['ca_a'])), int(round(res_32['ca_b'])), int(round(res_32['cb_a'])), int(round(res_32['cb_b'])), int(round(res_32['cb_c'])), int(round(res_32['ca'])), int(round(res_32['c_adit']))],
            "Traço Unitário": [f"1", f"{res_32['unitario']['Areia A']:.2f}", f"{res_32['unitario']['Areia B']:.2f}", f"{res_32['unitario']['Brita A']:.2f}", f"{res_32['unitario']['Brita B']:.2f}", f"{res_32['unitario']['Brita C']:.2f}", f"{res_32['unitario']['Água']:.2f}", f"{res_32['unitario']['Aditivo']:.3f}"],
        })
        st.dataframe(df_32_massa, use_container_width=True, hide_index=True)
        st.metric("Teor de Argamassa (tabela)", f"{res_32['teor_argamassa']}%")
        st.metric("Massa Total Adensada (32)", f"{int(round(res_32['peso_total']))} kg/m³")

    with col_m40:
        st.subheader("Cimento CP II-40")
        st.caption(f"fcj Buscado: {res_40['fcj_proximo']:.1f} MPa | Relação a/c: {res_40['ac']:.2f}")
        df_40_massa = pd.DataFrame({
            "Material": ["Cimento", "Areia A", "Areia B", "Brita A", "Brita B", "Brita C", "Água", "Aditivo"],
            "Massa Corrigida (kg)": [int(round(res_40['cc'])), int(round(res_40['ca_a'])), int(round(res_40['ca_b'])), int(round(res_40['cb_a'])), int(round(res_40['cb_b'])), int(round(res_40['cb_c'])), int(round(res_40['ca'])), int(round(res_40['c_adit']))],
            "Traço Unitário": [f"1", f"{res_40['unitario']['Areia A']:.2f}", f"{res_40['unitario']['Areia B']:.2f}", f"{res_40['unitario']['Brita A']:.2f}", f"{res_40['unitario']['Brita B']:.2f}", f"{res_40['unitario']['Brita C']:.2f}", f"{res_40['unitario']['Água']:.2f}", f"{res_40['unitario']['Aditivo']:.3f}"],
        })
        st.dataframe(df_40_massa, use_container_width=True, hide_index=True)
        st.metric("Teor de Argamassa (tabela)", f"{res_40['teor_argamassa']}%")
        st.metric("Massa Total Adensada (40)", f"{int(round(res_40['peso_total']))} kg/m³")

    st.markdown("---")
    st.header(f"Seção 2: Proporções em Volume Prático (Litros para {qtd_sacos} Saco(s) de 50kg)")

    st.subheader("Volume com Cimento CP II-32")
    df_32_vol = pd.DataFrame({
        "Material": ["Areia A (L)", "Areia B (L)", "Brita A (L)", "Brita B (L)", "Brita C (L)", "Água (L)", "Aditivo (L)"],
        "Volume Necessário": [f"{res_32['obra_litros']['Areia A']:.1f}", f"{res_32['obra_litros']['Areia B']:.1f}", f"{res_32['obra_litros']['Brita A']:.1f}", f"{res_32['obra_litros']['Brita B']:.1f}", f"{res_32['obra_litros']['Brita C']:.1f}", f"{res_32['obra_litros']['Água']:.1f}", f"{res_32['obra_litros']['Aditivo']:.3f}"],
    })
    st.dataframe(df_32_vol, use_container_width=True, hide_index=True)

    st.subheader("Volume com Cimento CP II-40")
    df_40_vol = pd.DataFrame({
        "Material": ["Areia A (L)", "Areia B (L)", "Brita A (L)", "Brita B (L)", "Brita C (L)", "Água (L)", "Aditivo (L)"],
        "Volume Necessário": [f"{res_40['obra_litros']['Areia A']:.1f}", f"{res_40['obra_litros']['Areia B']:.1f}", f"{res_40['obra_litros']['Brita A']:.1f}", f"{res_40['obra_litros']['Brita B']:.1f}", f"{res_40['obra_litros']['Brita C']:.1f}", f"{res_40['obra_litros']['Água']:.1f}", f"{res_40['obra_litros']['Aditivo']:.3f}"],
    })
    st.dataframe(df_40_vol, use_container_width=True, hide_index=True)
