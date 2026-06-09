import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Расчет фермы", layout="centered")

# Данные Фи (сокращенно, добавь все строки из своей таблицы)
raw_phi = """λ,200,220,240,260,280,300,320,340,360,380,400
70,801,789,776,763,750,736,723,709,695,682,668
80,754,739,724,709,693,677,661,645,629,613,597
90,702,686,669,652,634,616,598,581,563,546,529
100,648,630,612,593,574,555,536,518,500,482,464"""
df_phi = pd.read_csv(io.StringIO(raw_phi)).set_index("λ")

def get_phi(lam, r_val):
    col = min(df_phi.columns.astype(int), key=lambda x: abs(x - r_val * 10))
    row = min(df_phi.index, key=lambda x: abs(x - int(lam)))
    return df_phi.loc[row, str(col)] / 1000

st.title("🏗️ Расчет стержня фермы")

# Исходные
N = st.number_input("N (кН):", value=876.0)
R = st.number_input("R (кН/см²):", value=30.0)
L = st.number_input("L (м):", value=3.2)
Yx = st.number_input("Yx:", value=0.9)
Yy = st.number_input("Yy:", value=0.9)
lam1 = st.number_input("λ1 (начальная):", value=70)
phi1 = st.number_input("φ1 (начальный):", value=0.705, format="%.3f")

# Характеристики уголка
st.subheader("Характеристики уголка")
b_x = st.number_input("b (ширина полки):", value=125)
d_x = st.number_input("d (толщина полки):", value=9)
As = st.number_input("As (площадь одного уголка, см²):", value=22.0)
ix = st.number_input("ix (см):", value=3.86)
iy = st.number_input("iy (см):", value=5.41)

if st.button("🚀 Выполнить расчет по пунктам"):
    # 1. Атр
    A_tr = (N * Yx) / (phi1 * R * Yy)
    # 2. Атр/2
    A_half = A_tr / 2
    
    # 4. λx, λy
    lx = (L * 100) * Yx / ix
    ly = (L * 100) * Yy / iy
    
    # 5. λ2
    lam2 = round(max(lx, ly))
    phi2 = get_phi(lam2, R)
    
    # 6. σ
    sigma = (N * Yx) / (2 * As * phi2 * Yy)
    
    # 7. %
    diff = (R - sigma) / R * 100
    
    # ВЫВОД
    st.write("---")
    st.markdown(f"**λ1 = {lam1} ; φ1 = {phi1:.3f}**")
    st.markdown(f"""
    1. **Атр** = {A_tr:.2f} см²
    2. **Атр/2** = {A_half:.2f} см²
    3. **∟** = {b_x}x{d_x} <br>
       **As** = {As} см² <br>
       **ix** = {ix} см <br>
       **iy** = {iy} см
    4. **λx** = {lx:.1f} ; **λy** = {ly:.1f}
    5. **λ2** = {lam2} (φ2 = {phi2:.3f})
    6. **σ** = {sigma:.2f} кН/см² (условие σ ≤ {R})
    7. **(R-σ)/R * 100%** = {diff:.1f}%
    """)
    
    if sigma <= R:
        st.success("✅ Проверка прочности пройдена")
    else:
        st.error("❌ Сечение не проходит!")
