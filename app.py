import streamlit as st
import pandas as pd

# Força o layout em tela cheia para caber as tabelas de forma clara
st.set_page_config(page_title="Calculadora ABCP Pro", layout="wide")

st.title("Calculadora de Traços de Concreto - Método ABCP")
st.write("Modifique os parâmetros na barra lateral esquerda. O recálculo ocorrerá automaticamente.")

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

# Listas de opções fixas para as propriedades físicas (Incrementos de 10 em 10)
lista_mu_areia = list(range(1400, 1710, 10))
lista_me_brita = list(range(2600, 3010, 10))
lista_mu_brita = list(range(1400, 1710, 10))
lista_me_areia = list(range(2450, 2760, 10))
lista_me_cimento = list(range(2900, 3210, 10))
lista_me_aditivo = [round(x * 0.01, 2) for x in range(90, 141)]

st.sidebar.markdown("---")
st.sidebar.subheader("📐 Propriedades Físicas dos Materiais")
me_cimento = st.sidebar.selectbox("Massa Específica Cimento (kg/m³)", options=lista_me_cimento, index=2)
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
st.subheader(f"Parâmetros: fck Desejado {fck:.1f} MPa | fcj Calculado {fcj:.1f} MPa")
st.markdown("---")

def calcular_dosagem_abcp(tipo_cimento):
    if tipo_cimento == "CP II 32":
        ac = max(0.20, min(0.80, 0.68 - ((fcj - 16.6) * 0.01)))
        ca_inicial = 163.0 if dmax_escolhido == 19.0 else 148.0
    else:
        ac = 0.39
        ca_inicial = 165.0 if dmax_escolhido == 19.0 else 157.0

    cc = ca_inicial / ac
    c_adit = cc * 0.007
    
    vb = 0.69 if dmax_escolhido == 19.0 else 0.64
    cb_total = vb * mu_brita
    
    vol_cimento = cc / me_cimento
    vol_agua_inicial = ca_inicial / 1000.0
    vol_brita = cb_total / me_brita
    vol_adit = c_adit / me_aditivo
    vol_ar = 0.02
    
    vol_areia_total_seca = 1.0 - (vol_cimento + vol_agua_inicial + vol_brita + vol_adit + vol_ar)
    if vol_areia_total_seca < 0:
        vol_areia_total_seca = 0.25
        
    careia_total_seca = vol_areia_total_seca * me_areia
    
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
        "ca_a": ca_a, "ca_b": ca_b, "cb_a": cb_a, "cb_b": cb_b, "cb_c": cb_c,
        "unitario": traco_unit,
        "obra_litros": {
            "Areia A": vol_obra_areia_a, "Areia B": vol_obra_areia_b,
            "Brita A": vol_obra_brita_a, "Brita B": vol_obra_brita_b, "Brita C": vol_obra_brita_c,
            "Água": vol_obra_agua, "Aditivo": (traco_unit["Aditivo"] * 50) / me_aditivo
        }
    }

res_32 = calcular_dosagem_abcp("CP II 32")
res_40 = calcular_dosagem_abcp("CP II 40")

if erro_brita or erro_areia:
    st.error("🚨 Ajuste a barra lateral: As somas das Britas e Areias precisam dar exatamente 100% para liberar os resultados.")
else:
    st.header("Seção 1: Traço dos Materiais em Massa (kg/m³)")
    col_m32, col_m40 = st.columns(2)
    
    with col_m32:
        st.subheader("Cimento CP II-32")
        st.caption(f"Relação a/c Calculada: {res_32['ac']:.2f} | Água Efetiva: {res_32['ca']:.0f} L")
        df_32_massa = pd.DataFrame({
            "Material": ["Cimento", "Areia A", "Areia B", "Brita A", "Brita B", "Brita C", "Água", "Aditivo"],
            "Massa Corrigida (kg)": [int(round(res_32['cc'])), int(round(res_32['ca_a'])), int(round(res_32['ca_b'])), int(round(res_32['cb_a'])), int(round(res_32['cb_b'])), int(round(res_32['cb_c'])), int(round(res_32['ca'])), int(round(res_32['c_adit']))],
            "Traço Unitário": [f"1", f"{res_32['unitario']['Areia A']:.2f}", f"{res_32['unitario']['Areia B']:.2f}", f"{res_32['unitario']['Brita A']:.2f}", f"{res_32['unitario']['Brita B']:.2f}", f"{res_32['unitario']['Brita C']:.2f}", f"{res_32['unitario']['Água']:.2f}", f"{res_32['unitario']['Aditivo']:.3f}"]
        })
        st.dataframe(df_32_massa, use_container_width=True, hide_index=True)
        st.metric("Massa Total Adensada (32)", f"{int(round(res_32['peso_total']))} kg/m³")
        
    with col_m40:
        st.subheader("Cimento CP II-40")
        st.caption(f"Relação a/c Calculada: {res_40['ac']:.2f} | Água Efetiva: {res_40['ca']:.0f} L")
        df_40_massa = pd.DataFrame({
            "Material": ["Cimento", "Areia A", "Areia B", "Brita A", "Brita B", "Brita C", "Água", "Aditivo"],
            "Massa Corrigida (kg)": [int(round(res_40['cc'])), int(round(res_40['ca_a'])), int(round(res_40['ca_b'])), int(round(res_40['cb_a'])), int(round(res_40['cb_b'])), int(round(res_40['cb_c'])), int(round(res_40['ca'])), int(round(res_40['c_adit']))],
            "Traço Unitário": [f"1", f"{res_40['unitario']['Areia A']:.2f}", f"{res_40['unitario']['Areia B']:.2f}", f"{res_40['unitario']['Brita A']:.2f}", f"{res_40['unitario']['Brita B']:.2f}", f"{res_40['unitario']['Brita C']:.2f}", f"{res_40['unitario']['Água']:.2f}", f"{res_40['unitario']['Aditivo']:.3f}"]
        })
        st.dataframe(df_40_massa, use_container_width=True, hide_index=True)
        st.metric("Massa Total Adensada (40)", f"{int(round(res_40['peso_total']))} kg/m³")

    st.markdown("---")
    st.header("Seção 2: Proporções em Volume Prático (Litros para 1 Saco de 50kg)")
    
    st.subheader("Volume com Cimento CP II-32")
    df_32_vol = pd.DataFrame({
        "Material": ["Areia A (L)", "Areia B (L)", "Brita A (L)", "Brita B (L)", "Brita C (L)", "Água (L)", "Aditivo (L)"],
        "Volume Necessário": [f"{res_32['obra_litros']['Areia A']:.1f}", f"{res_32['obra_litros']['Areia B']:.1f}", f"{res_32['obra_litros']['Brita A']:.1f}", f"{res_32['obra_litros']['Brita B']:.1f}", f"{res_32['obra_litros']['Brita C']:.1f}", f"{res_32['obra_litros']['Água']:.1f}", f"{res_32['obra_litros']['Aditivo']:.3f}"]
    })
    st.dataframe(df_32_vol, use_container_width=True, hide_index=True)
    
    st.subheader("Volume com Cimento CP II-40")
    df_40_vol = pd.DataFrame({
        "Material": ["Areia A (L)", "Areia B (L)", "Brita A (L)", "Brita B (L)", "Brita C (L)", "Água (L)", "Aditivo (L)"],
        "Volume Necessário": [f"{res_40['obra_litros']['Areia A']:.1f}", f"{res_40['obra_litros']['Areia B']:.1f}", f"{res_40['obra_litros']['Brita A']:.1f}", f"{res_40['obra_litros']['Brita B']:.1f}", f"{res_40['obra_litros']['Brita C']:.1f}", f"{res_40['obra_litros']['Água']:.1f}", f"{res_40['obra_litros']['Aditivo']:.3f}"]
    })
