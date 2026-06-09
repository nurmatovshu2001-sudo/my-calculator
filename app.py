import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Расчет фермы", layout="centered")

# --- СТИЛИ ---
st.markdown("""
    <style>
    div.stButton > button:first-child { width: 100%; height: 3.5rem; font-size: 1.1rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🏗️ Расчет стержня фермы")

# --- ИСХОДНЫЕ ДАННЫЕ ---
N = st.number_input("Продольное усилие N (кН):", value=876.0)
R = st.number_input("Расчетное сопротивление R (кН/см²):", value=30.0)
L = st.number_input("Геометрическая длина L (м):", value=3.2)
Yx = st.number_input("Коэффициент Yx:", value=0.9, step=0.1)
Yy = st.number_input("Коэффициент Yy:", value=0.9, step=0.1)
lambda_start = st.number_input("Начальная гибкость λ:", value=83)

# --- ТАБЛИЦА ФИ (БЕЗ ИЗМЕНЕНИЙ) ---
raw_table_data = """λ\t200\t220\t240\t260\t280\t300\t320\t340\t360\t380\t400\t440\t480\t520
... (твоя таблица) ...
""" # (Вставь сюда всю таблицу из исходного файла)

# --- ПАРСИНГ ТАБЛИЦЫ ---
df_phi = pd.read_csv(io.StringIO(raw_table_data.strip()), sep="\t", dtype=str)
df_phi.set_index("λ", inplace=True)
for col in df_phi.columns:
    df_phi[col] = df_phi[col].str.replace(r'[^\w]', '', regex=True)
df_phi.index = [int(str(idx).replace('S', '8')) for idx in df_phi.index]
df_phi.columns = [int(col) for col in df_phi.columns]

# --- КНОПКА РАСЧЕТА ---
if st.button("🚀 Выполнить расчет", type="primary"):
    
    # 1. Автоматический поиск ФИ
    ry_mpa = int(R * 10)
    closest_col = min(df_phi.columns, key=lambda x: abs(x - ry_mpa))
    closest_row = min(df_phi.index, key=lambda x: abs(x - int(lambda_start)))
    phi = int(df_phi.loc[closest_row, closest_col].replace('S', '8')) / 1000
    
    # 2. Расчеты
    A_tr = (N * Yx) / (phi * R * Yy)
    A_one = A_tr / 2
    
    # Предположим выбор уголка (здесь твоя логика подбора)
    b, d, As, ix, iy = 125, 9, 22.0, 3.86, 5.48 # Пример данных
    
    lx = (L * 100) / ix
    ly = (L * 100) / iy
    lambda_calc = round(max(lx, ly))
    
    sigma = (N * Yx) / (2 * As * phi * Yy)
    diff = (R - sigma) / R * 100
    
    # 3. ВЫВОД 7 ПУНКТОВ
    st.subheader("Результат решения:")
    st.markdown(f"""
    1. **Aтр** = {A_tr:.2f} см²
    2. **Aтр/2** = {A_one:.2f} см²
    3. **∟** = {b}x{d} <br>
       **As** = {As} см² <br>
       **ix** = {ix} см <br>
       **iy** = {iy} см
    4. **λx** = {lx:.1f}  **λy** = {ly:.1f}
    5. **λ** = {lambda_calc}
    6. **σ** = {sigma:.2f} кН/см²
    7. **(R-σ)/R * 100%** = {diff:.1f}%
    """)
    
    if sigma <= R:
        st.success("✅ Условие σ <= R выполняется")
    else:
        st.error("❌ Условие σ <= R НЕ выполняется!")
