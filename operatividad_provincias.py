import pandas as pd

def crear_tabla_provincia(archivo):
    try:
        tipos_operatividad = ['OPERATIVO', 'SEMIOPERATIVO', 'INOPERATIVO']
        df_operativos = archivo[archivo['OPERATIVIDAD_ESTABLECIMIENTO'].isin(tipos_operatividad)]

        # Generar la tabla resumen
        conteo_establecimientos = (
            df_operativos.groupby(['PROVINCIA', 'OPERATIVIDAD_ESTABLECIMIENTO'])
            .size()
            .unstack(fill_value=0)
        )

        for tipo in tipos_operatividad:
            if tipo not in conteo_establecimientos.columns:
                conteo_establecimientos[tipo] = 0

        conteo_establecimientos = conteo_establecimientos[['OPERATIVO', 'SEMIOPERATIVO', 'INOPERATIVO']]
        conteo_establecimientos = conteo_establecimientos.reset_index()
        conteo_establecimientos = conteo_establecimientos.rename_axis(None, axis=1)
        conteo_establecimientos.rename(columns={'OPERATIVO': 'OPERATIVO_PROVINCIA'}, inplace=True)
        conteo_establecimientos.rename(columns={'SEMIOPERATIVO': 'SEMIOPERATIVO_PROVINCIA'}, inplace=True)
        conteo_establecimientos.rename(columns={'INOPERATIVO': 'INOPERATIVO_PROVINCIA'}, inplace=True)

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
        tablas_Operatividad['principalPROVINCIA'] = conteo_establecimientos_html

        # Para cada tipo de operatividad, crear una tabla con los datos filtrados
        for operatividad in tipos_operatividad:
            for provincias in archivo['PROVINCIA'].unique():
                # Filtrar el DataFrame por tipo de establecimiento y operatividad
                df_filtrado = archivo[(archivo['PROVINCIA'] == provincias) & 
                                (archivo['OPERATIVIDAD_ESTABLECIMIENTO'] == operatividad)]
                
                # Si el DataFrame no está vacío, proceder
                if not df_filtrado.empty:
                    columnas = ['NOMBRE_ESTABLECIMIENTO', 'OPERATIVIDAD_ESTABLECIMIENTO','COMUNA','DESCRIPCION_SITUACION','HORA_EDAN','FECHA_EDAN']
                    # Añadir la columna 'DESCRIPCION_SITUACION' si la operatividad es SEMIOPERATIVO o INOPERATIVO

                    # Convertir la tabla filtrada en HTML
                    table_name = f"{provincias}_{operatividad}_PROVINCIA".upper()
                    tablas_Operatividad[table_name] = df_filtrado[columnas].to_html(classes="table table-striped", index=False)

        # Asegurarse de que las tablas HTML se devuelvan correctamente
        return tablas_Operatividad

    except Exception as e:
        raise ValueError(f"Error al generar la tabla: {e}")
