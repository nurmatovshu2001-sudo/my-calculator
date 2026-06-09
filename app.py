import streamlit as st
import pandas as pd

# 1. ЗАГРУЗКА ДАННЫХ
@st.cache_data
def load_data():
    df_sort = pd.read_csv('sortament.csv', header=1)
    df_sort.columns = [c.strip() for c in df_sort.columns]
    df_phi = pd.read_csv('phi.csv', header=1)
    df_phi = df_phi.set_index(df_phi.columns[0])
    return df_sort, df_phi

df_sort, df_phi = load_data()

st.title("🏗️ Профессиональный расчет")
N = st.number_input("N (кН):", value=680.0)
R_val = st.selectbox("Ry (МПа):", [200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 440, 480, 520])
L = st.number_input("L (см):", value=150.0)
T = st.selectbox("Фасонка (мм):", [8, 10, 12, 14])
lam1 = st.number_input("λ1:", value=70)

if st.button("Рассчитать"):
    try:
        R_knsm2 = R_val / 10
        col_ry = str(R_val)
        phi1 = df_phi.loc[lam1, col_ry] / 1000
        
        # Атр (деление на 2)
        A_tr = (N * 0.95) / (phi1 * R_knsm2 * 0.95)
        A_half = A_tr / 2
        
        # Подбор
        best = df_sort[df_sort['As'] >= A_half].iloc[0]
        iy = best[f'iy_{T}']
        
        # Гибкость и уточнение фи
        lam2 = int(max((L * 0.95) / best['ix, см'], (L * 0.95) / iy))
        phi2 = df_phi.loc[lam2, col_ry] / 1000
        
        # Напряжение
        sigma = (N * 0.95) / (2 * best['As'] * phi2 * 0.95)
        
        # ФИНАЛЬНЫЙ РАСЧЕТ ЗАПАСА
        reserve = ((R_knsm2 - sigma) / R_knsm2) * 100
        
        st.write(f"### Выбран: {best['b']}x{best['d']}")
        st.write(f"Напряжение σ: {sigma:.2f} кН/см²")
        st.write(f"**Запас прочности: {reserve:.1f}%**")
        
        if sigma <= R_knsm2:
            st.success("✅ Проходит")
        else:
            st.error("❌ Не проходит")
            
    except Exception as e:
        st.error(f"Ошибка: {e}")
