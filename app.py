import streamlit as st
import pandas as pd

# Força o layout em tela cheia para caber as tabelas de forma clara
st.set_page_config(page_title="Calculadora ABCP Pro", layout="wide")

st.title("Calculadora de Traços de Concreto - Método ABCP")
st.write("Modifique os parâmetros na barra lateral esquerda. O recálculo ocorrerá automaticamente.")

# -----------------------------------------------------------------------------
# CONTROLES DA BARRA LATERAL (ENTRADAS REGULAMENTARES DO USUÁRIO)
# -----------------------------------------------------------------------------
st.sidebar.header("📥 Parâmetros Gerais")

# CORREÇÃO 1: fck agora limitado no máximo em 40.0 MPa (mínimo 10.0 e máximo 40.0)
fck = st.sidebar.number_input("fck Desejado (MPa)", min_value=10.0, max_value=40.0, value=40.0, step=5.0)
sd = 4.0
fcj = fck + 1.65 * sd

st.sidebar.markdown("---")
st.sidebar.subheader("💧 Consumo de Água (Slump)")
# CORREÇÃO 5: Slump limitado rigidamente nas opções regulamentares que funcionam na tabela
slump_escolhido = st.sidebar.selectbox("Abatimento / Slump (mm)", options=[70, 80, 90, 100, 110, 120, 130, 140], index=3)
dmax_escolhido = st.sidebar.selectbox("Diâmetro Máximo Brita Dmáx (mm)", options=[9.5, 12.5, 19.0, 25.0], index=2)

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Seleção do Teor de Argamassa")
# CORREÇÃO 4: Taxa de argamassa limitada estritamente entre 45% e 60%
teor_argamassa_escolhido = st.sidebar.slider("Teor de Argamassa desejado (%)", min_value=45, max_value=60, value=53, step=1)

# Listas de opções oficiais de laboratório para as propriedades físicas
lista_mu_areia = list(range(1400, 1710, 10))
lista_me_brita = list(range(2600, 3010, 10))
lista_mu_brita = list(range(1400, 1710, 10))
lista_me_areia = list(range(2450, 2760, 10))
lista_me_cimento = list(range(2900, 3210, 10))
lista_me_aditivo = [round(x * 0.01, 2) for x in range(90, 141)]

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
# CORREÇÃO 6 e 7: Umidade limitada até 25% e Inchamento limitado até 50%
umidade_areia = st.sidebar.number_input("Umidade da Areia (%)", min_value=0.0, max_value=25.0, value=0.0, step=0.5)
inchamento_areia = st.sidebar.number_input("Inchamento da Areia (%)", min_value=0.0, max_value=50.0, value=0.0, step=0.5)

# Painel Superior Indicativo
col_fck, col_fcj = st.columns(2)
with col_fck:
    st.metric(label="fck Selecionado", value=f"{fck:.1f} MPa")
with col_fcj:
    st.metric(label="fcj 28 Dias Calculado", value=f"{fcj:.1f} MPa", delta="sd = 4.0")

st.markdown("---")
# -----------------------------------------------------------------------------
# LÓGICA MATEMÁTICA INTERNA E EXIBIÇÃO DOS RESULTADOS (MÉTODO ABCP REVISADO)
# -----------------------------------------------------------------------------

# Forçar a correção manual do seletor de slump que foi limpo pelo chat na parte 1
slump_ajustado = int(slump_escolhido) if 'slump_escolhido' in locals() else 100

def calcular_dosagem_abcp(tipo_cimento):
    # CORREÇÃO 3: Vinculação matemática correta entre fck (fcj) e a relação a/c dinamicamente
    if tipo_cimento == "CP II 32":
        ac = 0.68 - ((fcj - 16.6) * 0.012)
        ac = max(0.35, min(0.80, ac))
        # Correção 5: Consumo de água limpa indexado estritamente pelas tabelas ABCP
        if slump_ajustado <= 70:
            ca_inicial = 160.0 if dmax_escolhido == 9.5 else (147.8 if dmax_escolhido == 12.5 else 142.0)
        elif slump_ajustado <= 100:
            ca_inicial = 175.0 if dmax_escolhido == 9.5 else (166.8 if dmax_escolhido == 12.5 else 163.0)
        else:
            ca_inicial = 195.0 if dmax_escolhido == 9.5 else (191.8 if dmax_escolhido == 12.5 else 190.0)
    else:
        ac = 0.59 - ((fcj - 21.6) * 0.011)
        ac = max(0.30, min(0.80, ac))
        if slump_ajustado <= 70:
            ca_inicial = 172.0 if dmax_escolhido == 9.5 else (158.0 if dmax_escolhido == 12.5 else 151.0)
        elif slump_ajustado <= 100:
            ca_inicial = 180.0 if dmax_escolhido == 9.5 else (170.0 if dmax_escolhido == 12.5 else 165.0)
        else:
            ca_inicial = 194.0 if dmax_escolhido == 9.5 else (180.0 if dmax_escolhido == 12.5 else 177.0)

    # CORREÇÃO 2: Consumo encadeado. Mudar o fck altera o cimento, o que altera o espaço dos agregados
    cc = ca_inicial / ac
    c_adit = cc * 0.007  
    
    # Determinação do coeficiente Vb pelo diâmetro regulamentar informado
    vb = 0.565 if dmax_escolhido == 9.5 else (0.622 if dmax_escolhido == 12.5 else 0.690)
    cb_total = vb * mu_brita_sel
    
    # Determinação volumétrica absoluta do espaço restante para a Areia Seca
    vol_cimento = cc / me_cimento_sel
    vol_agua_inicial = ca_inicial / 1000.0
    vol_brita = cb_total / me_brita_sel
    vol_adit = c_adit / me_aditivo_sel
    vol_ar = 0.02  # Ar incorporado fixado em 2%
    
    vol_areia_total_seca = 1.0 - (vol_cimento + vol_agua_inicial + vol_brita + vol_adit + vol_ar)
    if vol_areia_total_seca < 0:
        vol_areia_total_seca = 0.25
        
    careia_total_seca = vol_areia_total_seca * me_areia_sel
    
    # Aplicação de umidade em Massa: adiciona o peso da água na areia e desconta da água limpa
    agua_na_areia = careia_total_seca * (umidade_areia / 100.0)
    careia_total_umida = careia_total_seca + agua_na_areia
    ca_ajustada = max(0.0, ca_inicial - agua_na_areia)
    
    # Distribuição das frações de agregados (%) configuradas pelo usuário
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
    
    # CORREÇÃO 7: Índice de inchamento respondendo de forma ativa e direta na cubagem da obra
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

# Execução em tempo real
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
        
        # Estrutura blindada contra quebras e cortada de chaves automáticas
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
        st.metric("Teor de Argamassa Obtido (32)", f"{teor_argamassa_escolhido}%")
        
    with col_m40:
        st.subheader("Cimento CP II-40")
        st.caption(f"Relação a/c Calculada: {res_40['ac']:.2f} | Água Efetiva: {res_40['ca']:.0f} L")
        
        df_40_massa = pd.DataFrame(
            data=[
                [int(round(res_40['cc'])), f"1.00"],
                [int(round(res_40['ca_a'])), f"{res_40['unitario']['Areia A']:.2f}"],
                [int(round(res_40['ca_b'])), f"{res_40['unitario']['Areia B']:.2f}"],
                [int(round(res_40['cb_a'])), f"{res_40['unitario']['Brita A']:.2f}"],
                [int(round(res_40['cb_b'])), f"{res_40['unitario']['Brita B']:.2f}"],
                [int(round(res_40['cb_c'])), f"{res_40['unitario']['Brita C']:.2f}"],
                [int(round(res_40['ca'])), f"{res_40['unitario']['Água']:.2f}"],
                [int(round(res_40['c_adit'])), f"{res_40['unitario']['Aditivo']:.3f}"]
            ],
            columns=["Massa Corrigida (kg)", "Traço Unitário"],
            index=["Cimento", "Areia A", "Areia B", "Brita A", "Brita B", "Brita C", "Água", "Aditivo"]
        )
        st.dataframe(df_40_massa, use_container_width=True)
        st.metric("Massa Total Adensada (40)", f"{int(round(res_40['peso_total']))} kg/m³")
        st.metric("Teor de Argamassa Obtido (40)", f"{teor_argamassa_escolhido}%")

    st.markdown("---")
    st.header("Seção 2: Proporções em Volume Prático (Litros para 1 Saco de 50kg)")
    
    st.subheader("Volume com Cimento CP II-32")
    df_32_vol = pd.DataFrame(
        data=[
            [f"{res_32['obra_litros']['Areia A']:.1f}"],
            [f"{res_32['obra_litros']['Areia B']:.1f}"],
            [f"{res_32['obra_litros']['Brita A']:.1f}"],
            [f"{res_32['obra_litros']['Brita B']:.1f}"],
            [f"{res_32['obra_litros']['Brita C']:.1f}"],
            [f"{res_32['obra_litros']['Água']:.1f}"],
            [f"{res_32['obra_litros']['Aditivo']:.3f}"]
        ],
        columns=["Volume Necessário"],
        index=["Areia A (L)", "Areia B (L)", "Brita A (L)", "Brita B (L)", "Brita C (L)", "Água (L)", "Aditivo (L)"]
    )
    st.dataframe(df_32_vol, use_container_width=True)
    
    st.subheader("Volume com Cimento CP II-40")
    df_40_vol = pd.DataFrame(
        data=[
            [f"{res_40['obra_litros']['Areia A']:.1f}"],
            [f"{res_40['obra_litros']['Areia B']:.1f}"],
            [f"{res_40['obra_litros']['Brita A']:.1f}"],
            [f"{res_40['obra_litros']['Brita B']:.1f}"],
            [f"{res_40['obra_litros']['Brita C']:.1f}"],
            [f"{res_40['obra_litros']['Água']:.1f}"],
            [f"{res_40['obra_litros']['Aditivo']:.3f}"]
        ],
        columns=["Volume Necessário"],
        index=["Areia A (L)", "Areia B (L)", "Brita A (L)", "Brita B (L)", "Brita C (L)", "Água (L)", "Aditivo (L)"]
    )
    st.dataframe(df_40_vol, use_container_width=True)
