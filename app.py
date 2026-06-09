import streamlit as st
import pandas as pd
import io

# --- БАЗА ДАННЫХ ИЗ ВАШЕГО PDF ---
# Данные строго по ГОСТ 8509-72 из предоставленного файла
sortament_data = [
    # b*d, F, ix, iy_8, iy_10, iy_12, iy_14
    {"b": 45, "d": 4, "F": 3.48, "ix": 1.38, "iy_8": 2.24, "iy_10": 2.16, "iy_12": 2.32, "iy_14": 2.40},
    {"b": 45, "d": 5, "F": 4.29, "ix": 1.37, "iy_8": 2.26, "iy_10": 2.18, "iy_12": 2.34, "iy_14": 2.42},
    {"b": 50, "d": 4, "F": 3.89, "ix": 1.54, "iy_8": 2.35, "iy_10": 2.43, "iy_12": 2.51, "iy_14": 2.59},
    # Добавьте сюда остальные строки из вашей таблицы...
]
df_sort = pd.DataFrame(sortament_data)

# --- ЛОГИКА ПОДБОРА ---
def get_angle_data(A_needed, t_fas):
    # Фильтруем таблицу: выбираем уголки с площадью >= A_needed
    df_filtered = df_sort[df_sort["F"] >= A_needed]
    if not df_filtered.empty:
        best = df_filtered.iloc[0] # Берем первый подходящий
        iy_col = f"iy_{t_fas}"
        return best['b'], best['d'], best['F'], best['ix'], best[iy_col]
    return None, None, None, None, None

# --- ВЫВОД РЕЗУЛЬТАТА (по пунктам 1-7) ---
if st.button("🚀 Выполнить расчет"):
    # ... расчеты phi1, A_tr, A_half ...
    
    # ПОДБОР ПО ВАШЕЙ ТАБЛИЦЕ
    b, d, As, ix, iy = get_angle_data(A_half, t_фас)
    
    if As:
        st.markdown(f"""
        1. **Aтр** = {A_tr:.2f} см²
        2. **Aтр/2** = {A_half:.2f} см²
        3. **∟** = {int(b)}x{int(d)}
           **As** = {As:.2f} см²
           **ix** = {ix:.2f} см
           **iy** = {iy:.2f} см
        4. **λx** = {(L*100*Yx)/ix:.1f}
           **λy** = {(L*100*Yy)/iy:.1f}
        5. **λ2** = {round(max((L*100*Yx)/ix, (L*100*Yy)/iy))}
        6. **σ** = {(N*Yx)/(2*As*phi2*Yy):.2f} <= {R}
        7. **(R-σ)/R * 100%** = {((R-sigma)/R)*100:.1f}%
        """)
    else:
        st.error("В таблице не найдено сечение с такой площадью.")
