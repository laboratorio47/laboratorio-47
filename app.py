import streamlit as st
import pandas as pd

# Força o layout em tela cheia para caber as tabelas lado a lado de forma clara
st.set_page_config(page_title="Calculadora ABCP Pro", layout="wide")

st.title("Calculadora de Traços de Concreto - Método ABCP")
st.write("Modifique os parâmetros na barra lateral esquerda. O recálculo ocorrerá automaticamente.")

# -----------------------------------------------------------------------------
# BANCO DE DADOS DE ENGENHARIA (Mapeamento das tabelas enviadas pelo cliente)
# Parâmetros Técnicos Fixados: Módulo de Finura = 2.6 | Ar Incorporado = 2%
# -----------------------------------------------------------------------------

# Matriz de Dados Técnicos para o Cimento CP II-32
dados_cp32 = [
    # [fcj, a/c, slump, dmax, agua, cimento, brita, areia, teor_argamassa, mu_areia, me_brita, mu_brita, me_areia, me_cimento]
    [16.6, 0.68, 70, 9.5, 160, 235, 893, 1103, 59.98, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 80, 9.5, 165, 243, 887, 1089, 60.03, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 90, 9.5, 170, 250, 883, 1074, 59.99, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 100, 9.5, 175, 257, 878, 1060, 60.00, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 110, 9.5, 180, 265, 873, 1045, 60.01, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 120, 9.5, 185, 272, 868, 1030, 60.01, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 130, 9.5, 190, 279, 863, 1016, 60.02, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 140, 9.5, 195, 287, 858, 1001, 60.02, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 70, 12.5, 148, 217, 905, 1139, 59.97, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 80, 12.5, 155, 228, 898, 1118, 59.97, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 90, 12.5, 161, 236, 891, 1102, 60.02, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 100, 12.5, 167, 245, 886, 1083, 59.98, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 110, 12.5, 173, 254, 879, 1066, 60.03, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 120, 12.5, 180, 264, 872, 1046, 60.04, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 130, 12.5, 186, 273, 866, 1028, 60.04, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 140, 12.5, 192, 282, 862, 1009, 59.96, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 70, 19.0, 142, 209, 910, 1156, 60.01, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 80, 19.0, 149, 219, 904, 1135, 59.97, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 90, 19.0, 156, 229, 896, 1116, 60.02, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 100, 19.0, 163, 240, 889, 1095, 60.01, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 110, 19.0, 169, 249, 884, 1076, 59.99, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 120, 19.0, 176, 259, 877, 1056, 59.99, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 130, 19.0, 183, 269, 870, 1036, 60.00, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 140, 19.0, 190, 279, 863, 1016, 60.00, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 70, 25.0, 133, 196, 920, 1181, 59.96, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 80, 25.0, 140, 206, 912, 1162, 60.00, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 90, 25.0, 148, 218, 904, 1139, 60.01, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 100, 25.0, 155, 228, 898, 1118, 59.97, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 110, 25.0, 163, 240, 890, 1094, 59.98, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 120, 25.0, 170, 250, 882, 1075, 60.03, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 130, 25.0, 178, 262, 874, 1051, 60.04, 1650, 2750, 1750, 2630, 3100],
    [16.6, 0.68, 140, 25.0, 185, 272, 868, 1030, 60.00, 1650, 2750, 1750, 2630, 3100]
]

# -----------------------------------------------------------------------------
# DEFINIÇÃO DAS LISTAS DE OPÇÕES DA PLANILHA (Menus de Escolha de Massas)
# -----------------------------------------------------------------------------
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
    fcj_proximo = min([row[0] for row in dados_cp32], key=lambda x: abs(x - fcj))
    
    slump_ajustado = int(round(slump_escolhido / 10.0)) * 10
    slump_ajustado = max(70, min(140, slump_ajustado))
    dmax_ajustado = float(dmax_escolhido)

    linha_encontrada = None
    for row in dados_cp32:
        if row[0] == fcj_proximo and row[2] == slump_ajustado and row[3] == dmax_ajustado:
            linha_encontrada = row
            break
            
    if linha_encontrada is None:
        linha_encontrada = dados_cp32[0]

    ac = linha_encontrada[1]
    ca_inicial = linha_encontrada[4]
    
    if tipo_cimento == "CP II 40":
        ac = 0.39
        
    cc = ca_inicial / ac
    c_adit = cc * 0.007
    
    cb_total = linha_encontrada[6]
    careia_total_seca = linha_encontrada[7]
    
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
        "Brita A": cb_a / cc if cc > 0 else 0,
        "Brita B": cb_b / cc if cc > 0 else 0,
        "Brita C": cb_c / cc if cc > 0 else 0,
        "Água": ca_ajustada / cc if cc > 0 else 0,
        "Aditivo": c_adit / cc if cc > 0 else 0
    }
    
    fator_inchamento = 1.0 + (inchamento_areia / 100.0)
    
    vol_obra_areia_a = ((traco_unit["Areia A"] * 50) * fator_inchamento) / (mu_areia / 1000) if ca_a > 0 else 0
    vol_obra_areia_b = ((traco_unit["Areia B"] * 50) * fator_inchamento) / (mu_areia / 1000) if ca_b > 0 else 0
    vol_obra_brita_a = ((traco_unit["Brita A"] * 50)) / (mu_brita / 1000) if cb_a > 0 else 0
    vol_obra_brita_b = ((traco_unit["Brita B"] * 50)) / (mu_brita / 1000) if cb_b > 0 else 0
    vol_obra_brita_c = ((traco_unit["Brita C"] * 50)) / (mu_brita / 1000) if cb_c > 0 else 0
    vol_obra_agua = max(0.0, (traco_unit["Água"] * 50))

    return {
        "ac": ac, "ca": ca_ajustada, "cc": cc, "c_adit": c_adit, "peso_total": peso_total,
        "ca_a": ca_a, "ca_b": ca_b, "cb_a": cb_a, "cb_b": cb_b, "cb_c": cb_c, "fcj_proximo": fcj_proximo,
        "unitario": traco_unit,
        "obra_litros": {
            "Areia A": vol_obra_areia_a, "Areia B": vol_obra_areia_b,
            "Brita A": vol_obra_brita_a, "Brita B": vol_obra_brita_b, "Brita C": vol_obra_brita_c,
            "Água": vol_obra_agua, "Aditivo": (traco_unit["Aditivo"] * 50) / me_aditivo
        }
    }

res_32 = buscar_e_calcular_traco("CP II 32")
res_40 = buscar_e_calcular_traco("CP II 40")

if erro_brita or erro_areia:
