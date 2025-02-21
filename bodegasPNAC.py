import pandas as pd

def crear_tabla_bodegas(archivo):
    try:
        tipos_operatividad = ['OPERATIVO', 'SEMI_OPERATIVO', 'NO_OPERATIVO']
        df_operativos = archivo[archivo['BODEGAS_PNAC'].isin(tipos_operatividad)]

        # Generar la tabla resumen
        conteo_establecimientos = (
            df_operativos.groupby(['TIPO_ESTABLECIMIENTO', 'BODEGAS_PNAC'])
            .size()
            .unstack(fill_value=0)
        )

        for tipo in tipos_operatividad:
            if tipo not in conteo_establecimientos.columns:
                conteo_establecimientos[tipo] = 0

        conteo_establecimientos = conteo_establecimientos[['OPERATIVO', 'SEMI_OPERATIVO', 'NO_OPERATIVO']]
        conteo_establecimientos = conteo_establecimientos.reset_index()
        conteo_establecimientos = conteo_establecimientos.rename_axis(None, axis=1)
        conteo_establecimientos.rename(columns={'OPERATIVO': 'OPERATIVO_BODEGAS_PNAC'}, inplace=True)
        conteo_establecimientos.rename(columns={'SEMI_OPERATIVO': 'SEMI_OPERATIVO_BODEGAS_PNAC'}, inplace=True)
        conteo_establecimientos.rename(columns={'NO_OPERATIVO': 'NO_OPERATIVO_BODEGAS_PNAC'}, inplace=True)

        # Convertir la tabla en HTML
        conteo_establecimientos_html = conteo_establecimientos.to_html(classes="table table-striped", index=False, escape=False)

        # Marcar celdas clicables con un atributo "data-clickable"
        conteo_establecimientos_html = conteo_establecimientos_html.replace(
            r'<td>([1-9][0-9]*)</td>',
            r'<td data-clickable="true" style="cursor: pointer;">\1</td>'
        )

        # Usar un diccionario en lugar de una lista
        tablas_Operatividad = {}

        # Almacenar la tabla resumen
        tablas_Operatividad['principalBODEGAS_PNAC'] = conteo_establecimientos_html

        # Para cada tipo de operatividad, crear una tabla con los datos filtrados
        for operatividad in tipos_operatividad:
            for tipo_establecimiento in archivo['TIPO_ESTABLECIMIENTO'].unique():
                # Filtrar el DataFrame por tipo de establecimiento y operatividad
                df_filtrado = archivo[(archivo['TIPO_ESTABLECIMIENTO'] == tipo_establecimiento) & 
                                (archivo['BODEGAS_PNAC'] == operatividad)]
                
                # Si el DataFrame no está vacío, proceder
                if not df_filtrado.empty:
                    columnas = ['NOMBRE_ESTABLECIMIENTO', 'BODEGAS_PNAC','DETALLE_BODEGAS_PNAC','HORA_EDAN','FECHA_EDAN']


                    # Convertir la tabla filtrada en HTML
                    table_name = f"{tipo_establecimiento}_{operatividad}_BODEGAS_PNAC".upper()
                    tablas_Operatividad[table_name] = df_filtrado[columnas].to_html(classes="table table-striped", index=False)

        # Asegurarse de que las tablas HTML se devuelvan correctamente
        return tablas_Operatividad

    except Exception as e:
        raise ValueError(f"Error al generar la tabla: {e}")

