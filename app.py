import streamlit as st
import pandas as pd
import io

# Данные внутри кода — теперь они точно не пропадут
sort_csv = """b;d;As;ix, см;iy_8;iy_10;iy_12;iy_14
100;10;19.2;3.05;4.63;4.63;4.63;4.63
125;8;19.6;3.86;5.56;5.56;5.56;5.56
""" # (Добавь сюда остальные строки из своего сортамента в таком же формате)

phi_csv = """lambda;240;300;360
70;0.750;0.750;0.750
37;0.865;0.865;0.865
""" # (Добавь остальные значения фи)

df_sort = pd.read_csv(io.StringIO(sort_csv), sep=';')
df_phi = pd.read_csv(io.StringIO(phi_csv), sep=';').set_index('lambda')

st.title("Расчет")

N = st.number_input("N (кН):", value=980.0)
R = st.selectbox("Ry (МПа):", [240, 300, 360])
L = st.number_input("L (см):", value=150.0)
T = st.selectbox("t (мм):", [8, 10, 12, 14])
Ys = st.number_input("Ys:", value=0.95)
Yy = st.number_input("Yy:", value=0.95)

if st.button("Рассчитать"):
    R_knsm2 = R / 10
    phi_pre = df_phi.loc[70, R] / 1000
    A_half = (N * Ys) / (phi_pre * R_knsm2 * Yy * 2)
    best = df_sort[df_sort['As'] >= A_half].iloc[0]
    
    lam = max((L * Ys) / best['ix, см'], (L * Ys) / best[f'iy_{T}'])
    phi = df_phi.loc[int(lam), R] / 1000
    sigma = (N * Ys) / (2 * best['As'] * phi * Yy)
    
    delta = ((R_knsm2 - sigma) / R_knsm2) * 100
    st.write(f"Дельта: {delta:.2f}%")
