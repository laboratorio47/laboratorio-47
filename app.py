import streamlit as st
import pandas as pd

# Força o layout em tela cheia para caber as tabelas de forma clara
st.set_page_config(page_title="Calculadora ABCP Pro", layout="wide")

st.title("Calculadora de Traços de Concreto - Método ABCP")
st.write("Modifique os parâmetros na barra lateral esquerda. O recálculo ocorrerá automaticamente.")

# -----------------------------------------------------------------------------
# BANCO DE DADOS DE ENGENHARIA (Valores exatos extraídos da sua nova tabela)
# Parâmetros Técnicos Fixados nos bastidores: MF = 2.6 | Ar Incorporado = 2%
# -----------------------------------------------------------------------------

dados_planilha = [
    # Formato: [fcj, a/c, slump, dmax, agua, cimento, brita, areia, teor_argamassa, mu_areia, me_brita, mu_brita, me_areia, me_cimento, me_agua]
    [16.6, 0.68, 70, 9.5, 160, 235, 893, 1103.19, 59.97, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 80, 9.5, 165, 243, 887, 1088.99, 60.02, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 90, 9.5, 170, 250, 883, 1073.73, 59.98, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 100, 9.5, 175, 257, 877.66, 1059.74, 60.00, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 110, 9.5, 180, 265, 872.66, 1044.59, 60.01, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 120, 9.5, 185, 272, 867.66, 1030.28, 60.01, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 130, 9.5, 190, 279, 862.66, 1015.97, 60.01, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 140, 9.5, 195, 287, 857.66, 1000.82, 60.02, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 70, 12.5, 148, 217, 905, 1138.55, 59.96, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 80, 12.5, 155, 228, 898, 1117.50, 59.97, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 90, 12.5, 161, 236, 891, 1101.63, 60.02, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 100, 12.5, 167, 245, 886, 1082.99, 59.98, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 110, 12.5, 173, 254, 879, 1066.27, 60.03, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 120, 12.5, 180, 264, 872, 1046.07, 60.03, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 130, 12.5, 186, 273, 866, 1028.39, 60.04, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 140, 12.5, 192, 282, 862, 1008.80, 59.95, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 70, 19.0, 142, 209, 910, 1156.33, 60.00, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 80, 19.0, 149, 219, 904, 1135.18, 59.96, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 90, 19.0, 156, 229, 896, 1115.93, 60.01, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 100, 19.0, 163, 240, 889.33, 1094.57, 60.01, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 110, 19.0, 169, 249, 884, 1076.25, 59.98, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 120, 19.0, 176, 259, 877, 1056.05, 59.99, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 130, 19.0, 183, 269, 870, 1035.85, 59.99, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 140, 19.0, 190, 279, 863, 1015.65, 60.00, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 70, 25.0, 133, 196, 920, 1181.47, 59.95, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 80, 25.0, 140, 206, 912, 1162.22, 60.00, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 90, 25.0, 148, 218, 904, 1138.65, 60.01, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 100, 25.0, 155, 228, 898, 1117.50, 59.97, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 110, 25.0, 163, 240, 890, 1093.93, 59.98, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 120, 25.0, 170, 250, 882, 1074.69, 60.03, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 130, 25.0, 178, 262, 874, 1051.12, 60.03, 1650, 2750, 1750, 2630, 3100, 1000],
    [16.6, 0.68, 140, 25.0, 185, 272, 868, 1029.96, 59.99, 1650, 2750, 1750, 2630, 3100, 1000]
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
st.sidebar.subheader("📐 Propriedades Físicas dos Materiais")
me_cimento_sel = st.sidebar.selectbox("Massa Específica Cimento (kg/m³)", options=lista_me_cimento, index=20)
me_areia_sel = st.sidebar.selectbox("Massa Específica Areia (kg/m³)", options=lista_me_areia, index=18)
me_brita_sel = st.sidebar.selectbox("Massa Específica Brita (kg/m³)", options=lista_me_brita, index=14)
mu_areia_sel = st.sidebar.selectbox("Massa Unitária Areia (kg/m³)", options=lista_mu_areia, index=6)
mu_brita_sel = st.sidebar.selectbox("Massa Unitária Brita (kg/m³)", options=lista_mu_brita, index=8)
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
    # Procura o fcj mais próximo dentro do banco de dados fornecido
    fcj_proximo = min([row[0] for row in dados_cp32], key=lambda x: abs(x - fcj))
    slump_ajustado = int(round(slump_escolhido / 10.0)) * 10
    slump_ajustado = max(70, min(140, slump_ajustado))
    dmax_ajustado = float(dmax_escolhido)

    linha_encontrada = None
    for row in dados_cp32:
        if abs(row[0] - fcj_proximo) < 0.1 and row[2] == slump_ajustado and row[3] == dmax_ajustado:
            linha_encontrada = row
            break
            
    if linha_encontrada is None:
        linha_encontrada = dados_cp32[0]

    # Busca dinâmica da tabela nova mapeada
    ac = linha_encontrada[1]
    ca_inicial = linha_encontrada[4]
    
    if tipo_cimento == "CP II 40":
        ac = 0.39
        
    cc = ca_inicial / ac
    c_adit = cc * 0.007
    
    cb_total = linha_encontrada[6]
    careia_total_seca = linha_encontrada[7]
    teor_argamassa_tabela = linha_encontrada[9]
    
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
    
    vol_obra_areia_a = ((traco_unit["Areia A"] * 50) * fator_inchamento) / (mu_areia_sel / 1000) if ca_a > 0 else 0
    vol_obra_areia_b = ((traco_unit["Areia B"] * 50) * fator_inchamento) / (mu_areia_sel / 1000) if ca_b > 0 else 0
    vol_obra_brita_a = ((traco_unit["Brita A"] * 50)) / (mu_brita_sel / 1000) if cb_a > 0 else 0
    vol_obra_brita_b = ((traco_unit["Brita B"] * 50)) / (mu_brita_sel / 1000) if cb_b > 0 else 0
    vol_obra_brita_c = ((traco_unit["Brita C"] * 50)) / (mu_brita_sel / 1000) if cb_c > 0 else 0
    vol_obra_agua = max(0.0, (traco_unit["Água"] * 50))

    return {
        "ac": ac, "ca": ca_ajustada, "cc": cc, "c_adit": c_adit, "peso_total": peso_total,
        "ca_a": ca_a, "ca_b": ca_b, "cb_a": cb_a, "cb_b": cb_b, "cb_c": cb_c, "fcj_proximo": fcj_proximo,
        "teor_argamassa": teor_argamassa_tabela,
        "unitario": traco_unit,
        "obra_litros": {
            "Areia A": vol_obra_areia_a, "Areia B": vol_obra_areia_b,
            "Brita A": vol_obra_brita_a, "Brita B": vol_obra_brita_b, "Brita C": vol_obra_brita_c,
            "Água": vol_obra_agua, "Aditivo": (traco_unit["Aditivo"] * 50) / me_aditivo_sel
        }
    }




res_32 = buscar_e_calcular_traco("CP II 32")
res_40 = buscar_e_calcular_traco("CP II 40")

if erro_brita or erro_areia:
    st.error("🚨 Ajuste a barra lateral: As somas de britas e areias precisam dar exatamente 100% antes de liberar os resultados.")
else:
    st.header("Seção 1: Traço dos Materiais em Massa (kg/m³)")
    col_m32, col_m40 = st.columns(2)
    
    with col_m32:
        st.subheader("Cimento CP II-32")
        st.caption(f"fcj Buscado: {res_32['fcj_proximo']:.1f} MPa | Relação a/c Tabela: {res_32['ac']:.2f}")
        df_32_massa = pd.DataFrame({
            "Material": ["Cimento", "Areia A", "Areia B", "Brita A", "Brita B", "Brita C", "Água", "Aditivo"],
            "Massa Corrigida (kg)": [int(round(res_32['cc'])), int(round(res_32['ca_a'])), int(round(res_32['ca_b'])), int(round(res_32['cb_a'])), int(round(res_32['cb_b'])), int(round(res_32['cb_c'])), int(round(res_32['ca'])), int(round(res_32['c_adit']))],
            "Traço Unitário": [f"{res_32['unitario']['Cimento']:.0f}", f"{res_32['unitario']['Areia A']:.2f}", f"{res_32['unitario']['Areia B']:.2f}", f"{res_32['unitario']['Brita A']:.2f}", f"{res_32['unitario']['Brita B']:.2f}", f"{res_32['unitario']['Brita C']:.2f}", f"{res_32['unitario']['Água']:.2f}", f"{res_32['unitario']['Aditivo']:.3f}"]
        })
        st.dataframe(df_32_massa, use_container_width=True, hide_index=True)
        st.metric("Teor de Argamassa", f"{int(round(res_32['teor_argamassa']))}%")
        st.metric("Massa Total Adensada (32)", f"{int(round(res_32['peso_total']))} kg/m³")
        
    with col_m40:
        st.subheader("Cimento CP II-40")
        st.caption(f"fcj Buscado: {res_40['fcj_proximo']:.1f} MPa | Relação a/c Tabela: {res_40['ac']:.2f}")
        df_40_massa = pd.DataFrame({
            "Material": ["Cimento", "Areia A", "Areia B", "Brita A", "Brita B", "Brita C", "Água", "Aditivo"],
            "Massa Corrigida (kg)": [int(round(res_40['cc'])), int(round(res_40['ca_a'])), int(round(res_40['ca_b'])), int(round(res_40['cb_a'])), int(round(res_40['cb_b'])), int(round(res_40['cb_c'])), int(round(res_40['ca'])), int(round(res_40['c_adit']))],
            "Traço Unitário": [f"{res_40['unitario']['Cimento']:.0f}", f"{res_40['unitario']['Areia A']:.2f}", f"{res_40['unitario']['Areia B']:.2f}", f"{res_40['unitario']['Brita A']:.2f}", f"{res_40['unitario']['Brita B']:.2f}", f"{res_40['unitario']['Brita C']:.2f}", f"{res_40['unitario']['Água']:.2f}", f"{res_40['unitario']['Aditivo']:.3f}"]
        })
        st.dataframe(df_40_massa, use_container_width=True, hide_index=True)
        st.metric("Teor de Argamassa", f"{int(round(res_40['teor_argamassa']))}%")
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
