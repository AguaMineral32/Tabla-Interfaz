import pandas as pd

def crear_tabla_consultas(archivo):
    try:
        # Lista de columnas a convertir
        consultas = ['NUMERO_PACIENTES_ACTUALES_HOSPITALIZADOS', 'NUMERO_PACIENTES_FALLECIDOS'
                     ,'NUMERO_ATENCIONES_ULTIMO_REPORTE','NUMERO_ATENCIONES_ACUMULADOS']

        # Convertir las columnas a float y reemplazar None o vacío con 0
        archivo[consultas] = archivo[consultas].apply(pd.to_numeric, errors='coerce').fillna(0)

        # Filtrar solo los hospitales (manejo correcto de cadenas)
        df_hospitales = archivo[archivo['NOMBRE_ESTABLECIMIENTO'].str.contains('HOSPITAL', case=False, na=False)]
        df_cesfam = archivo[archivo['NOMBRE_ESTABLECIMIENTO'].str.contains('CENTRO_DE_SALUD_FAMILIAR', case=False, na=False)]
        df_cescof = archivo[archivo['NOMBRE_ESTABLECIMIENTO'].str.contains('CENTRO_COMUNITARIO_DE_SALUD_FAMILIAR', case=False, na=False)]
        df_posta = archivo[archivo['NOMBRE_ESTABLECIMIENTO'].str.contains('POSTA', case=False, na=False)]
        df_sur = archivo[archivo['NOMBRE_ESTABLECIMIENTO'].str.contains('SUR', case=False, na=False)]
        df_sar = archivo[archivo['NOMBRE_ESTABLECIMIENTO'].str.contains('SAR', case=False, na=False)]
        df_sapu = archivo[archivo['NOMBRE_ESTABLECIMIENTO'].str.contains('SAPU', case=False, na=False)]
        df_modulo = archivo[archivo['NOMBRE_ESTABLECIMIENTO'].str.contains('MODULO_DENTAL', case=False, na=False)]
        df_base = archivo[archivo['NOMBRE_ESTABLECIMIENTO'].str.contains('BASE', case=False, na=False)]
        df_regulador = archivo[archivo['NOMBRE_ESTABLECIMIENTO'].str.contains('CENTRO_REGULADOR', case=False, na=False)]

        # Sumar los valores de las columnas requeridas
        hospitalizados_hospital = df_hospitales['NUMERO_PACIENTES_ACTUALES_HOSPITALIZADOS'].sum()
        fallecidos_hospital = df_hospitales['NUMERO_PACIENTES_FALLECIDOS'].sum()
        ultimo_hospital = df_hospitales['NUMERO_ATENCIONES_ULTIMO_REPORTE'].sum()
        acumulados_hospital = df_hospitales['NUMERO_ATENCIONES_ACUMULADOS'].sum()

        hospitalizados_cesfam = df_cesfam['NUMERO_PACIENTES_ACTUALES_HOSPITALIZADOS'].sum()
        fallecidos_cesfam = df_cesfam['NUMERO_PACIENTES_FALLECIDOS'].sum()
        ultimo_cesfam = df_cesfam['NUMERO_ATENCIONES_ULTIMO_REPORTE'].sum()
        acumulados_cesfam = df_cesfam['NUMERO_ATENCIONES_ACUMULADOS'].sum()

        hospitalizados_cescof = df_cescof['NUMERO_PACIENTES_ACTUALES_HOSPITALIZADOS'].sum()
        fallecidos_cescof = df_cescof['NUMERO_PACIENTES_FALLECIDOS'].sum()
        ultimo_cescof = df_cescof['NUMERO_ATENCIONES_ULTIMO_REPORTE'].sum()
        acumulados_cescof = df_cescof['NUMERO_ATENCIONES_ACUMULADOS'].sum()

        hospitalizados_posta = df_posta['NUMERO_PACIENTES_ACTUALES_HOSPITALIZADOS'].sum()
        fallecidos_posta = df_posta['NUMERO_PACIENTES_FALLECIDOS'].sum()
        ultimo_posta = df_posta['NUMERO_ATENCIONES_ULTIMO_REPORTE'].sum()
        acumulados_posta = df_posta['NUMERO_ATENCIONES_ACUMULADOS'].sum()

        hospitalizados_sur = df_sur['NUMERO_PACIENTES_ACTUALES_HOSPITALIZADOS'].sum()
        fallecidos_sur = df_sur['NUMERO_PACIENTES_FALLECIDOS'].sum()
        ultimo_sur = df_sur['NUMERO_ATENCIONES_ULTIMO_REPORTE'].sum()
        acumulados_sur = df_sur['NUMERO_ATENCIONES_ACUMULADOS'].sum()

        hospitalizados_sar = df_sar['NUMERO_PACIENTES_ACTUALES_HOSPITALIZADOS'].sum()
        fallecidos_sar = df_sar['NUMERO_PACIENTES_FALLECIDOS'].sum()
        ultimo_sar = df_sar['NUMERO_ATENCIONES_ULTIMO_REPORTE'].sum()
        acumulados_sar = df_sar['NUMERO_ATENCIONES_ACUMULADOS'].sum()

        hospitalizados_sapu = df_sapu['NUMERO_PACIENTES_ACTUALES_HOSPITALIZADOS'].sum()
        fallecidos_sapu = df_sapu['NUMERO_PACIENTES_FALLECIDOS'].sum()
        ultimo_sapu = df_sapu['NUMERO_ATENCIONES_ULTIMO_REPORTE'].sum()
        acumulados_sapu = df_sapu['NUMERO_ATENCIONES_ACUMULADOS'].sum()

        hospitalizados_modulo = df_modulo['NUMERO_PACIENTES_ACTUALES_HOSPITALIZADOS'].sum()
        fallecidos_modulo = df_modulo['NUMERO_PACIENTES_FALLECIDOS'].sum()
        ultimo_modulo = df_modulo['NUMERO_ATENCIONES_ULTIMO_REPORTE'].sum()
        acumulados_modulo = df_modulo['NUMERO_ATENCIONES_ACUMULADOS'].sum()

        hospitalizados_base = df_base['NUMERO_PACIENTES_ACTUALES_HOSPITALIZADOS'].sum()
        fallecidos_base = df_base['NUMERO_PACIENTES_FALLECIDOS'].sum()
        ultimo_base = df_base['NUMERO_ATENCIONES_ULTIMO_REPORTE'].sum()
        acumulados_base = df_base['NUMERO_ATENCIONES_ACUMULADOS'].sum()

        hospitalizados_regulador = df_regulador['NUMERO_PACIENTES_ACTUALES_HOSPITALIZADOS'].sum()
        fallecidos_regulador = df_regulador['NUMERO_PACIENTES_FALLECIDOS'].sum()
        ultimo_regulador = df_regulador['NUMERO_ATENCIONES_ULTIMO_REPORTE'].sum()
        acumulados_regulador = df_regulador['NUMERO_ATENCIONES_ACUMULADOS'].sum()

        datos = {
            'TIPO_ESTABLECIMIENTO': ['HOSPITAL','CENTRO_REGULADOR','BASE','CENTRO_DE_SALUD_FAMILIAR','CENTRO_COMUNITARIO_DE_SALUD_FAMILIAR','POSTA','SUR','SAR','SAPU','MODULO_DENTAL'],
            'NUMERO_PACIENTES_ACTUALES_HOSPITALIZADOS': [hospitalizados_hospital,hospitalizados_regulador
                                                         ,hospitalizados_base,hospitalizados_cesfam,hospitalizados_cescof
                                                         ,hospitalizados_posta,hospitalizados_sur,hospitalizados_sar,hospitalizados_sapu
                                                         ,hospitalizados_modulo],
            'NUMERO_PACIENTES_FALLECIDOS' : [fallecidos_hospital,fallecidos_regulador,fallecidos_base,fallecidos_cesfam,
                                             fallecidos_cescof,fallecidos_posta,fallecidos_sur,fallecidos_sar,fallecidos_sapu,
                                             fallecidos_modulo],
            'NUMERO_ATENCIONES_ULTIMO_REPORTE' : [ultimo_hospital,ultimo_regulador,ultimo_base,ultimo_cesfam,ultimo_cescof,ultimo_posta
                                                  ,ultimo_sur,ultimo_sar,ultimo_sapu,ultimo_modulo],
            'NUMERO_ATENCIONES_ACUMULADOS' : [acumulados_hospital,acumulados_regulador,acumulados_base,acumulados_cesfam,acumulados_cescof,
                                              acumulados_posta,acumulados_sur,acumulados_sar,acumulados_sapu,acumulados_modulo]
        }

    except Exception as e:
        return f'Error: {e}'

    # Crear DataFrame con los resultados
    tabla = pd.DataFrame(datos)
    tabla_html = tabla.to_html(classes="table table-striped", index=False, escape=False)
    tabla_html = tabla_html.replace(
            r'<td>([1-9][0-9]*)</td>',
            r'<td data-clickable="true" style="cursor: pointer;">\1</td>')

    # Crear diccionario para almacenar las mini tablas
    tablas_Operatividad = {'principalCONSULTAS': tabla_html}

    # Crear mini tablas para cada valor distinto de 0
    for c in consultas:
        for tipo_establecimiento in archivo['TIPO_ESTABLECIMIENTO'].unique():
            # Filtrar el DataFrame por tipo de establecimiento y columna de consulta
            df_filtrado = archivo[(archivo['TIPO_ESTABLECIMIENTO'] == tipo_establecimiento) & 
                                  (archivo[c] != 0)]
                
            # Si el DataFrame no está vacío, proceder
            if not df_filtrado.empty:
                # Crear una mini tabla para los establecimientos con valor distinto de 0
                table_name = f"{tipo_establecimiento}_{c}".upper()
                tablas_Operatividad[table_name] = df_filtrado[['NOMBRE_ESTABLECIMIENTO', c]].to_html(classes="table table-striped", index=False)
    
    return tablas_Operatividad