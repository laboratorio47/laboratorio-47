import streamlit as st
import pandas as pd

# Força o layout em tela cheia para caber as tabelas lado a lado de forma clara
st.set_page_config(page_title="Calculadora ABCP Pro", layout="wide")

st.title("Calculadora de Traços de Concreto - Método ABCP")
st.write("Modifique os parâmetros na barra lateral esquerda. O recálculo ocorrerá automaticamente.")

# -----------------------------------------------------------------------------
# BANCO DE DADOS DE ENGENHARIA (Valores reais e fixos da sua planilha)
# Parâmetros Técnicos Fixados nos bastidores: Módulo de Finura = 2.6 | Ar Incorporado = 2%
# -----------------------------------------------------------------------------

# Matriz organizada de dados para busca exata de laboratório
dados_cp32 = [
    # Cada linha representa um cruzamento exato cadastrado
    {"fcj": 16.6, "ac": 0.68, "slump": 70, "dmax": 9.5, "agua": 160, "cimento": 235, "brita": 893, "areia": 1103, "argamassa": 59.98},
    {"fcj": 16.6, "ac": 0.68, "slump": 80, "dmax": 9.5, "agua": 165, "cimento": 243, "brita": 887, "areia": 1089, "argamassa": 60.03},
    {"fcj": 16.6, "ac": 0.68, "slump": 90, "dmax": 9.5, "agua": 170, "cimento": 250, "brita": 883, "areia": 1074, "argamassa": 59.99},
    {"fcj": 16.6, "ac": 0.68, "slump": 100, "dmax": 9.5, "agua": 175, "cimento": 257, "brita": 878, "areia": 1060, "argamassa": 60.00},
    {"fcj": 16.6, "ac": 0.68, "slump": 110, "dmax": 9.5, "agua": 180, "cimento": 265, "brita": 873, "areia": 1045, "argamassa": 60.01},
    {"fcj": 16.6, "ac": 0.68, "slump": 120, "dmax": 9.5, "agua": 185, "cimento": 272, "brita": 868, "areia": 1030, "argamassa": 60.01},
    {"fcj": 16.6, "ac": 0.68, "slump": 130, "dmax": 9.5, "agua": 190, "cimento": 279, "brita": 863, "areia": 1016, "argamassa": 60.02},
    {"fcj": 16.6, "ac": 0.68, "slump": 140, "dmax": 9.5, "agua": 195, "cimento": 287, "brita": 858, "areia": 1001, "argamassa": 60.02},
    {"fcj": 16.6, "ac": 0.68, "slump": 70, "dmax": 12.5, "agua": 148, "cimento": 217, "brita": 905, "areia": 1139, "argamassa": 59.97},
    {"fcj": 16.6, "ac": 0.68, "slump": 80, "dmax": 12.5, "agua": 155, "cimento": 228, "brita": 898, "areia": 1118, "argamassa": 59.97},
    {"fcj": 16.6, "ac": 0.68, "slump": 90, "dmax": 12.5, "agua": 161, "cimento": 236, "brita": 891, "areia": 1101, "argamassa": 60.02},
    {"fcj": 16.6, "ac": 0.68, "slump": 100, "dmax": 12.5, "agua": 167, "cimento": 245, "brita": 886, "areia": 1083, "argamassa": 59.98},
    {"fcj": 16.6, "ac": 0.68, "slump": 110, "dmax": 12.5, "agua": 173, "cimento": 254, "brita": 879, "areia": 1066, "argamassa": 60.03},
    {"fcj": 16.6, "ac": 0.68, "slump": 120, "dmax": 12.5, "agua": 180, "cimento": 264, "brita": 872, "areia": 1046, "argamassa": 60.04},
    {"fcj": 16.6, "ac": 0.68, "slump": 130, "dmax": 12.5, "agua": 186, "cimento": 273, "brita": 866, "areia": 1028, "argamassa": 60.04},
    {"fcj": 16.6, "ac": 0.68, "slump": 140, "dmax": 12.5, "agua": 192, "cimento": 282, "brita": 862, "areia": 1009, "argamassa": 59.96},
    {"fcj": 16.6, "ac": 0.68, "slump": 70, "dmax": 19.0, "agua": 142, "cimento": 209, "brita": 910, "areia": 1156, "argamassa": 60.01},
    {"fcj": 16.6, "ac": 0.68, "slump": 80, "dmax": 19.0, "agua": 149, "cimento": 219, "brita": 904, "areia": 1135, "argamassa": 59.97},
    {"fcj": 16.6, "ac": 0.68, "slump": 90, "dmax": 19.0, "agua": 156, "cimento": 229, "brita": 896, "areia": 1116, "argamassa": 60.02},
    {"fcj": 16.6, "ac": 0.68, "slump": 100, "dmax": 19.0, "agua": 163, "cimento": 240, "brita": 889, "areia": 1094, "argamassa": 60.01},
    {"fcj": 16.6, "ac": 0.68, "slump": 110, "dmax": 19.0, "agua": 169, "cimento": 249, "brita": 884, "areia": 1076, "argamassa": 59.98},
    {"fcj": 16.6, "ac": 0.68, "slump": 120, "dmax": 19.0, "agua": 176, "cimento": 259, "brita": 877, "areia": 1056, "argamassa": 59.99},
    {"fcj": 16.6, "ac": 0.68, "slump": 130, "dmax": 19.0, "agua": 183, "cimento": 269, "brita": 870, "areia": 1035, "argamassa": 60.00},
    {"fcj": 16.6, "ac": 0.68, "slump": 140, "dmax": 19.0, "agua": 190, "cimento": 279, "brita": 863, "areia": 1015, "argamassa": 60.00},
    {"fcj": 16.6, "ac": 0.68, "slump": 70, "dmax": 25.0, "agua": 133, "cimento": 196, "brita": 920, "areia": 1181, "argamassa": 59.95},
    {"fcj": 16.6, "ac": 0.68, "slump": 80, "dmax": 25.0, "agua": 140, "cimento": 206, "brita": 912, "areia": 1162, "argamassa": 60.00},
    {"fcj": 16.6, "ac": 0.68, "slump": 90, "dmax": 25.0, "agua": 148, "cimento": 218, "brita": 904, "areia": 1138, "argamassa": 60.01},
    {"fcj": 16.6, "ac": 0.68, "slump": 100, "dmax": 25.0, "agua": 155, "cimento": 228, "brita": 898, "areia": 1117, "argamassa": 59.97},
    {"fcj": 16.6, "ac": 0.68, "slump": 110, "dmax": 25.0, "agua": 163, "cimento": 240, "brita": 890, "areia": 1093, "argamassa": 59.98},
    {"fcj": 16.6, "ac": 0.68, "slump": 120, "dmax": 25.0, "agua": 170, "cimento": 250, "brita": 882, "areia": 1074, "argamassa": 60.03},
    {"fcj": 16.6, "ac": 0.68, "slump": 130, "dmax": 25.0, "agua": 178, "cimento": 262, "brita": 874, "areia": 1051, "argamassa": 60.03},
    {"fcj": 16.6, "ac": 0.68, "slump": 140, "dmax": 25.0, "agua": 185, "cimento": 272, "brita": 868, "areia": 1029, "argamassa": 59.99}
]

# Definição das listas fechadas das fotos regulamentares do laboratório
lista_mu_areia = list(range(1400, 1710, 10))
lista_me_brita = list(range(2600, 3010, 10))
lista_mu_brita = list(range(1400, 1710, 10))
lista_me_areia = list(range(2450, 2760, 10))
lista_me_cimento = list(range(2900, 3210, 10))
lista_me_aditivo = [round(x * 0.01, 2) for x in range(90, 141)]

# -----------------------------------------------------------------------------
# CONTROLES DA BARRA LATERAL (ENTRADAS DO USUÁRIO)
# -----------------------------------------------------------------------------
st.sidebar.header("📥 Parâmetros Gerais")
fck = st.sidebar.number_input("fck Desejado (MPa)", min_value=10.0, max_value=50.0, value=40.0, step=5.0)
sd = 4.0
fcj = fck + 1.65 * sd

st.sidebar.markdown("---")
st.sidebar.subheader("💧 Consumo de Água (Slump)")
slump_escolhido = st.sidebar.number_input("Abatimento / Slump (mm)", min_value=70, max_value=140, value=100, step=10)
dmax_escolhido = st.sidebar.selectbox("Diâmetro Máximo Brita Dmáx (mm)", options=[9.5, 12.5, 19.0, 25.0], index=2)

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Seleção do Teor de Argamassa")
teor_argamassa_escolhido = st.sidebar.slider("Teor de Argamassa desejado (%)", min_value=45, max_value=65, value=53, step=1)

st.sidebar.markdown("---")
st.sidebar.subheader("📐 Propriedades Físicas dos Materiais")
me_cimento = st.sidebar.selectbox("Massa Específica Cimento (kg/m³)", options=lista_me_cimento, index=20)
me_areia = st.sidebar.selectbox("Massa Específica Areia (kg/m³)", options=lista_me_areia, index=18)
me_brita = st.sidebar.selectbox("Massa Específica Brita (kg/m³)", options=lista_me_brita, index=14)
mu_areia = st.sidebar.selectbox("Massa Unitária Areia (kg/m³)", options=lista_mu_areia, index=6)
mu_brita = st.sidebar.selectbox("Massa Unitária Brita (kg/m³)", options=lista_mu_brita, index=8)
me_aditivo = st.sidebar.selectbox("Massa Específica Aditivo (kg/m³)", options=lista_me_aditivo, index=20)

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
umidade_areia = st.sidebar.number_input("Umidade da Areia (%)", value=0.0, step=0.5)
inchamento_areia = st.sidebar.number_input("Inchamento da Areia (%)", value=0.0, step=0.5)

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
    # Lógica limpa e estruturada sem perigo de cortes automáticos do chat
    fcj_proximo = min([row["fcj"] for row in dados_cp32], key=lambda x: abs(x - fcj))
    
    slump_ajustado = int(round(slump_escolhido / 10.0)) * 10
    slump_ajustado = max(70, min(140, slump_ajustado))
    dmax_ajustado = float(dmax_escolhido)

    linha_encontrada = None
    for row in dados_cp32:
        if row["fcj"] == fcj_proximo and row["slump"] == slump_ajustado and row["dmax"] == dmax_ajustado:
            linha_encontrada = row
            break
            
    if linha_encontrada is None:
        linha_encontrada = dados_cp32[0]

    ac = linha_encontrada["ac"]
    ca_inicial = linha_encontrada["agua"]
    
    if tipo_cimento == "CP II 40":
        ac = 0.39
        
    cc = ca_inicial / ac
    c_adit = cc * 0.007
    
    cb_total = linha_encontrada["brita"]
    careia_total_seca = linha_encontrada["areia"]
    
    # Correção física da Umidade: soma o peso da água no agregado e desconta dos litros limpos
    agua_na_areia = careia_total_seca * (umidade_areia / 100.0)
    careia_total_umida = careia_total_seca + agua_na_areia
    ca_ajustada = max(0.0, ca_inicial - agua_na_areia)
    
    cb_a = cb_total * (p_brita_a / 100.0)
    cb_b = cb_total * (p_brita_b / 100.0)
    cb_c = cb_total * (p_brita_c / 100.0)
    
    ca_a = careia_total_umida * (p_areia_a / 100.0)
    ca_b = careia_total_umida * (p_areia_b / 100.0)
    
    peso_total = cc + careia_total_umida + cb_total + ca_ajustada + c_adit
    
    traco_unit = {
        "Cimento": 1.0,
        "Areia A": ca_a / cc if cc > 0 else 0,
        "Areia B": ca_b / cc if cc > 0 else 0,
