import streamlit as st
import pandas as pd
import os

# Фиксированные параметры (стандартные для студенческих задач)
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
    R_val = st.selectbox("Ry (МПа):", [200, 220, 240
