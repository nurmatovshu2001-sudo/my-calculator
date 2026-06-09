import streamlit as st
import pandas as pd

# 1. КОНФИГУРАЦИЯ
st.set_page_config(page_title="Инженерный калькулятор фермы", layout="centered")

# 2. БАЗА ДАННЫХ (Расширяй этот список данными из своего PDF)
# iy_N — радиус инерции при толщине фасонки N мм
SORTAMENT = [
    {"b": 45, "d": 4, "A": 3.48, "ix": 1.38, "iy_8": 2.24, "iy_10": 2.16, "iy_12": 2.32, "iy_14": 2.40},
    {"b": 50, "d": 4, "A": 3.89, "ix": 1.54, "iy_8": 2.35, "iy_10": 2.43, "iy_12": 2.51, "iy_14": 2.59},
    {"b": 63, "d": 5, "A": 6.13, "ix": 1.94, "iy_8": 2.92, "iy_10": 2.98, "iy_12": 3.04, "iy_14": 3.11},
    {"b": 125, "d": 9, "A": 22.0, "ix": 3.86, "iy_8": 5.48, "iy_10": 5.41, "iy_12": 5.56, "iy_14": 5.63}
]
df = pd.DataFrame(SORTAMENT)

# 3. ИНТЕРФЕЙС
st.title("🏗️ Расчет сжатого стержня фермы")
col1, col2 = st.columns(2)
with col1:
    N = st.number_input("N (кН):", value=876.0)
    R = st.number_input("R (кН/см²):", value=23.0) # Сталь С235
    L = st.number_input("l (м):", value=3.2)
    lam1 = st.number_input("λ1 (для подбора):", value=70.0)
with col2:
    Yx = st.number_input("Yx:", value=0.9)
    Yy = st.number_input("Yy:", value=0.9)
    T = st.selectbox("Толщина фасонки (мм):", [8, 10, 12, 14])

# 4. ЛОГИКА РАСЧЕТА
if st.button("🚀 Выполнить расчет"):
    try:
        # П1-2: Расчет требуемой площади
        # Заглушка phi1 (в реальности заменить на функцию поиска по таблице)
        phi1 = 0.705 
        A_tr = (N * Yx) / (phi1 * R * Yy)
        A_half = A_tr / 2
        
        # П3: Подбор сечения
        best = df[df["A"] >= A_half].iloc[0]
        
        # Динамический выбор iy в зависимости от фасонки
        iy_col = f"iy_{T}"
        iy = best[iy_col]
        ix = best["ix"]
        A_s = best["A"]
        
        # П4-5: Гибкость
        lam_x = (L * 100 * Yx) / ix
        lam_y = (L * 100 * Yy) / iy
        lam2 = round(max(lam_x, lam_y))
        
        # П6: Проверка напряжений
        # Заглушка phi2
        phi2 = 0.600 
        sigma = (N * Yx) / (2 * A_s * phi2 * Yy)
        
        # П7: Запас
        reserve = ((R - sigma) / R) * 100
        
        # ВЫВОД
        st.subheader("Результаты расчета")
        st.markdown(f"""
        * **1. Атр**: {A_tr:.2f} см²
        * **2. Атр/2**: {A_half:.2f} см²
        * **3. Выбран уголок**: {int(best['b'])}x{int(best['d'])} (As={A_s} см²)
        * **4. Гибкость**: λx={lam_x:.1f}, λy={lam_y:.1f}
        * **5. λ2 (max)**: {lam2}
        * **6. Напряжение σ**: {sigma:.2f} кН/см² (при R={R})
        * **7. Запас прочности**: **{reserve:.1f}%**
        """)
        
        if sigma <= R:
            st.success("✅ Стержень проходит по прочности.")
        else:
            st.error("❌ Стержень не проходит по прочности!")
            
    except Exception as e:
        st.error(f"Ошибка в расчетах: {e}. Проверь параметры сечения!")
