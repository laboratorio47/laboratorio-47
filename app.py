import streamlit as st
import pandas as pd
import os

# Configuração de tela cheia para acomodar as tabelas comparativas
st.set_page_config(page_title="Calculadora ABCP Pro", layout="wide")

# LÓGICA DA LOGO: O código verifica se a imagem existe na pasta para não dar erro
if os.path.exists("logo.png"):
    st.image("logo.png", width=150)
elif os.path.exists("logo.jpg"):
    st.image("logo.jpg", width=150)

st.title("Calculadora para Traços de Concreto      Laboratório 47")
st.write("Modifique os parâmetros na barra lateral esquerda. O recálculo ocorrerá automaticamente.")

# -----------------------------------------------------------------------------
# BANCO DE DADOS DA PLANILHA (Tabelas do método ABCP)
# -----------------------------------------------------------------------------

tabela_agua_cp32 = {
    70:  {9.5: 160.0, 12.5: 147.8, 19.0: 142.0, 25.0: 133.0},
    80:  {9.5: 165.0, 12.5: 154.8, 19.0: 149.0, 25.0: 140.0},
    90:  {9.5: 170.0, 12.5: 160.8, 19.0: 156.0, 25.0: 148.0},
    100: {9.5: 175.0, 12.5: 166.8, 19.0: 163.0, 25.0: 155.0},
    110: {9.5: 180.0, 12.5: 172.8, 19.0: 169.0, 25.0: 163.0},
    120: {9.5: 185.0, 12.5: 179.8, 19.0: 176.0, 25.0: 170.0},
    130: {9.5: 190.0, 12.5: 185.8, 19.0: 183.0, 25.0: 178.0},
    140: {9.5: 195.0, 12.5: 191.8, 19.0: 190.0, 25.0: 185.0}
}

tabela_agua_cp40 = {
    70:  {9.5: 172.0, 12.5: 158.0, 19.0: 151.0, 25.0: 142.0},
    80:  {9.5: 176.0, 12.5: 164.0, 19.0: 157.0, 25.0: 148.0},
    90:  {9.5: 177.0, 12.5: 166.0, 19.0: 160.0, 25.0: 152.0},
    100: {9.5: 180.0, 12.5: 170.0, 19.0: 165.0, 25.0: 157.0},
    110: {9.5: 184.0, 12.5: 175.0, 19.0: 170.0, 24.0: 164.0},
    120: {9.5: 187.0, 12.5: 177.0, 19.0: 172.0, 25.0: 166.0},
    130: {9.5: 190.0, 12.5: 178.0, 19.0: 174.0, 25.0: 169.0},
    140: {9.5: 194.0, 12.5: 180.0, 19.0: 177.0, 25.0: 172.0}
}

tabela_vb = {
    1.8: {9.5: 0.645, 12.5: 0.7016, 19.0: 0.77,  25.0: 0.795},
    2.0: {9.5: 0.625, 12.5: 0.682,  19.0: 0.75,  25.0: 0.775},
    2.2: {9.5: 0.605, 12.5: 0.662,  19.0: 0.73,  25.0: 0.755},
    2.4: {9.5: 0.585, 12.5: 0.642,  19.0: 0.71,  25.0: 0.735},
    2.6: {9.5: 0.565, 12.5: 0.622,  19.0: 0.69,  25.0: 0.715},
    2.8: {9.5: 0.545, 12.5: 0.602,  19.0: 0.67,  25.0: 0.695},
    3.0: {9.5: 0.525, 12.5: 0.582,  19.0: 0.65,  25.0: 0.675},
    3.2: {9.5: 0.505, 12.5: 0.562,  19.0: 0.63,  25.0: 0.655},
    3.4: {9.5: 0.485, 12.5: 0.542,  19.0: 0.61,  25.0: 0.635},
    3.6: {9.5: 0.465, 12.5: 0.522,  19.0: 0.59,  25.0: 0.615}
}

# TABELA DE BUSCA DINÂMICA (Imagem Anexa)
tabela_ac_cp32 = {
    12.0: 0.80, 12.3: 0.79, 12.7: 0.78, 13.0: 0.77, 13.3: 0.76, 13.7: 0.75, 14.0: 0.74, 14.3: 0.73, 14.7: 0.72, 15.0: 0.71,
    15.5: 0.70, 16.0: 0.69, 16.5: 0.68, 17.0: 0.67, 17.5: 0.66, 18.0: 0.65, 18.5: 0.64, 19.0: 0.63, 19.5: 0.62, 20.0: 0.61,
    20.6: 0.60, 21.1: 0.59, 21.7: 0.58, 22.2: 0.57, 22.8: 0.56, 23.3: 0.55, 23.9: 0.54, 24.4: 0.53, 25.0: 0.52, 25.8: 0.51,
    26.7: 0.50, 27.5: 0.49, 28.3: 0.48, 29.2: 0.47, 30.0: 0.46, 30.8: 0.45, 31.7: 0.44, 32.5: 0.43, 33.3: 0.42, 34.2: 0.41,
    35.0: 0.40, 35.8: 0.39, 36.7: 0.38, 37.5: 0.37, 38.3: 0.36, 39.2: 0.35, 40.0: 0.34, 40.8: 0.33, 41.7: 0.32, 42.5: 0.31,
    43.3: 0.30, 44.2: 0.29, 45.0: 0.28, 45.8: 0.27, 46.7: 0.26, 47.5: 0.25, 48.3: 0.24, 49.2: 0.23, 50.0: 0.22, 50.8: 0.21, 51.7: 0.20
}

tabela_ac_cp40 = {
    15.0: 0.80, 15.5: 0.79, 16.1: 0.78, 16.6: 0.77, 17.1: 0.76, 17.6: 0.75, 18.2: 0.74, 18.7: 0.73, 19.2: 0.72, 19.7: 0.71,
    20.3: 0.70, 20.8: 0.69, 21.4: 0.68, 22.1: 0.67, 22.7: 0.66, 23.3: 0.65, 23.9: 0.64, 24.6: 0.63, 25.2: 0.62, 25.8: 0.61,
    26.5: 0.60, 27.2: 0.59, 27.9: 0.58, 28.6: 0.57, 29.3: 0.56, 30.0: 0.55, 30.8: 0.54, 31.7: 0.53, 32.5: 0.52, 33.3: 0.51,
    34.2: 0.50, 35.0: 0.49, 36.1: 0.48, 37.1: 0.47, 38.2: 0.46, 39.2: 0.45, 40.3: 0.44, 41.6: 0.43, 42.8: 0.42, 44.1: 0.41,
    45.3: 0.40, 46.6: 0.39, 47.8: 0.38, 49.1: 0.37, 50.3: 0.36, 51.6: 0.35, 52.8: 0.34, 54.1: 0.33, 55.3: 0.32, 56.6: 0.31,
    57.8: 0.30, 59.1: 0.29, 60.3: 0.28, 61.6: 0.27, 62.1: 0.26, 64.1: 0.25, 65.3: 0.24, 66.6: 0.23, 67.8: 0.22, 69.1: 0.21, 70.3: 0.20
}
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
st.sidebar.subheader("📐 Propriedades Físicas")
mf_areia = st.sidebar.selectbox("Módulo de Finura Areia (MF)", options=[1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6], index=3)

me_cimento = st.sidebar.number_input("Massa Específica Cimento (kg/m³)", value=3100, step=10)
me_agua = 1000
ar_inc = 2.0 

me_areia = st.sidebar.number_input("M. Específica Areia (kg/m³)", value=2630, step=10)
me_brita = st.sidebar.number_input("M. Específica Brita (kg/m³)", value=2740, step=10)
mu_areia = st.sidebar.number_input("M. Unitária Areia (kg/m³)", value=1460, step=10)
mu_brita = st.sidebar.number_input("M. Unitária Brita (kg/m³)", value=1480, step=10)
me_aditivo = st.sidebar.number_input("M. Específica Aditivo (kg/m³)", value=1.10, step=0.01)

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
    st.metric(label="fck Selecionado", value=f"{fck} MPa")
with col_fcj:
    st.metric(label="fcj 28 Dias Calculado", value=f"{fcj:.1f} MPa", delta="sd = 4.0")

st.markdown("---")

def calcular_traco(tipo_cimento):
    slump_ajustado = int(round(slump_escolhido / 10.0)) * 10
    slump_ajustado = max(70, min(140, slump_ajustado))
    dmax_ajustado = float(dmax_escolhido)

    if tipo_cimento == "CP II 32":
        fcj_proximo = min(tabela_ac_cp32.keys(), key=lambda x: abs(x - fcj))
        ac = tabela_ac_cp32[fcj_proximo]
        ca_inicial = tabela_agua_cp32[slump_ajustado][dmax_ajustado]
    else:
        fcj_proximo = min(tabela_ac_cp40.keys(), key=lambda x: abs(x - fcj))
        ac = tabela_ac_cp40[fcj_proximo]
        ca_inicial = tabela_agua_cp40[slump_ajustado][dmax_ajustado]

    cc = ca_inicial / ac
    c_adit = cc * 0.007
    
    vb = tabela_vb[mf_areia][dmax_ajustado]
    cb_total = vb * mu_brita
    
    vol_cimento = cc / me_cimento
    vol_agua_inicial = ca_inicial / me_agua
    vol_brita = cb_total / me_brita
    vol_adit = c_adit / me_aditivo
    vol_ar = ar_inc / 100.0
    
    vol_areia_total_seca = 1.0 - (vol_cimento + vol_agua_inicial + vol_brita + vol_adit + vol_ar)
    if vol_areia_total_seca < 0:
        vol_areia_total_seca = 0.25 
        
    careia_total_seca = vol_areia_total_seca * me_areia
    
    # Efeito da umidade nas massas
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
        "Areia A": ca_a / cc if cc > 0 else 0, "Areia B": ca_b / cc if cc > 0 else 0,
        "Brita A": cb_a / cc if cc > 0 else 0, "Brita B": cb_b / cc if cc > 0 else 0, "Brita C": cb_c / cc if cc > 0 else 0,
        "Água": ca_ajustada / cc if cc > 0 else 0, "Aditivo": c_adit / cc if cc > 0 else 0
    }
    
    fator_inchamento = 1.0 + (inchamento_areia / 100.0)
    
    vol_obra_areia_a = ((traco_unit["Areia A"] * 50) * fator_inchamento) / (mu_areia / 1000) if ca_a > 0 else 0
    vol_obra_areia_b = ((traco_unit["Areia B"] * 50) * fator_inchamento) / (mu_areia / 1000) if ca_b > 0 else 0
    vol_obra_brita_a = ((traco_unit["Brita A"] * 50)) / (mu_brita / 1000) if cb_a > 0 else 0
    vol_obra_brita_b = ((traco_unit["Brita B"] * 50)) / (mu_brita / 1000) if cb_b > 0 else 0
    vol_obra_brita_c = ((traco_unit["Brita C"] * 50)) / (mu_brita / 1000) if cb_c > 0 else 0
    vol_obra_agua = max(0.0, (traco_unit["Água"] * 50))

    return {
        "ca": ca_ajustada, "ac": ac, "cc": cc, "c_adit": c_adit, "cb_total": cb_total,
        "cb_a": cb_a, "cb_b": cb_b, "cb_c": cb_c, "ca_a": ca_a, "ca_b": ca_b, "peso_total": peso_total, "fcj_proximo": fcj_proximo,
        "unitario": traco_unit,
        "obra_50kg_litros": {
            "Areia A": vol_obra_areia_a, "Areia B": vol_obra_areia_b,
            "Brita A": vol_obra_brita_a, "Brita B": vol_obra_brita_b, "Brita C": vol_obra_brita_c,
            "Água": vol_obra_agua, "Aditivo": (traco_unit["Aditivo"] * 50) / me_aditivo
        }
    }

res_32 = calcular_traco("CP II 32")
res_40 = calcular_traco("CP II 40")

if erro_brita or erro_areia:
    st.error("🚨 Ajuste a barra lateral: As somas de britas e areias precisam dar exatamente 100% para destravar as tabelas.")
else:
    st.header("Seção 1: Traço dos Materiais em Massa (kg/m³)")
    col_m32, col_m40 = st.columns(2)
    
    with col_m32:
        st.subheader("Cimento CP II-32")
        st.caption(f"fcj Encontrado: {res_32['fcj_proximo']} MPa | Relação a/c Tabela: {res_32['ac']:.2f}")
        df_32_massa = pd.DataFrame({
            "Material": ["Cimento", "Areia A", "Areia B", "Brita A", "Brita B", "Brita C", "Água", "Aditivo"],
            "Massa Corrigida (kg)": [res_32['cc'], res_32['ca_a'], res_32['ca_b'], res_32['cb_a'], res_32['cb_b'], res_32['cb_c'], res_32['ca'], res_32['c_adit']],
            "Traço Unitário": [res_32['unitario']['Cimento'], res_32['unitario']['Areia A'], res_32['unitario']['Areia B'], res_32['unitario']['Brita A'], res_32['unitario']['Brita B'], res_32['unitario']['Brita C'], res_32['unitario']['Água'], res_32['unitario']['Aditivo']]
        })
        st.dataframe(df_32_massa.round(2), use_container_width=True, hide_index=True)
        st.metric("Massa Total Adensada (32)", f"{res_32['peso_total']:.2f} kg/m³")
        
    with col_m40:
        st.subheader("Cimento CP II-40")
        st.caption(f"fcj Encontrado: {res_40['fcj_proximo']} MPa | Relação a/c Tabela: {res_40['ac']:.2f}")
        df_40_massa = pd.DataFrame({
            "Material": ["Cimento", "Areia A", "Areia B", "Brita A", "Brita B", "Brita C", "Água", "Aditivo"],
            "Massa Corrigida (kg)": [res_40['cc'], res_40['ca_a'], res_40['ca_b'], res_40['cb_a'], res_40['cb_b'], res_40['cb_c'], res_40['ca'], res_40['c_adit']],
            "Traço Unitário": [res_40['unitario']['Cimento'], res_40['unitario']['Areia A'], res_40['unitario']['Areia B'], res_40['unitario']['Brita A'], res_40['unitario']['Brita B'], res_40['unitario']['Brita C'], res_40['unitario']['Água'], res_40['unitario']['Aditivo']]
        })
        st.dataframe(df_40_massa.round(2), use_container_width=True, hide_index=True)
        st.metric("Massa Total Adensada (40)", f"{res_40['peso_total']:.2f} kg/m³")

    st.markdown("---")
    st.header("Seção 2: Volume (litros) para Betoneira na Obra (para 1 Saco de 50kg)")
    col_v32, col_v40 = st.columns(2)
    
    with col_v32:
        st.subheader("Volume com CP II-32")
        df_32_vol = pd.DataFrame({
            "Material": ["Areia A (L)", "Areia B (L)", "Brita A (L)", "Brita B (L)", "Brita C (L)", "Água (L)", "Aditivo (L)"],
            "Volume Necessário": [res_32['obra_50kg_litros']['Areia A'], res_32['obra_50kg_litros']['Areia B'], res_32['obra_50kg_litros']['Brita A'], res_32['obra_50kg_litros']['Brita B'], res_32['obra_50kg_litros']['Brita C'], res_32['obra_50kg_litros']['Água'], res_32['obra_50kg_litros']['Aditivo']]
        })
        st.dataframe(df_32_vol.round(1), use_container_width=True, hide_index=True)
        
    with col_v40:
        st.subheader("Volume com CP II-40")
        df_40_vol = pd.DataFrame({
            "Material": ["Areia A (L)", "Areia B (L)", "Brita A (L)", "Brita B (L)", "Brita C (L)", "Água (L)", "Aditivo (L)"],
            "Volume Necessário": [res_40['obra_50kg_litros']['Areia A'], res_40['obra_50kg_litros']['Areia B'], res_40['obra_50kg_litros']['Brita A'], res_40['obra_50kg_litros']['Brita B'], res_40['obra_50kg_litros']['Brita C'], res_40['obra_50kg_litros']['Água'], res_40['obra_50kg_litros']['Aditivo']]
        })
        st.dataframe(df_40_vol.round(1), use_container_width=True, hide_index=True)