import streamlit as st
import pandas as pd
import io

# Настраиваем мобильный интерфейс
st.set_page_config(
    page_title="Расчет стержня фермы", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# ... (CSS стили оставляем как были) ...

st.title("🏗️ Автоматический подбор сортамента фермы")

# 1. Текстовая база данных коэффициентов Фи
raw_phi_data = """λ,200,220,240,245,260,280,300,320,340,360,380,400,440,480,520
70,801,789,776,773,763,750,736,723,709,695,682,668,641,614,587
80,754,739,724,720,709,693,677,661,645,629,613,597,566,535,504
90,702,686,669,665,652,634,616,598,581,563,546,529,495,462,430
100,648,630,612,607,593,574,555,536,518,500,482,464,430,398,368"""

df_phi = pd.read_csv(io.StringIO(raw_phi_data.strip()), index_col=0)

# ... (сортамент как у тебя) ...
sortament_data = [{"b": 125, "d": 8, "F": 19.7, "rx": 3.87, "ry_8": 5.46, "ry_10": 5.39, "ry_12": 5.53, "ry_14": 5.60},
                  {"b": 125, "d": 9, "F": 22.0, "rx": 3.86, "ry_8": 5.48, "ry_10": 5.41, "ry_12": 5.56, "ry_14": 5.63}]
df_sort = pd.DataFrame(sortament_data)

# --- ИНТЕРФЕЙС ---
N = st.number_input("Продольное усилие N (кН):", value=560.0)
R = st.number_input("Расчетное сопротивление R (кН/см²):", value=38.0)
L = st.number_input("Длина L (м):", value=1.5)
Yx = st.number_input("Yx:", value=0.9)
Yy = st.number_input("Yy:", value=0.9)
lambda_start = st.number_input("Начальная гибкость λ:", value=100)
t_фасонки = st.selectbox("Толщина фасонки t (мм):", [8, 10, 12, 14], index=1)

# --- КНОПКА (ВСЯ ЛОГИКА ТУТ) ---
if st.button("🚀 Выполнить автоматический подбор сечения", type="primary"):
    
    # 1. СНАЧАЛА ВЫЧИСЛЯЕМ ФИ (безопасно)
    ry_mpa = int(R * 10)
    try:
        # Ищем ближайший столбец (Ry) и строку (Lambda)
        closest_col = min(df_phi.columns.astype(int), key=lambda x: abs(x - ry_mpa))
        closest_row = min(df_phi.index.astype(int), key=lambda x: abs(x - int(lambda_start)))
        phi = df_phi.loc[closest_row, str(closest_col)] / 1000
        st.write(f"✅ Найдено $\phi = {phi:.3f}$ для $\lambda={closest_row}$")
    except Exception as e:
        phi = 0.593
        st.warning(f"⚠️ Автоматический поиск ФИ не сработал ({e}), использую $\phi=0.593$")

    # 2. РАСЧЕТЫ
    A_tr = (N * Yx) / (phi * R * Yy)
    A_one_tr = A_tr / 2
    
    # 3. ПОДБОР ПО СОРТАМЕНТУ
    df_filtered = df_sort[df_sort["F"] >= A_one_tr]
    
    if not df_filtered.empty:
        best_match = df_filtered.sort_values(by="F").iloc[0]
        st.success(f"Подобрано: ∟{int(best_match['b'])}x{int(best_match['d'])}, As={best_match['F']} см²")
        # ... остальной код проверки устойчивости ...
    else:
        st.error("Не найдено подходящее сечение!")
