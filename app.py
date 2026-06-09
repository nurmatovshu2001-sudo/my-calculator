import streamlit as st
import pandas as pd
import os

# 1. Загрузка данных
@st.cache_data
def load_data():
    if not os.path.exists('sortament.csv') or not os.path.exists('phi.csv'):
        return None, None
    df_sort = pd.read_csv('sortament.csv', sep=';', header=2, encoding='cp1251')
    df_sort.columns = [c.strip() for c in df_sort.columns]
    df_phi = pd.read_csv('phi.csv', sep=';', encoding='cp1251')
    df_phi = df_phi.set_index(df_phi.columns[0])
    return df_sort, df_phi

df_sort, df_phi = load_data()

st.title("🏗️ Расчет сжатого стержня")

if df_sort is None:
    st.error("Файлы sortament.csv или phi.csv не найдены!")
else:
    # Ввод параметров студентом
    N = st.number_input("Усилие N (кН):", value=680.0)
    R_val = st.selectbox("Ry (МПа):", [200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400])
    L = st.number_input("Длина L (см):", value=150.0)
    T = st.selectbox("Фасонка t (мм):", [8, 10, 12, 14])
    Ys = st.number_input("Коэф. Ys:", value=0.95)
    Yy = st.number_input("Коэф. Yy:", value=0.95)

    if st.button("Рассчитать"):
        try:
            R_knsm2 = R_val / 10
            # Предварительный подбор
            phi_pre = df_phi.loc[70, R_val] / 1000
            A_tr = (N * Ys) / (phi_pre * R_knsm2 * Yy)
            A_half = A_tr / 2
            
            # Поиск уголка
            best = df_sort[df_sort['As'] >= A_half].iloc[0]
            ix = best['ix, см']
            iy = best[f'iy_{T}']
            
            # Проверка гибкости
            lam_max = int(max((L * Ys) / ix, (L * Ys) / iy))
            
            # Уточнение фи
            phi2 = df_phi.loc[lam_max, R_val] / 1000
            sigma = (N * Ys) / (2 * best['As'] * phi2 * Yy)
            
            # Расчет запаса (Дельта)
            reserve = ((R_knsm2 - sigma) / R_knsm2) * 100
            
            st.subheader(f"Выбран уголок: {best['b']}x{best['d']}")
            st.write(f"Напряжение σ: {sigma:.2f} кН/см²")
            st.write(f"Запас прочности (Дельта): **{reserve:.2f}%**")
            
            if 0 <= reserve <= 5:
                st.success("✅ Идеально (запас менее 5%)!")
            elif reserve < 0:
                st.error("❌ Сечение не проходит!")
            else:
                st.warning("⚠️ Большой запас прочности.")
                
        except Exception as e:
            st.error(f"Ошибка: {e}")
