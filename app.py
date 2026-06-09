import streamlit as st
import pandas as pd

# 1. ЗАГРУЗКА ТВОИХ ДАННЫХ
df_phi = pd.read_csv('Копия_ Задачник - лол – 7 июня, 23_07 (1).xlsx - коэф.csv').set_index('Гибкость λ')
df_sort = pd.read_csv('Копия_ Задачник - лол – 7 июня, 23_07 (1).xlsx - сортамент.csv')

# 2. ИНТЕРФЕЙС
st.title("🏗️ Профессиональный расчет фермы")
N = st.number_input("Усилие N (кН):", value=876.0)
R_val = st.selectbox("Ry (МПа):", [200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 440, 480, 520])
L = st.number_input("Длина стержня l (м):", value=3.2)
T = st.selectbox("Толщина фасонки (мм):", [8, 10, 12, 14])
lam1 = st.number_input("λ1:", value=70)

if st.button("🚀 Выполнить точный расчет"):
    # Логика поиска Phi из твоей таблицы
    col_name = str(R_val)
    phi1 = df_phi.loc[lam1, col_name] / 1000
    
    # Расчет Атр (перевод Ry в кН/см2 = МПа/10)
    R_knsm2 = R_val / 10
    A_tr = (N * 0.9) / (phi1 * R_knsm2 * 0.9)
    A_half = A_tr / 2
    
    # Подбор из твоего сортамента
    # Фильтруем таблицу по площади
    suitable = df_sort[df_sort['As'] >= A_half]
    best = suitable.iloc[0]
    
    # Берем iy динамически (названия колонок в CSV: iy_8, iy_10 и т.д.)
    iy = best[f'iy_{T}']
    
    # Расчет гибкостей
    lam_x = (L * 100 * 0.9) / best['ix, см']
    lam_y = (L * 100 * 0.9) / iy
    lam2 = int(max(lam_x, lam_y))
    
    # Уточненный Phi2
    phi2 = df_phi.loc[lam2, col_name] / 1000
    
    # Проверка
    sigma = (N * 0.9) / (2 * best['As'] * phi2 * 0.9)
    
    st.write("---")
    st.write(f"### Выбран уголок: {best['b']}x{best['d']}")
    st.write(f"**Атр**: {A_tr:.2f} см²")
    st.write(f"**λ2**: {lam2} (φ2 = {phi2:.3f})")
    st.write(f"**Напряжение σ**: {sigma:.2f} кН/см²")
    
    if sigma <= R_knsm2:
        st.success("✅ Проходит")
    else:
        st.error("❌ Не проходит")
