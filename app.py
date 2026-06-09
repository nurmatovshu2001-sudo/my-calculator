import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Авто-Расчет Фермы", layout="centered")

# --- БАЗА ДАННЫХ (ФИ и Сортамент) ---
raw_phi = """λ,200,220,240,260,280,300,320,340,360,380,400
70,801,789,776,763,750,736,723,709,695,682,668
80,754,739,724,709,693,677,661,645,629,613,597
90,702,686,669,652,634,616,598,581,563,546,529
100,648,630,612,593,574,555,536,518,500,482,464"""
df_phi = pd.read_csv(io.StringIO(raw_phi)).set_index("λ")

sortament = pd.DataFrame([
    {"b": 125, "d": 9, "F": 22.0, "rx": 3.86, "ry_8": 5.48, "ry_10": 5.41, "ry_12": 5.56, "ry_14": 5.63},
    {"b": 125, "d": 8, "F": 19.7, "rx": 3.87, "ry_8": 5.46, "ry_10": 5.39, "ry_12": 5.53, "ry_14": 5.60}
])

def get_phi(lam, r_val):
    col = min(df_phi.columns.astype(int), key=lambda x: abs(x - r_val * 10))
    row = min(df_phi.index, key=lambda x: abs(x - int(lam)))
    return df_phi.loc[row, str(col)] / 1000

# --- ИНТЕРФЕЙС ---
st.title("🏗️ Авто-Расчет Стержня")
N = st.number_input("N (кН):", value=876.0)
R = st.number_input("R (кН/см²):", value=30.0)
L = st.number_input("L (м):", value=3.2)
Yx = st.number_input("Yx:", value=0.9)
Yy = st.number_input("Yy:", value=0.9)
t_фас = st.selectbox("Толщина фасонки (мм):", [8, 10, 12, 14])
lam1 = st.number_input("λ1 (начальная):", value=70)

if st.button("🚀 Рассчитать решение"):
    # 1. Авто-вычисление фи1
    phi1 = get_phi(lam1, R)
    A_tr = (N * Yx) / (phi1 * R * Yy)
    A_half = A_tr / 2
    
    # 3. Авто-подбор уголка
    best = sortament[sortament["F"] >= A_half].iloc[0]
    As, ix = best["F"], best["rx"]
    iy = best[f"ry_{t_фас}"]
    
    # 4-5. Фактическая λ2 и фи2
    lx = (L * 100) * Yx / ix
    ly = (L * 100) * Yy / iy
    lam2 = round(max(lx, ly))
    phi2 = get_phi(lam2, R)
    
    # 6. σ
    sigma = (N * Yx) / (2 * As * phi2 * Yy)
    diff = (R - sigma) / R * 100
    
    # ВЫВОД
    st.markdown(f"**λ1 = {lam1} ; φ1 = {phi1:.3f}**")
    st.markdown(f"""
    1. **Атр** = {A_tr:.2f} см²
    2. **Атр/2** = {A_half:.2f} см²
    3. **∟** = {best['b']}x{best['d']} | **As** = {As} см² | **ix** = {ix} см | **iy** = {iy} см
    4. **λx** = {lx:.1f} ; **λy** = {ly:.1f}
    5. **λ2** = {lam2}
    6. **σ** = {sigma:.2f} ≤ {R}
    7. **(R-σ)/R * 100%** = {diff:.1f}%
    """)
    
    if sigma <= R: st.success("✅ Проверка пройдена!")
    else: st.error("❌ Сечение слабое!")
