import streamlit as st
import pandas as pd

# Настройка страницы
st.set_page_config(page_title="Расчет стержня фермы", layout="centered")
st.title("🏗️ Подбор сортамента фермы")

# --- БАЗА ДАННЫХ ---
sortament_data = [
    {"b": 125, "d": 8, "F": 19.7, "rx": 3.87, "ry_8": 5.46, "ry_10": 5.39, "ry_12": 5.53, "ry_14": 5.60},
    {"b": 125, "d": 9, "F": 22.0, "rx": 3.86, "ry_8": 5.48, "ry_10": 5.41, "ry_12": 5.56, "ry_14": 5.63},
]
df_sort = pd.DataFrame(sortament_data)

# --- ИСХОДНЫЕ ДАННЫЕ ---
N = st.number_input("Продольное усилие N (кН):", value=876.0)
R = st.number_input("Расчетное сопротивление R (кН/см²):", value=30.0)
L = st.number_input("Геометрическая длина стержня L (м):", value=3.2)
Yx = st.number_input("Yx:", value=0.9)
Yy = st.number_input("Yy:", value=0.9)
t_фасонки = st.selectbox("Толщина фасонки t (мм):", [8, 10, 12, 14])

# --- РАСЧЕТ ---
phi = 0.705 
A_tr = (N * Yx) / (phi * R * Yy)
df_filtered = df_sort[df_sort["F"] >= (A_tr / 2)]

if not df_filtered.empty:
    best = df_filtered.iloc[0]
    As = best['F']
    ix = best['rx']
    iy = best[f"ry_{t_фасонки}"]
    
    # Расчет λ
    lx = (L * 100) * Yx / ix
    ly = (L * 100) * Yy / iy
    lambda_max = round(max(lx, ly))
    
    # Расчет σ по формуле из твоего решения
    sigma = (N * Yx) / (2 * As * phi * Yy)
    diff = (R - sigma) / R * 100
    
    st.write("### Вот решение:")
    st.markdown(f"""
    1. **Aтр** = {A_tr:.2f} см²
    2. **Aтр/2** = {A_tr/2:.2f} см²
    3. **∟** = {int(best['b'])}x{int(best['d'])}
       **As** = {As:.2f} см²
       **ix** = {ix:.2f} см
       **iy** = {iy:.2f} см
    4. **λx** = {lx:.1f}
       **λy** = {ly:.1f}
    5. **λ** = {lambda_max}
    6. **σ** = {sigma:.2f} кН/см²
    7. **(R-σ)/R * 100%** = {diff:.1f}%
    """)
    
    if diff <= 10 or sigma > R:
        st.error("❌ ВСЁ плохо, Выберите другую λ")
    else:
        st.success(f"✅ Молодец, у тебя ответ: σ = {sigma:.2f} кН/см²")
