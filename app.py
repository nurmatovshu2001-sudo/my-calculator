import streamlit as st
import pandas as pd

st.set_page_config(page_title="Расчет стержня фермы", layout="centered")
st.title("🏗️ Подбор сортамента фермы")

# --- БАЗА ДАННЫХ (с ry_8, ry_10, ry_12, ry_14) ---
sortament_data = [
    {"b": 125, "d": 9, "F": 22.0, "rx": 3.86, "ry_8": 5.48, "ry_10": 5.41, "ry_12": 5.56, "ry_14": 5.63},
    # Добавь остальные строки из таблицы по этому же шаблону...
]
df_sort = pd.DataFrame(sortament_data)

# --- ИСХОДНЫЕ ДАННЫЕ ---
st.subheader("📋 Исходные данные")
N = st.number_input("Продольное усилие N (кН):", value=876.0)
R = st.number_input("Расчетное сопротивление R (кН/см²):", value=30.0)
L = st.number_input("Геометрическая длина стержня L (м):", value=3.2)
Yx = st.number_input("Yx:", value=0.9)
Yy = st.number_input("Yy:", value=0.9)
t_фасонки = st.selectbox("Толщина фасонки t (мм):", [8, 10, 12, 14])

# --- ЭТАП 1: ПОДБОР ---
st.subheader("⚙️ Этап 1: Подбор сечения")
lambda_input = st.number_input("Задайте начальную гибкость λ (для подбора):", value=70)
phi_input = st.number_input("Задайте коэффициент фи φ (для подбора):", value=0.705, format="%.3f")

# Вычисление Атр для подбора
A_tr = (N * Yx) / (phi_input * R * Yy)
df_filtered = df_sort[df_sort["F"] >= (A_tr / 2)]

if not df_filtered.empty:
    best = df_filtered.iloc[0]
    As = best['F']
    ix = best['rx']
    iy = best[f"ry_{t_фасонки}"]
    
    st.write(f"Подобрано сечение: ∟ {int(best['b'])}x{int(best['d'])}, As = {As} см²")
    
    # --- ЭТАП 2: ИТОГОВОЕ РЕШЕНИЕ ---
    st.subheader("📊 Этап 2: Итоговое решение")
    
    # Расчет λ факт
    lx_fact = (L * 100) * Yx / ix
    ly_fact = (L * 100) * Yy / iy
    lambda_max = round(max(lx_fact, ly_fact))
    
    # Тут должна быть логика поиска фи по lambda_max из таблицы
    # Для примера берем фи из рукописного решения (0.597)
    phi_fact = 0.597 
    
    sigma = (N * Yx) / (2 * As * phi_fact * Yy)
    diff = (R - sigma) / R * 100
    
    st.markdown(f"""
    1. **Aтр** = {A_tr:.2f} см²
    2. **Aтр/2** = {A_tr/2:.2f} см²
    3. **∟** = {int(best['b'])}x{int(best['d'])}
       **As** = {As:.2f} см²
       **ix** = {ix:.2f} см
       **iy** = {iy:.2f} см
    4. **λx** = {lx_fact:.1f}
       **λy** = {ly_fact:.1f}
    5. **λ** = {lambda_max} (фи = {phi_fact})
    6. **σ** = {sigma:.2f} кН/см²
    7. **(R-σ)/R * 100%** = {diff:.1f}%
    """)
    
    if diff <= 10 or sigma > R:
        st.error("❌ ВСЁ плохо, Выберите другую λ")
    else:
        st.success("✅ Молодец!")
else:
    st.error("⚠️ Увеличьте площадь сечения!")
