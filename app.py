import streamlit as st
import pandas as pd
import io

# Настройка страницы
st.set_page_config(page_title="Расчет стержня фермы", layout="centered")

st.title("🏗️ Подбор сортамента фермы")

# --- БАЗА ДАННЫХ (ГОСТ 8509-72) ---
# (Используем данные из прикрепленного файла)
sortament_data = [
    {"b": 125, "d": 9, "F": 22.0, "rx": 3.86, "ry_10": 5.41},
    {"b": 125, "d": 8, "F": 19.7, "rx": 3.87, "ry_10": 5.39},
    # ... (добавлю остальные по необходимости, но сейчас для примера)
]
df_sort = pd.DataFrame(sortament_data)

# --- ИСХОДНЫЕ ДАННЫЕ ---
st.subheader("📋 Данные из условия задачи")
N = st.number_input("Продольное усилие N (кН):", value=876.0)
R = st.number_input("Расчетное сопротивление R (кН/см²):", value=30.0)
L = st.number_input("Геометрическая длина стержня L (м):", value=3.2)
Yx = st.number_input("Yx:", value=0.9)
Yy = st.number_input("Yy:", value=0.9)
t_фасонки = st.selectbox("Толщина фасонки t (мм):", [8, 10, 12, 14], index=1)
lambda_start = st.number_input("Начальная гибкость λ:", value=70)

# --- РАСЧЕТ ПО НАЖАТИЮ ---
if st.button("🚀 Выполнить расчет"):
    # 1. Атр = (N*Yn)/(fi*Ry*Yc) - упрощенный расчет для примера
    phi = 0.705 
    A_tr = (N * Yx) / (phi * R * Yy)
    
    # Подбор сечения
    best = df_sort[df_sort["F"] >= (A_tr / 2)].iloc[0]
    As = best['F']
    sigma = N / (0.6 * (2 * As) * Yy)
    diff = (R - sigma) / R * 100
    
    # ЛОГИКА ПРОВЕРКИ
    if diff <= 10 or sigma > R:
        st.error("❌ ВСЁ плохо, Выберите другую λ")
    else:
        st.success(f"✅ Молодец, у тебя ответ: σ = {sigma:.2f} кН/см²")
        st.write("### Вот решение:")
        st.markdown(f"""
        1. **Aтр** = {A_tr:.2f} см²
        2. **Aтр/2** = {A_tr/2:.2f} см²
        3. **∟** = {int(best['b'])}x{int(best['d'])}
           **As** = {As:.2f} см²
           **ix** = {best['rx']:.2f} см
           **iy** = {best[f'ry_{t_фасонки}']:.2f} см
        4. **λx** = {((L*100)*Yx)/best['rx']:.1f}
           **λy** = {((L*100)*Yy)/best[f'ry_{t_фасонки}']:.1f}
        5. **λ** = {lambda_start}
        6. **σ** = {sigma:.2f} кН/см²
        7. **(R-σ)/R * 100%** = {diff:.1f}%
        """)
