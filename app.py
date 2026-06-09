import streamlit as st
import pandas as pd
import io

# Настройка страницы
st.set_page_config(page_title="Расчет стержня фермы", layout="centered")

st.title("🏗️ Подбор сортамента фермы")

# --- БАЗА ДАННЫХ ---
raw_phi_data = """λ,200,220,240,245,260,280,300,320,340,360,380,400,440,480,520
70,801,789,776,773,763,750,736,723,709,695,682,668,641,614,587
83,739,723,708,704,692,675,659,642,626,609,593,577,545,513,481""" # Сокращено для краткости, используй полную версию из прошлого сообщения

df_phi = pd.read_csv(io.StringIO(raw_phi_data.strip()), index_col=0)
df_phi.columns = df_phi.columns.astype(int)

# Сортамент (упрощенная структура)
sortament_data = [
    {"b": 125, "d": 9, "F": 22.0, "rx": 3.86, "ry_10": 5.41},
    {"b": 125, "d": 8, "F": 19.7, "rx": 3.87, "ry_10": 5.39}
]
df_sort = pd.DataFrame(sortament_data)

# --- БЛОК 1: ИСХОДНЫЕ ДАННЫЕ ---
st.subheader("📋 Данные из условия задачи")
N = st.number_input("Продольное усилие N (кН):", value=876.0)
R = st.number_input("Расчетное сопротивление R (кН/см²):", value=30.0)
L = st.number_input("Геометрическая длина стержня L (м):", value=3.2)
Yx = st.number_input("Yx:", value=0.9)
Yy = st.number_input("Yy:", value=0.9)
t_фасонки = st.selectbox("Толщина фасонки t (мм):", [8, 10, 12, 14], index=1)

st.markdown("---")
lambda_start = st.number_input("Начальная гибкость λ:", value=70)

# --- БЛОК 2: КНОПКА И РАСЧЕТ ---
# Кнопка должна идти в конце, чтобы все переменные выше уже существовали
if st.button("🚀 Выполнить автоматический подбор сечения", type="primary"):
    ry_mpa = int(R * 10)
    phi = 0.705 # Упрощенно для примера
    
    A_tr = (N * Yx) / (phi * R * Yy)
    A_one_tr = A_tr / 2
    
    st.write(f"Требуемая площадь одного уголка As: {A_one_tr:.2f} см²")
    
    # Подбор
    best_match = df_sort[df_sort["F"] >= A_one_tr].iloc[0]
    As = best_match['F']
    ix = best_match['rx']
    iy = best_match[f'ry_{t_фасонки}']
    
    st.markdown(f"""
    <div style='background-color:#e8f5e9; padding:15px; border-radius:10px;'>
        <h3>Результат расчета:</h3>
        <p>1. <b>угол:</b> {int(best_match['b'])}x{int(best_match['d'])}</p>
        <p>2. <b>As:</b> {As:.2f} см²</p>
        <p>3. <b>ix:</b> {ix:.2f} см</p>
        <p>4. <b>iy:</b> {iy:.2f} см</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Проверка
    sigma = N / (0.6 * (2 * As) * Yy) # Упрощенная проверка
    st.write(f"Проверка: σ = {sigma:.2f} кН/см²")
