import streamlit as st
import pandas as pd
import io

# --- 1. ДАННЫЕ ИЗ ТВОИХ ТАБЛИЦ (ВШИТЫЕ) ---
# Таблица коэффициентов фи (сокращенно для примера, структура сохранена)
phi_csv = """Гибкость λ,200,220,240,260,280,300,320,340,360,380,400,440,480,520
1,999,999,999,999,999,999,999,999,999,999,999,999,999,999
50,810,810,810,810,810,810,810,810,810,810,810,810,810,810
70,750,750,750,750,750,750,750,750,750,750,750,750,750,750
80,600,600,600,600,600,600,600,600,600,600,600,600,600,600
100,430,430,430,430,430,430,430,430,430,430,430,430,430,430"""

# Сортамент (равнополочные уголки)
sort_csv = """b,d,As,ix,iy_8,iy_10,iy_12,iy_14
45,4,3.48,1.38,2.24,2.16,2.32,2.40
50,4,3.89,1.54,2.35,2.43,2.51,2.59
63,5,6.13,1.94,2.92,2.98,3.04,3.11
125,9,22.0,3.86,5.48,5.41,5.56,5.63"""

df_phi = pd.read_csv(io.StringIO(phi_csv)).set_index('Гибкость λ')
df_sort = pd.read_csv(io.StringIO(sort_csv))

# --- 2. ИНТЕРФЕЙС ---
st.title("🏗️ Расчет сжатого стержня")
N = st.number_input("Усилие N (кН):", value=876.0)
R_val = st.selectbox("Ry (МПа):", [200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 440, 480, 520])
L = st.number_input("Длина стержня l (м):", value=3.2)
T = st.selectbox("Толщина фасонки (мм):", [8, 10, 12, 14])
lam1 = st.number_input("Начальная гибкость λ1:", value=70)

# --- 3. ЛОГИКА ---
if st.button("🚀 Выполнить расчет"):
    try:
        col_ry = str(R_val)
        phi1 = df_phi.loc[min(df_phi.index, key=lambda x: abs(x - lam1)), col_ry] / 1000
        
        R_knsm2 = R_val / 10
        A_tr = (N * 0.9) / (phi1 * R_knsm2 * 0.9)
        best = df_sort[df_sort['As'] >= A_tr/2].iloc[0]
        
        iy = best[f'iy_{T}']
        lam2 = int(max((L * 100 * 0.9) / best['ix'], (L * 100 * 0.9) / iy))
        phi2 = df_phi.loc[min(df_phi.index, key=lambda x: abs(x - lam2)), col_ry] / 1000
        
        sigma = (N * 0.9) / (2 * best['As'] * phi2 * 0.9)
        
        st.write(f"### Выбран уголок: {best['b']}x{best['d']}")
        st.write(f"Атр: {A_tr:.2f} см² | λ2: {lam2} | φ2: {phi2:.3f}")
        st.write(f"Напряжение: {sigma:.2f} кН/см²")
        
        if sigma <= R_knsm2:
            st.success("✅ Прочность обеспечена")
        else:
            st.error("❌ Не проходит")
    except Exception as e:
        st.error(f"Ошибка: {e}")
