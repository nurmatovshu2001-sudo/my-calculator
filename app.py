import streamlit as st
import pandas as pd

# Блок 1: Чтение и «чистка» данных
@st.cache_data
def load_and_clean_data():
    # Читаем сортамент: пропускаем 2 строки заголовков
    # В твоем файле 2-я строка — это названия: b, d, As, ix, iy_8 и т.д.
    df_sort = pd.read_csv('Копия_ Задачник - лол – 7 июня, 23_07 (1).xlsx - сортамент.csv', header=1)
    
    # Читаем коэффициенты: пропускаем 1 строку
    df_phi = pd.read_csv('Копия_ Задачник - лол – 7 июня, 23_07 (1).xlsx - коэф.csv', header=1)
    df_phi = df_phi.set_index(df_phi.columns[0]) # Делаем первый столбец индексом (Гибкость λ)
    
    return df_sort, df_phi

# Загружаем данные
try:
    df_sort, df_phi = load_and_clean_data()
    st.success("Данные успешно загружены!")
    # Выведем для проверки первые строки (можно будет убрать)
    st.write("Сортамент:", df_sort.head(3))
except Exception as e:
    st.error(f"Ошибка загрузки файлов: {e}")
