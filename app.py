import streamlit as st
import pandas as pd
import io

# --- 1. НАСТРОЙКИ ---
st.set_page_config(page_title="Расчет фермы", layout="centered")

# --- 2. БАЗА ДАННЫХ (ГОСТ 8509-72) ---
# Сюда вставлены данные из твоего PDF
sort_data = [
    {"b": 45, "d": 4, "F": 3.48, "ix": 1.38, "iy_8": 2.24, "iy_10": 2.16, "iy_12": 2.32, "iy_14": 2.40},
    {"b": 50, "d": 4, "F": 3.89, "ix": 1.54, "iy_8": 2.35, "iy_10": 2.43, "iy_12": 2.51, "iy_14": 2.59},
    {"b": 63, "d": 5, "F": 6.13, "ix": 1.94, "iy_8": 2.92, "iy_10": 2.98, "iy_12": 3.04, "iy_14": 3.11},
    {"b": 125, "d": 9, "F": 22.0, "ix": 3.86, "iy_8": 5.48, "iy_10": 5.41, "iy_12": 5.56, "iy_14": 5.63}
]
df_sort = pd.DataFrame(sort_data)

# --- 3. ИНТЕРФЕЙС ВВОДА ---
st.title("🏗️ Расчет стержня")
N = st.number_input("N (кН):", value=876.0)
R = st.number_input("R (кН/см²):", value=30.0)
L = st.number_input("l (м):", value=3.2)
Yx = st.number_input("Yx:", value=0.9)
Yy = st.number_input("Yy:", value=0.9)
T = st.selectbox("T (фасонка, мм):", [8, 10, 12, 14])
lam1 = st.number_input("λ1:", value=70)

# --- 4. ЛОГИКА РАСЧЕТА (ВСЁ ВНУТРИ КНОПКИ) ---
if st.button("🚀 Выполнить расчет"):
    try:
        # 0. фи1 (заглушка для примера, замени на функцию поиска по своей таблице Фи)
        phi1 = 0.705 
        
        # 1. Атр
        A_tr = (N * Yx) / (phi1 * R * Yy)
        # 2. Атр/2
        A_half = A_tr / 2
        
        # 3. ПОДБОР ПО ТАБЛИЦЕ
        best = df_sort[df_sort["F"] >= A_half].iloc[0]
        As = best["F"]
        ix = best["ix"]
        iy = best[f"iy_{T}"]
        
        # 4. λx, λy
        lam_x = (L * 100 * Yx) / ix
        lam_y = (L * 100 * Yy) / iy
        
        # 5. λ2
        lam2 = round(max(lam_x, lam_y))
        phi2 = 0.600 # Замени на get_phi(lam2, R)
        
        # 6. σ
        sigma = (N * Yx) / (2 * As * phi2 * Yy)
        
        # 7. %
        diff = ((R - sigma) / R) * 100
        
        # --- ВЫВОД 7 ПУНКТОВ ---
        st.markdown(f"**λ1 = {lam1} ; φ1 = {phi1:.3f}**")
        st.markdown(f"""
        1. **Атр** = {A_tr:.2f} см²
        2. **Атр/2** = {A_half:.2f} см²
        3. **∟** = {int(best['b'])}x{int(best['d'])} <br> 
           **As** = {As:.2f} см² | **ix** = {ix:.2f} см | **iy** = {iy:.2f} см
        4. **λx** = {lam_x:.1f} | **λy** = {lam_y:.1f}
        5. **λ2** = {lam2}
        6. **σ** = {sigma:.2f} <= {R}
        7. **(R-σ)/R * 100%** = {diff:.1f}%
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Ошибка в расчетах: {e}. Проверь таблицу сортамента!")
