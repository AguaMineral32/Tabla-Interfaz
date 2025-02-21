import pandas as pd
def crear_tabla_comunas2(archivo):
    try:
        # Crear lista con los tipos de establecimientos únicos
        tipos_establecimiento = archivo[archivo['TIPO_ESTABLECIMIENTO'].isin(['CENTRO_DE_SALUD_FAMILIAR','CENTRO_COMUNITARIO_DE_SALUD_FAMILIAR' ,'POSTA'])]['TIPO_ESTABLECIMIENTO'].unique()
        
        # Crear un diccionario para almacenar los resultados de cada tipo de establecimiento
        resultado = {'COMUNA': []}
        
        # Añadir las columnas de tipo S (semioperativo) e I (inoperativo)
        for tipo in tipos_establecimiento:
            resultado[f'{tipo}_S'] = []
            resultado[f'{tipo}_I'] = []
        
        # Diccionario para almacenar las tablas individuales
        tablasAfectacionC = {}
        
        # Agrupar los datos por COMUNA
        for comuna, grupo in archivo.groupby('COMUNA'):
            resultado['COMUNA'].append(comuna)
            
            # Para cada tipo de establecimiento, contar los semioperativos e inoperativos
            for tipo in tipos_establecimiento:
                # Filtrar los establecimientos con el tipo y operatividad correspondientes
                semioperativos = grupo[(grupo['TIPO_ESTABLECIMIENTO'] == tipo) & (grupo['OPERATIVIDAD_ESTABLECIMIENTO'] == 'SEMIOPERATIVO')]
                inoperativos = grupo[(grupo['TIPO_ESTABLECIMIENTO'] == tipo) & (grupo['OPERATIVIDAD_ESTABLECIMIENTO'] == 'INOPERATIVO')]
                
                # Contar los registros y agregarlos a las listas de resultados
                resultado[f'{tipo}_S'].append(semioperativos.shape[0])
                resultado[f'{tipo}_I'].append(inoperativos.shape[0])
                
                # Crear tablas individuales para semioperativos
                if not semioperativos.empty:
                    # Obtener el primer valor de la fila (comuna) y columna (tipo de establecimiento)
                    comuna_valor = semioperativos.iloc[0]['COMUNA']
                    operatividad = 'S'  # Para semioperativo
                    table_name = f"{comuna_valor}_{tipo}_{operatividad}".upper()
                    tablasAfectacionC[table_name] = semioperativos[['COMUNA', 'TIPO_ESTABLECIMIENTO', 'NOMBRE_ESTABLECIMIENTO']].to_html(classes="table table-striped", index=False)
                
                # Crear tablas individuales para inoperativos
                if not inoperativos.empty:
                    # Obtener el primer valor de la fila (comuna) y columna (tipo de establecimiento)
                    comuna_valor = inoperativos.iloc[0]['COMUNA']
                    operatividad = 'I'  # Para inoperativo
                    table_name = f"{comuna_valor}_{tipo}_{operatividad}".upper()
                    tablasAfectacionC[table_name] = inoperativos[['COMUNA', 'TIPO_ESTABLECIMIENTO', 'NOMBRE_ESTABLECIMIENTO']].to_html(classes="table table-striped", index=False)
        
        # Crear el DataFrame final con los resultados
        df_resultado = pd.DataFrame(resultado)
        
        # Convertir el DataFrame final a una tabla HTML
        principalAfectacionC = df_resultado.to_html(classes="table table-striped", index=False)
        tablasAfectacionC['principalComunas 2'] = principalAfectacionC
        
        # Incluir las tablas individuales en la variable de retorno
        return tablasAfectacionC

    except Exception as e:
        raise ValueError(f"Error al generar la tabla: {e}")
