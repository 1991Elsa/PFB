nasdaq_tickers_historic["Date"] = pd.to_datetime(nasdaq_tickers_historic["Date"])
    ultima_fecha = nasdaq_tickers_historic["Date"].max()

    fecha_hace_1_dia= ultima_fecha - pd.Timedelta(days=1)
    fecha_hace_7_dias = ultima_fecha - pd.Timedelta(days=7)
    fecha_hace_1_mes = ultima_fecha - pd.Timedelta(days=30)
    fecha_hace_1_anyo = ultima_fecha - pd.Timedelta(days=365)


    df_ticker = nasdaq_tickers_historic[nasdaq_tickers_historic["Ticker"] == selected_ticker]
    precio_fin = df_ticker[df_ticker["Date"] == ultima_fecha]["Close"].values
    precio_1_dia = df_ticker[df_ticker["Date"] == fecha_hace_1_dia]["Close"].values
    precio_7_dias = df_ticker[df_ticker["Date"] == fecha_hace_7_dias]["Close"].values
    precio_1_mes = df_ticker[df_ticker["Date"] == fecha_hace_1_mes]["Close"].values
    precio_1_anyo= df_ticker[df_ticker["Date"] == fecha_hace_1_anyo]["Close"].values
    

    variacion_1_dia = ((precio_fin - precio_1_dia) / precio_1_dia) * 100
    variacion_7_dias = ((precio_fin - precio_7_dias) / precio_7_dias) * 100
    variacion_1_mes = ((precio_fin - precio_1_mes) / precio_1_mes) * 100
    variacion_1_anyo = ((precio_fin - precio_1_anyo) / precio_1_anyo) * 100
    
    st.subheader("Evolución de los últimos días")
    evo_col1, evo_col2, evo_col3, evo_col4, evo_col5, evo_col6 = st.columns(6)
    with evo_col1:
        if variacion_1_dia[0] > 0:
            st.success(f"24h:{variacion_1_dia[0]:.2f} %")
        elif variacion_1_dia[0] < 0:
            st.error(f"24h: {variacion_1_dia[0]:.2f} %")
        else:
            st.warning(f"24h: {variacion_1_dia[0]:.2f} %")
        
    
    with evo_col2:
        if variacion_7_dias[0] > 0:
            st.success(f"7 dias:{variacion_7_dias[0]:.2f} %")
        elif variacion_7_dias[0] < 0:
            st.error(f"7 dias: {variacion_7_dias[0]:.2f} %")
        else:
            st.warning(f"7 dias: {variacion_7_dias[0]:.2f} %")
        

    with evo_col3:
        if variacion_1_mes[0] > 0:
            st.success(f"1 mes: {variacion_1_mes[0]:.2f} %")
        elif variacion_1_mes[0] < 0:
            st.error(f"1 mes: {variacion_1_mes[0]:.2f} %")
        else:
            st.warning(f"1 mes: {variacion_1_mes[0]:.2f} %")

        

    with evo_col4:
        if variacion_1_anyo[0] > 0:
            st.success(f"1 año:{variacion_1_anyo[0]:.2f} %")
        elif variacion_1_anyo[0] < 0:
            st.error(f"1 año: {variacion_1_anyo[0]:.2f} %")
        else:
            st.warning(f"1 año: {variacion_1_anyo[0]:.2f} %")
        

   