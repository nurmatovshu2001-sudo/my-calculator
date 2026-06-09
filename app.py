# 1. Расчет коэффициента ФИ (примерная логика для итерации)
    # Сначала считаем фи1 на основе начальной ламбды
    phi1 = get_phi(lam1, R) 
    
    # 2. ПЕРЕСЧЕТ Атр (ЗДЕСЬ ОН ОБНОВИТСЯ ПРИ СМЕНЕ ЛЮБОГО ВХОДНОГО ПАРАМЕТРА)
    A_tr = (N * Yx) / (phi1 * R * Yy)
    A_half = A_tr / 2
    
    # 3. ПОДБОР УГОЛКА (теперь берет самый свежий A_half)
    # Используем .iloc[0] для выбора первой подходящей строки из PDF-таблицы
    best = df_sort[df_sort["F"] >= A_half].iloc[0]
    
    As = best["F"]
    ix = best["ix"]
    # Вот здесь магия: динамически берем iy для нужной толщины T
    iy = best[f"iy_{T}"]
def get_phi(lam, r_val):
    # Берем данные из таблицы df_phi (которую мы загрузили из строк 1-150)
    # Ищем столбец, ближайший к R*10 (МПа)
    ry_mpa = int(r_val * 10)
    closest_col = min(df_phi.columns, key=lambda x: abs(x - ry_mpa))
    # Ищем строку, ближайшую к текущей lambda
    closest_row = min(df_phi.index, key=lambda x: abs(x - int(lam)))
    return int(df_phi.loc[closest_row, closest_col]) / 1000
    if st.button("🚀 Выполнить расчет сечения", type="primary"):
    # 1. Сначала считаем ФИ для начальной гибкости
    phi1 = get_phi(lam1, R) 
    
    # 2. Теперь Атр пересчитается правильно, так как phi1 берется из таблицы
    A_tr = (N * Yx) / (phi1 * R * Yy)
    A_one = A_tr / 2
    
    # 3. Подбор уголка (программа ищет тот, что больше A_one)
    # Используем .iloc[0] для выбора первой подходящей строки
    best = df_sort[df_sort["F"] >= A_one].iloc[0]
    As = best["F"]
    ix = best["ix"]
    iy = best[f"iy_{T}"] # Здесь T - это толщина из твоего selectbox
    
    # И так далее для λ2, σ, и %.
