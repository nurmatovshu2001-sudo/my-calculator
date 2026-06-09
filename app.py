# ... (код выше остается прежним)

if st.button("🚀 Выполнить автоматический подбор сечения", type="primary"):
    st.write("---")
    st.write("### Ход решения:")
    st.write(f"1. При начальной гибкости $\lambda = {lambda_start}$ и $R_y = {ry_mpa}$ МПа определен коэф. $\phi = {phi:.3f}$")
    st.write(f"2. Требуемая общая площадь сечения: $A_{{тр}} = {A_tr:.2f}$ см²")
    st.write(f"3. Требуемая площадь одного уголка: $A_{{s,тр}} = {A_one_tr:.2f}$ см²")
    
    # Имя колонки для определения iy в зависимости от t (дельта = t)
    ry_col_name = f"ry_{t_фасонки}"
    
    # Ищем все уголки, где площадь F больше или равна требуемой
    df_filtered = df_sort[df_sort["F"] >= A_one_tr]
        
    if not df_filtered.empty:
        # Выбираем самый оптимальный
        best_match = df_filtered.sort_values(by="F").iloc[0]
        
        b_val = int(best_match['b'])
        d_val = int(best_match['d'])
        As = best_match['F'] # Теперь это наше As
        ix = best_match['rx']
        iy = best_match[ry_col_name]
        
        # Вывод строго по твоей форме
        st.markdown(f"""
        <div class="result-card">
            <h3 style='margin-top:0; color:#1b5e20;'>Результат расчета:</h3>
            <p style='font-size:1.15rem; margin-bottom:6px;'>1. <b>угол:</b> BxD = ∟ {b_val}x{d_val}</p>
            <p style='font-size:1.15rem; margin-bottom:6px;'>2. <b>As:</b> {As:.2f} см²</p>
            <p style='font-size:1.15rem; margin-bottom:6px;'>3. <b>ix:</b> {ix:.2f} см</p>
            <p style='font-size:1.15rem; margin-bottom:12px;'>4. <b>iy:</b> {iy:.2f} см</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Второе приближение (Проверка устойчивости)
        Lef_x = (L * 100) * Yx
        Lef_y = (L * 100) * Yy
        
        lambda_x_fact = Lef_x / ix
        lambda_y_fact = Lef_y / iy
        lambda_max_fact = max(lambda_x_fact, lambda_y_fact)
        
        closest_row_2 = min(df_phi.index, key=lambda x: abs(x - int(round(lambda_max_fact))))
        phi_fact = int(df_phi.loc[closest_row_2, closest_col]) / 1000
        
        # Итоговая проверка (пункт 8 из рукописного решения)
        # sigma = N / (phi * 2As * Yy)
        sigma = N / (phi_fact * (2 * As) * Yy)
        
        st.write("### Проверка устойчивости (2-е приближение):")
        st.latex(r"\sigma = \frac{N \cdot \gamma_n}{2 \cdot A_s \cdot \phi \cdot \gamma_c} = \frac{" + f"{N}" + r"}{2 \cdot " + f"{As}" + r" \cdot " + f"{phi_fact}" + r" \cdot " + f"{Yy}" + r"} = " + f"{sigma:.2f}" + r" \text{ кН/см}^2")
        
        if sigma <= R:
            st.success(f"✅ Проверка пройдена! σ = {sigma:.2f} кН/см² ≤ R = {R:.1f} кН/см².")
        else:
            st.error(f"❌ Перенапряжение! σ = {sigma:.2f} кН/см² > R = {R:.1f} кН/см².")
