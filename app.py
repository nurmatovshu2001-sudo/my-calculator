import streamlit as st
import pandas as pd
import io

# Настраиваем мобильный интерфейс
st.set_page_config(
    page_title="Расчет стержня фермы", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem !important; padding-bottom: 1.5rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }
    div.stButton > button:first-child { width: 100% !important; height: 3.5rem !important; font-size: 1.1rem !important; border-radius: 12px !important; margin-top: 15px; }
    .result-card { background-color: #f0f7f4; padding: 18px; border-radius: 12px; border-left: 6px solid #2e7d32; margin-top: 15px; margin-bottom: 15px; }
    .section-divider { border-top: 2px dashed #9ec5fe; margin-top: 30px; margin-bottom: 20px; }
    .selection-box { background-color: #e8f4fd; padding: 15px; border-radius: 12px; border: 1px solid #b3d7ff; margin-bottom: 10px; }
    .selection-title { color: #0056b3; font-weight: bold; font-size: 1.1rem; margin-top: 0; margin-bottom: 10px; }
    @media (prefers-color-scheme: dark) {
        .result-card { background-color: #1b3820; color: #a5d6a7; }
        .section-divider { border-color: #2a4365; }
        .selection-box { background-color: #1a2634; border-color: #2b3e55; }
        .selection-title { color: #63b3ed; }
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏗️ Подбор сортамента фермы")

# =========================================================
# БАЗА ДАННЫХ: КОЭФФИЦИЕНТЫ ФИ И СОРТАМЕНТ ИЗ ТВОИХ ФАЙЛОВ
# =========================================================
raw_phi_data = """λ,200,220,240,245,260,280,300,320,340,360,380,400,440,480,520
1,999,999,999,999,999,999,999,999,999,999,999,999,999,999,999
2,999,999,999,999,999,999,999,999,998,998,998,998,998,998,998
3,998,998,998,998,998,998,997,997,997,997,997,997,997,997,997
4,997,997,997,997,996,996,996,996,996,996,996,995,995,995,995
5,996,996,995,995,995,995,995,994,994,994,994,994,993,993,993
50,883,875,866,864,858,850,842,834,826,818,810,801,784,767,750
60,844,834,823,820,812,801,791,780,770,759,748,737,715,693,670
70,801,789,776,773,763,750,736,723,709,695,682,668,641,614,587
80,754,739,724,720,709,693,677,661,645,629,613,597,566,535,504
90,702,686,669,665,652,634,616,598,581,563,546,529,495,462,430
100,648,630,612,607,593,574,555,536,518,500,482,464,430,398,368
110,593,574,555,550,536,516,497,478,460,443,425,409,376,346,319
120,539,520,501,496,482,463,444,425,408,391,375,360,330,303,279
130,488,469,451,446,432,414,396,379,363,348,333,319,292,268,247
140,441,423,405,401,387,370,353,338,323,310,297,285,261,240,221
150,399,382,365,361,348,332,317,303,290,278,266,255,235,216,199"""

df_phi = pd.read_csv(io.StringIO(raw_phi_data.strip()), index_col=0)
df_phi.index = df_phi.index.astype(int)
df_phi.columns = df_phi.columns.astype(int)

sortament_data = [
    {"b": 45, "d": 4, "F": 3.48, "rx": 1.38, "ry_8": 2.24, "ry_10": 2.16, "ry_12": 2.32, "ry_14": 2.40},
    {"b": 45, "d": 5, "F": 4.29, "rx": 1.37, "ry_8": 2.26, "ry_10": 2.18, "ry_12": 2.34, "ry_14": 2.42},
    {"b": 50, "d": 4, "F": 3.89, "rx": 1.54, "ry_8": 2.35, "ry_10": 2.43, "ry_12": 2.51, "ry_14": 2.59},
    {"b": 50, "d": 5, "F": 4.80, "rx": 1.53, "ry_8": 2.45, "ry_10": 2.38, "ry_12": 2.53, "ry_14": 2.61},
    {"b": 56, "d": 4, "F": 4.38, "rx": 1.73, "ry_8": 2.66, "ry_10": 2.58, "ry_12": 2.73, "ry_14": 2.81},
    {"b": 56, "d": 5, "F": 5.41, "rx": 1.72, "ry_8": 2.61, "ry_10": 2.72, "ry_12": 2.77, "ry_14": 2.85},
    {"b": 63, "d": 5, "F": 6.13, "rx": 1.94, "ry_8": 2.92, "ry_10": 2.98, "ry_12": 3.04, "ry_14": 3.11},
    {"b": 63, "d": 6, "F": 7.28, "rx": 1.93, "ry_8": 2.95, "ry_10": 3.01, "ry_12": 3.07, "ry_14": 3.14},
    {"b": 70, "d": 5, "F": 6.86, "rx": 2.16, "ry_8": 3.23, "ry_10": 3.29, "ry_12": 3.35, "ry_14": 3.42},
    {"b": 70, "d": 6, "F": 8.15, "rx": 2.15, "ry_8": 3.26, "ry_10": 3.32, "ry_12": 3.38, "ry_14": 3.45},
    {"b": 75, "d": 5, "F": 7.39, "rx": 2.32, "ry_8": 3.45, "ry_10": 3.51, "ry_12": 3.57, "ry_14": 3.64},
    {"b": 75, "d": 6, "F": 8.78, "rx": 2.31, "ry_8": 3.48, "ry_10": 3.54, "ry_12": 3.60, "ry_14": 3.67},
    {"b": 75, "d": 8, "F": 11.50, "rx": 2.29, "ry_8": 3.54, "ry_10": 3.60, "ry_12": 3.66, "ry_14": 3.73},
    {"b": 80, "d": 6, "F": 9.38, "rx": 2.47, "ry_8": 3.70, "ry_10": 3.76, "ry_12": 3.82, "ry_14": 3.89},
    {"b": 80, "d": 8, "F": 12.30, "rx": 2.44, "ry_8": 3.76, "ry_10": 3.82, "ry_12": 3.88, "ry_14": 3.95},
    {"b": 90, "d": 6, "F": 10.60, "rx": 2.78, "ry_8": 4.14, "ry_10": 4.20, "ry_12": 4.26, "ry_14": 4.33},
    {"b": 90, "d": 7, "F": 12.30, "rx": 2.77, "ry_8": 4.17, "ry_10": 4.23, "ry_12": 4.29, "ry_14": 4.36},
    {"b": 90, "d": 8, "F": 13.90, "rx": 2.76, "ry_8": 4.20, "ry_10": 4.26, "ry_12": 4.32, "ry_14": 4.39},
    {"b": 100, "d": 7, "F": 13.80, "rx": 3.09, "ry_8": 4.61, "ry_10": 4.67, "ry_12": 4.73, "ry_14": 4.80},
    {"b": 100, "d": 8, "F": 15.60, "rx": 3.08, "ry_8": 4.64, "ry_10": 4.70, "ry_12": 4.76, "ry_14": 4.83},
    {"b": 100, "d": 10, "F": 19.20, "rx": 3.05, "ry_8": 4.70, "ry_10": 4.76, "ry_12": 4.82, "ry_14": 4.89},
    {"b": 125, "d": 8, "F": 19.70, "rx": 3.87, "ry_8": 5.74, "ry_10": 5.80, "ry_12": 5.86, "ry_14": 5.93},
    {"b": 125, "d": 10, "F": 24.30, "rx": 3.84, "ry_8": 5.80, "ry_10": 5.86, "ry_12": 5.92, "ry_14": 5.99},
    {"b": 125, "d": 12, "F": 28.90, "rx": 3.81, "ry_8": 5.86, "ry_10": 5.92, "ry_12": 5.98, "ry_14": 6.05}
]

df_sort = pd.DataFrame(sortament_data)

# =========================================================
# БЛОК 1: ДАННЫЕ ИЗ УСЛОВИЯ ЗАДАЧИ
# =========================================================
st.subheader("📋 Данные из условия задачи")

N = st.number_input("Продольное усилие N (кН):", value=560.0, step=10.0)
R = st.number_input("Расчетное сопротивление R (кН/см²):", value=38.0, step=1.0)
L = st.number_input("Геометрическая длина стержня L (м):", value=1.5, step=0.1)

col1, col2 = st.columns(2)
with col1: 
    Yx = st.number_input("Коэффициент расчетной длины Yx:", value=0.9, step=0.1)
with col2: 
    Yy = st.number_input("Коэффициент расчетной длины Yy:", value=0.9, step=0.1)

# =========================================================
# РАЗДЕЛИТЕЛЬ И БЛОК 2: ДЛЯ САМОСТОЯТЕЛЬНОГО ВЫБОРА (В САМОМ НИЗУ)
# =========================================================
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Оборачиваем нижние поля в красивый синий блок, чтобы отделить от задачи
st.markdown('<div class="selection-box">', unsafe_allow_html=True)
st.markdown('<p class="selection-title">⚙️ Выбери параметры для расчета самостоятельно:</p>', unsafe_allow_html=True)

lambda_start = st.number_input("Начальная гибкость λ:", value=100, step=1)
t_фасонки = st.selectbox("Толщина фасонки t (мм):", options=[8, 10, 12, 14], index=1)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# РАСЧЕТ И АВТОПОДБОР СОРТАМЕНТА
# =========================================================
ry_mpa = int(R * 10)
closest_col = min(df_phi.columns, key=lambda x: abs(x - ry_mpa))
closest_row = min(df_phi.index, key=lambda x: abs(x - lambda_start))

try:
    phi = int(df_phi.loc[closest_row, closest_col]) / 1000
except Exception:
    phi = 0.593

A_tr = (N * Yx) / (phi * R * Yy)
A_one_tr = A_tr / 2

if st.button("🚀 Выполнить автоматический подбор сечения", type="primary"):
    st.write("---")
    st.write("### Результат расчёта:")
    st.write(f"При заданных $\lambda = {lambda_start}$ и $R_y = {ry_mpa}$ МПа найден $\phi = {phi:.3f}$")
    st.write(f"Требуемая площадь одного уголка: $A_{{1,тр}} = {A_one_tr:.2f}$ см²")
    
    # Имя колонки с нужным iy в зависимости от выбранной фасонки t
    ry_col_name = f"ry_{t_фасонки}"
    
    # Ищем уголки, площадь которых больше или равна требуемой
    df_filtered = df_sort[df_sort["F"] >= A_one_tr]
        
    if not df_filtered.empty:
        # Берем самый ближайший по площади уголок (минимальный перерасход металла)
        best_match = df_filtered.sort_values(by="F").iloc[0]
        
        уголок_name = f"{int(best_match['b'])}x{int(best_match['d'])}"
        As = best_match['F']
        ix = best_match['rx']
        iy = best_match[ry_col_name]
        
        запас_площади = ((As - A_one_tr) / A_one_tr) * 100
        
        # Вывод строго по твоей форме
        st.markdown(f"""
        <div class="result-card">
            <h3 style='margin-top:0; color:#1b5e20;'>Принятый сортамент:</h3>
            <p style='font-size:1.2rem; margin-bottom:8px;'>1. <b>угол:</b> BxD = ∟ {уголок_name}</p>
            <p style='font-size:1.2rem; margin-bottom:8px;'>2. <b>As:</b> {As:.2f} см²</p>
            <p style='font-size:1.2rem; margin-bottom:8px;'>3. <b>ix:</b> {ix:.2f} см</p>
            <p style='font-size:1.2rem; margin-bottom:8px;'>4. <b>iy:</b> {iy:.2f} см</p>
            <hr style='border: 0; border-top: 1px solid #c3e6cb; margin: 10px 0;'>
            <span style='font-size:0.9rem; color:#555;'>Уголок выбран с минимальным запасом площади (+{запас_площади:.1f}%). Значение <b>iy</b> автоматически определено по твоей фасонке t = {t_фасонки} мм.</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Второе приближение
        Lef_x = (L * 100) * Yx
        Lef_y = (L * 100) * Yy
        
        lambda_x_fact = Lef_x / ix
        lambda_y_fact = Lef_y / iy
        lambda_max_fact = max(lambda_x_fact, lambda_y_fact)
        
        closest_row_2 = min(df_phi.index, key=lambda x: abs(x - int(round(lambda_max_fact))))
        phi_fact = int(df_phi.loc[closest_row_2, closest_col]) / 1000
        
        sigma = N / (phi_fact * (As * 2))
        
        st.write("### Проверка устойчивости (2-е приближение):")
        st.latex(r"\lambda_{max} = \max\left(" + f"{lambda_x_fact:.1f}, {lambda_y_fact:.1f}" + r"\right) = " + f"{lambda_max_fact:.1f}")
        st.write(f"По таблице для новой гибкости $\lambda = {closest_row_2}$ найден коэффициент $\phi_{{факт}} = {phi_fact:.3f}$")
        
        if sigma <= R:
            st.success(f"✅ Проверка пройдена! Напряжение σ = {sigma*10:.1f} МПа ≤ Ry = {R*10:.0f} МПа.")
        else:
            st.error(f"❌ Перенапряжение! σ = {sigma*10:.1f} МПа > Ry = {R*10:.0f} МПа. Рекомендуется вручную взять калибр больше.")
            
    else:
        st.warning("⚠️ В базе данных задачника не найдено уголков с такой большой площадью. Проверь усилия N.")
