import streamlit as st
import pandas as pd

# Força o layout em tela cheia para caber as tabelas comparativas lado a lado
st.set_page_config(page_title="Calculadora ABCP Pro", layout="wide")

st.title("Calculadora de Traços de Concreto - Método ABCP")
st.write("Modifique os parâmetros na barra lateral esquerda. O recálculo ocorrerá puxando os dados exatos do seu laboratório.")

# -----------------------------------------------------------------------------
# DEFINIÇÃO DAS LISTAS REGULAMENTARES DO LABORATÓRIO (Menus de Escolha de Massas)
# -----------------------------------------------------------------------------
lista_mu_areia = list(range(1400, 1710, 10))
lista_me_brita = list(range(2600, 3010, 10))
lista_mu_brita = list(range(1400, 1710, 10))
lista_me_areia = list(range(2450, 2760, 10))
lista_me_cimento = list(range(2900, 3210, 10))
lista_me_aditivo = [round(x * 0.01, 2) for x in range(90, 141)]

# -----------------------------------------------------------------------------
# CONTROLES DA BARRA LATERAL (ENTRADAS REGULAMENTARES DO USUÁRIO)
# -----------------------------------------------------------------------------
st.sidebar.header("📥 Parâmetros Gerais")
# fck limitado de 10 a 40 MPa conforme seu pedido
fck = st.sidebar.number_input("fck Desejado (MPa)", min_value=10.0, max_value=40.0, value=40.0, step=5.0)
sd = 4.0
fcj = fck + 1.65 * sd

st.sidebar.markdown("---")
st.sidebar.subheader("💧 Consumo de Água (Slump)")
slump_escolhido = st.sidebar.selectbox("Abatimento / Slump (mm)", options=[70, 80, 90, 100, 110, 120, 130, 140], index=3)
dmax_escolhido = st.sidebar.selectbox("Diâmetro Máximo Brita Dmáx (mm)", options=[9.5, 12.5, 19.0, 25.0], index=2)

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Seleção do Teor de Argamassa")
teor_argamassa_escolhido = st.sidebar.slider("Teor de Argamassa desejado (%)", min_value=45, max_value=60, value=53, step=1)

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
umidade_areia = st.sidebar.number_input("Umidade da Areia (%)", min_value=0.0, max_value=25.0, value=0.0, step=0.5)
inchamento_areia = st.sidebar.number_input("Inchamento da Areia (%)", min_value=0.0, max_value=50.0, value=0.0, step=0.5)

# Painel Superior Indicativo com formatação laboratorial (0.0)
col_fck, col_fcj = st.columns(2)
with col_fck:
    st.metric(label="fck Selecionado", value=f"{fck:.1f} MPa")
with col_fcj:
    st.metric(label="fcj 28 Dias Calculado", value=f"{fcj:.1f} MPa", delta="sd = 4.0")

st.markdown("---")

# -----------------------------------------------------------------------------
# BANCO DE DADOS INTELIGENTE - CÁLCULO DIRETO CONFORME AS NOVAS ABAS ENVIADAS
# -----------------------------------------------------------------------------
def buscar_e_calcular_traco(tipo_cimento):
    # Correção do consumo e relação a/c: CP II-32 consome mais cimento e tem menor a/c que o CP II-40
    if tipo_cimento == "CP II 32":
        ac = 0.68 - ((fcj - 16.6) * 0.014)
        ac = max(0.25, min(0.70, ac))
        
        if slump_escolhido <= 70:
            ca_inicial = 160.0 if dmax_escolhido == 9.5 else (147.8 if dmax_escolhido == 12.5 else 142.0)
        elif slump_escolhido <= 100:
            ca_inicial = 175.0 if dmax_escolhido == 9.5 else (166.8 if dmax_escolhido == 12.5 else 163.0)
        else:
            ca_inicial = 195.0 if dmax_escolhido == 9.5 else (191.8 if dmax_escolhido == 12.5 else 190.0)
    else:
        ac = 0.78 - ((fcj - 16.6) * 0.011)
        ac = max(0.35, min(0.85, ac))
        
        if slump_escolhido <= 70:
            ca_inicial = 172.0 if dmax_escolhido == 9.5 else (158.0 if dmax_escolhido == 12.5 else 151.0)
        elif slump_escolhido <= 100:
            ca_inicial = 180.0 if dmax_escolhido == 9.5 else (170.0 if dmax_escolhido == 12.5 else 165.0)
        else:
            ca_inicial = 194.0 if dmax_escolhido == 9.5 else (180.0 if dmax_escolhido == 12.5 else 177.0)

    cc = ca_inicial / ac
    c_adit = cc * 0.007
    
    # Busca do volume compactado pelas tabelas de massa do novo arquivo
    vb = 0.565 if dmax_escolhido == 9.5 else (0.622 if dmax_escolhido == 12.5 else 0.690)
    cb_total = vb * mu_brita_sel
    
    vol_cimento = cc / me_cimento_sel
    vol_agua_inicial = ca_inicial / 1000.0
    vol_brita = cb_total / me_brita_sel
    vol_adit = c_adit / me_aditivo_sel
    vol_ar = 0.02
    
    vol_areia_total_seca = 1.0 - (vol_cimento + vol_agua_inicial + vol_brita + vol_adit + vol_ar)
    if vol_areia_total_seca < 0:
        vol_areia_total_seca = 0.25
        
    careia_total_seca = vol_areia_total_seca * me_areia_sel
    
    # CORREÇÃO DA UMIDADE: Soma a água na massa da areia úmida e desconta da água limpa
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
    
    # CORREÇÃO DO INCHAMENTO: Atua de forma direta no volume final da areia na obra (Seção 2)
    fator_inchamento = 1.0 + (inchamento_areia / 100.0)
    vol_obra_areia_a = ((traco_unit["Areia A"] * 50) * fator_inchamento) / (mu_areia_sel / 1000) if ca_a > 0 else 0
    vol_obra_areia_b = ((traco_unit["Areia B"] * 50) * fator_inchamento) / (mu_areia_sel / 1000) if ca_b > 0 else 0
    vol_obra_brita_a = ((traco_unit["Brita A"] * 50)) / (mu_brita_sel / 1000) if cb_a > 0 else 0
    vol_obra_brita_b = ((traco_unit["Brita B"] * 50)) / (mu_brita_sel / 1000) if cb_b > 0 else 0
    vol_obra_brita_c = ((traco_unit["Brita C"] * 50)) / (mu_brita_sel / 1000) if cb_c > 0 else 0
    vol_obra_agua = max(0.0, (traco_unit["Água"] * 50))

    return {
        "ac": ac, "ca": ca_ajustada, "cc": cc, "c_adit": c_adit, "peso_total": peso_total,
        "ca_a": ca_a, "ca_b": ca_b, "cb_a": cb_a, "cb_b": cb_b, "cb_c": cb_c,
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
    st.error("🚨 Ajuste a barra lateral: As somas de britas e areias precisam dar exatamente 100% para liberar os resultados.")
else:
    st.header("Seção 1: Traço dos Materiais em Massa (kg/m³)")
    col_m32, col_m40 = st.columns(2)
    
    with col_m32:
        st.subheader("Cimento CP II-32")
        st.caption(f"Relação a/c Tabela: {res_32['ac']:.2f} | Água Efetiva: {res_32['ca']:.0f} L")
        
        df_32_massa = pd.DataFrame(
            data=[
                [int(round(res_32['cc'])), f"1.00"],
                [int(round(res_32['ca_a'])), f"{res_32['unitario']['Areia A']:.2f}"],
                [int(round(res_32['ca_b'])), f"{res_32['unitario']['Areia B']:.2f}"],
                [int(round(res_32['cb_a'])), f"{res_32['unitario']['Brita A']:.2f}"],
                [int(round(res_32['cb_b'])), f"{res_32['unitario']['Brita B']:.2f}"],
                [int(round(res_32['cb_c'])), f"{res_32['unitario']['Brita C']:.2f}"],
                [int(round(res_32['ca'])), f"{res_32['unitario']['Água']:.2f}"],
                [int(round(res_32['c_adit'])), f"{res_32['unitario']['Aditivo']:.3f}"]
            ],
            columns=["Massa Corrigida (kg)", "Traço Unitário"],
            index=["Cimento", "Areia A", "Areia B", "Brita A", "Brita B", "Brita C", "Água", "Aditivo"]
        )
        st.dataframe(df_32_massa, use_container_width=True)
        st.metric("Massa Total Adensada (32)", f"{int(round(res_32['peso_total']))} kg/m³")
        st.metric("Teor de Argamassa Mapeado (32)", f"{teor_argamassa_escolhido}%")
        
    with col_m40:
        st.subheader("Cimento CP II-40")
        st.caption(f"Relação a/c Tabela: {res_40['ac']:.2f} | Água Efetiva: {res_40['ca']:.0f} L")
        
        df_40_massa = pd.DataFrame(
            data=[
                [int(round(res_40['cc'])), f"1.00"],
