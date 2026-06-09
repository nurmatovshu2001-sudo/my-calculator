import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Расчет фермы", layout="centered")
st.title("🏗️ Расчет стержня фермы")

# 1. ТАБЛИЦА ФИ (полная структура)
# Замени этот блок на свою таблицу, если она отличается
raw_table = """λ,200,220,240,260,280,300,320,340,360,380,400
70,801,789,776,763,750,736,723,709,695,682,668
80,754,739,724,709,693,677,661,645,629,613,597"""
df_phi = pd.read_csv(io.StringIO(raw_table)).set_index("λ")

# 2. ИНТЕРФЕЙС
N = st.number_input("Продольное усилие N (кН):", value=876.0)
R = st.number_input("Сопротивление R (кН/см²):", value=30.0)
L = st.number_input("Длина L (м):", value=3.2)
Yx = st.number_input("Yx:", value=0.9)
Yy = st.number_input("Yy:", value=0.9)
t_фас = st.selectbox("Толщина фасонки (мм):", [8, 10, 12, 14])
lambda_init = st.number_input("Начальная гибкость λ:", value=70)

# 3. КНОПКА И ЛОГИКА (ВСЁ ВНУТРИ)
if st.button("🚀 Выполнить расчет"):
    try:
        # Поиск ФИ (упрощенный пример)
        phi = 0.597 
        
        # Расчет
        A_tr = (N * Yx) / (phi * R * Yy)
        A_half = A_tr / 2
        
        # Подбор (имитация выбора 125х9)
        b, d, As, ix, iy = 125, 9, 22.0, 3.86, 5.48
        
        lx = (L * 100) * Yx / ix
        ly = (L * 100) * Yy / iy
        lam_max = round(max(lx, ly))
        
        sigma = (N * Yx) / (2 * As * phi * Yy)
        diff = (R - sigma) / R * 100
        
        # ВЫВОД 7 ПУНКТОВ
        st.subheader("Вот решение:")
        st.markdown(f"""
        1. **Aтр** = {A_tr:.2f} см²
        2. **Aтр/2** = {A_half:.2f} см²
        3. **∟** = {b}x{d} <br>
           **As** = {As} см² <br>
           **ix** = {ix} см <br>
           **iy** = {iy} см
        4. **λx** = {lx:.1f}  **λy** = {ly:.1f}
        5. **λ** = {lam_max}
        6. **σ** = {sigma:.2f} кН/см²
        7. **(R-σ)/R * 100%** = {diff:.1f}%
        """)
        
        if diff <= 10 or sigma > R:
            st.error("❌ ВСЁ плохо, Выберите другую λ")
        else:
            st.success("✅ Молодец!")
            
    except Exception as e:
        st.error(f"Ошибка при расчете: {e}")
