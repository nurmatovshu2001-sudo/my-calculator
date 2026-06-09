import streamlit as st
import pandas as pd
import os

# Фиксированные параметры
L_CONST = 150.0
T_CONST = 12
YC_CONST = 0.95

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
    st.error("Файлы данных не найдены!")
else:
    # Пользователь вводит ТОЛЬКО N и R
    N = st.number_input("Усилие N (кН):", value=980.0)
    R_val = st.selectbox("Ry (МПа):", [200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400])

    if st.button("Рассчитать"):
        try:
            R_knsm2 = R_val / 10
            # Предварительный подбор (lambda=70)
            phi_pre = df_phi.loc[70, R_val] / 1000
            A_tr = (N * YC_CONST) / (phi_pre * R_knsm2 * YC_CONST)
            A_half = A_tr / 2
            
            # Поиск уголка
            best = df_sort[df_sort['As'] >= A_half].iloc[0]
            ix = best['ix, см']
            iy = best[f'iy_{T_CONST}']
            
            # Проверка гибкости
            lam_x = (L_CONST * YC_CONST) / ix
            lam_y = (L_CONST * YC_CONST) / iy
            lam_max = int(max(lam_x, lam_y))
            
            # Уточнение фи
            phi2 = df_phi.loc[lam_max, R_val] / 1000
            sigma = (N * YC_CONST) / (2 * best['As'] * phi2 * YC_CONST)
            
            # Расчет запаса
            reserve = ((R_knsm2 - sigma) / R_knsm2) * 100
            
            st.subheader(f"Результат: Уголок {best['b']}x{best['d']}")
            st.write(f"Напряжение σ: {sigma:.2f} кН/см²")
            st.write(f"Запас прочности: **{reserve:.2f}%**")
            
            if 0 <= reserve <= 5:
                st.success("✅ Идеально (запас менее 5%)!")
            elif reserve > 5:
                st.warning("⚠️ Большой запас, можно взять уголок меньше.")
            else:
                st.error("❌ Не проходит (перегруз)!")
        except Exception as e:
            st.error(f"Ошибка в расчете: {e}")
