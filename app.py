import pandas as pd
import os
import glob
import datetime
import threading
import subprocess
from unidecode import unidecode
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, send_file, session
from flask_session import Session
from datetime import time

# Importar funciones de las tablas
from vehiculos import crear_tabla_vehiculos
from boxes_de_atencion import crear_tabla_boxes
from sapu import crear_tabla_sapu
from servicios_de_apoyo import crear_tabla_servicios
from medicamentosInsumos import crear_tabla_medicamentos
from farmacia import crear_tabla_farmacia
from recursosHumanos import crear_tabla_rrhh
from pabellones import crear_tabla_pabellones
from agua_potable import crear_tabla_agua
from alcantarillado import crear_tabla_alcantarillado
from urgencia import crear_tabla_urgencia
from bodegasPNAC import crear_tabla_bodegas
from energia import crear_tabla_energia
from vias_de_acceso import crear_tabla_vias_acceso
from telecomunicaciones import crear_tabla_teleco
from gases_clinicos import crear_tabla_gases
from vacunatorios import crear_tabla_vacunatorios
from camas import crear_tabla_camas
from UPC import crear_tabla_UPC
from operatividad_provincias import crear_tabla_provincia
from samu import crear_tabla_samu
from evacuacion import crear_tabla_evacuacion
from consultas_avanzada import crear_tabla_consultas
from comunas1 import crear_tabla_comunas1
from comunas2 import crear_tabla_comunas2
from comunas3 import crear_tabla_comunas3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.secret_key = 'goku'
app.config['SESSION_TYPE'] = 'filesystem'  # Guarda la sesión en archivos temporales
Session(app)  # Activa Flask-Session

# Tabla de operatividad
def tabla_operatividad(archivo):
    try:
        tipos_operatividad = ['OPERATIVO', 'SEMIOPERATIVO', 'INOPERATIVO']
        df_operativos = archivo[archivo['OPERATIVIDAD_ESTABLECIMIENTO'].isin(tipos_operatividad)]

        # Generar la tabla resumen
        conteo_establecimientos = (
            df_operativos.groupby(['TIPO_ESTABLECIMIENTO', 'OPERATIVIDAD_ESTABLECIMIENTO'])
            .size()
            .unstack(fill_value=0)
        )

        for tipo in tipos_operatividad:
            if tipo not in conteo_establecimientos.columns:
                conteo_establecimientos[tipo] = 0

        conteo_establecimientos = conteo_establecimientos[['OPERATIVO', 'SEMIOPERATIVO', 'INOPERATIVO']]
        conteo_establecimientos = conteo_establecimientos.reset_index()
        conteo_establecimientos = conteo_establecimientos.rename_axis(None, axis=1)

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
        tablas_Operatividad['principalOperatividad'] = conteo_establecimientos_html

        # Para cada tipo de operatividad, crear una tabla con los datos filtrados
        for operatividad in tipos_operatividad:
            for tipo_establecimiento in archivo['TIPO_ESTABLECIMIENTO'].unique():
                # Filtrar el DataFrame por tipo de establecimiento y operatividad
                df_filtrado = archivo[(archivo['TIPO_ESTABLECIMIENTO'] == tipo_establecimiento) &
                                (archivo['OPERATIVIDAD_ESTABLECIMIENTO'] == operatividad)]

                # Si el DataFrame no está vacío, proceder
                if not df_filtrado.empty:
                    columnas = ['NOMBRE_ESTABLECIMIENTO', 'OPERATIVIDAD_ESTABLECIMIENTO']
                    # Añadir la columna 'DESCRIPCION_SITUACION' si la operatividad es SEMIOPERATIVO o INOPERATIVO
                    if operatividad in ['SEMIOPERATIVO', 'INOPERATIVO']:
                        df_filtrado['DESCRIPCION_SITUACION'] = df_filtrado.get('DESCRIPCION_SITUACION', 'SIN_DESCRIPCION')
                        columnas.append('DESCRIPCION_SITUACION')

                    # Convertir la tabla filtrada en HTML
                    table_name = f"{tipo_establecimiento}_{operatividad}".upper()
                    tablas_Operatividad[table_name] = df_filtrado[columnas].to_html(classes="table table-striped", index=False)

        # Asegurarse de que las tablas HTML se devuelvan correctamente
        return tablas_Operatividad

    except Exception as e:
        raise ValueError(f"Error al generar la tabla: {e}")



    except Exception as e:
        raise ValueError(f"Error al generar la tabla: {e}")


# Funciones de procesamiento
def remove_accents(text):
    return unidecode(text) if isinstance(text, str) else text

def convert_to_string(value):
    if pd.api.types.is_number(value):  # Si es un número, conviértelo a cadena
        return str(value)
    elif isinstance(value, pd.Timestamp):  # Si es datetime, formatea como fecha y hora
        return value.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(value, pd.Timedelta):  # Si es un timedelta, conviértelo a cadena
        return str(value)
    elif isinstance(value, (datetime.time)):  # Si es un objeto de tiempo, formatea como hh:mm:ss
        return value.strftime('%H:%M:%S')
    return value  # Devolver el valor tal cual si no aplica ninguna condición


def eliminar_guiones_bajos(texto):
    if isinstance(texto, str):
        return texto.strip('_')
    return texto

def limpiar_df(_df_):
    _df_ = _df_.fillna('NOINFO')
    _df_.columns = [col.upper() for col in _df_.columns]
    _df_.columns = _df_.columns.map(remove_accents)
    _df_ = _df_.map(remove_accents)
    _df_ = _df_.map(lambda x: x.upper() if isinstance(x, str) else x)
    _df_ = _df_.map(convert_to_string)
    _df_ = _df_.replace(' ', '_', regex=True)
    _df_.columns = _df_.columns.str.replace(' ', '_', regex=False)
    _df_ = _df_.map(eliminar_guiones_bajos)
    _df_.columns = _df_.columns.str.strip('_')
    return _df_

def obtener_provincia(Nombre_Comuna):
    if Nombre_Comuna in ['CAUQUENES', 'CHANCO', 'PELLUHUE']:
        return 'CAUQUENES'
    elif Nombre_Comuna in ['COLBUN','LINARES', 'LONGAVI', 'PARRAL', 'RETIRO', 'SAN_JAVIER', 'VILLA_ALEGRE', 'YERBAS_BUENAS']:
        return 'LINARES'
    elif Nombre_Comuna in ['CONSTITUCION', 'CUREPTO', 'EMPEDRADO', 'MAULE', 'PELARCO', 'PENCAHUE', 'RIO_CLARO', 'SAN_CLEMENTE', 'SAN_RAFAEL', 'TALCA']:
        return 'TALCA'
    elif Nombre_Comuna in ['CURICO', 'HUALAÑE', 'HUALANE', 'LICANTEN', 'MOLINA', 'RAUCO', 'ROMERAL', 'SAGRADA_FAMILIA', 'TENO', 'VICHUQUEN']:
        return 'CURICO'
    else:
        return 'NOPROVINCIA'

def obtener_tipo(NOMBRE_ESTABLECIMIENTO):
    if 'HOSPITAL' in NOMBRE_ESTABLECIMIENTO:
        return 'HOSPITAL'
    elif 'POSTA' in NOMBRE_ESTABLECIMIENTO:
        return 'POSTA'
    elif 'CENTRO_DE_SALUD_FAMILIAR' in NOMBRE_ESTABLECIMIENTO:
        return 'CENTRO_DE_SALUD_FAMILIAR'
    elif 'SUR' in NOMBRE_ESTABLECIMIENTO:
        return 'SUR'
    elif 'SAR' in NOMBRE_ESTABLECIMIENTO:
        return 'SAR'
    elif 'SAPU' in NOMBRE_ESTABLECIMIENTO:
        return 'SAPU'
    elif 'CENTRO_COMUNITARIO_DE_SALUD_FAMILIAR' in NOMBRE_ESTABLECIMIENTO:
        return 'CENTRO_COMUNITARIO_DE_SALUD_FAMILIAR'
    elif 'MODULO_DENTAL' in NOMBRE_ESTABLECIMIENTO:
        return 'MODULO_DENTAL'
    elif 'BASE' in NOMBRE_ESTABLECIMIENTO:
        return 'BASE_SAMU'
    elif 'CENTRO_REGULADOR' in NOMBRE_ESTABLECIMIENTO:
        return 'CENTRO_REGULADOR_SAMU'
    else:
        return 'TIPO_NO_ESPECIFICADO'

def delete_uploaded_files():
    upload_folder = os.path.join(os.path.dirname(__file__), 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)  # Crear la carpeta si no existe

    files = glob.glob(os.path.join(upload_folder, '*'))
    for file in files:
        try:
            os.remove(file)  # Elimina el archivo
            print(f'Archivo eliminado: {file}')
        except Exception as e:
            print(f'Error al eliminar el archivo {file}: {e}')

def delete_map():
    templates_folder = os.path.join(os.path.dirname(__file__), 'templates')
    mapa_file = os.path.join(templates_folder, 'mapa_interactivo.html')

    print(f"Ruta de la carpeta templates: {templates_folder}")
    print(f"Ruta del archivo mapa_interactivo.html: {mapa_file}")

    if os.path.exists(mapa_file):
        try:
            os.remove(mapa_file)
            print(f'Archivo mapa_interactivo.html eliminado de templates')
        except Exception as e:
            print(f'Error al eliminar mapa_interactivo.html: {e}')
    else:
        print(f"El archivo mapa_interactivo.html no existe en la ruta especificada.")


# Hook para ejecutar antes de cada solicitud
@app.before_request
def before_request():
    # Eliminar archivos solo si la solicitud es GET o HEAD
    if request.method in ['GET', 'HEAD']:
        delete_uploaded_files()
    if request.method in ['GET', 'HEAD'] and not request.path.startswith('/mostrar_mapa'):
        delete_map()

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Cargar y preparar los datos al iniciar la aplicación
custom_df = pd.DataFrame()  # Variable para almacenar la tabla filtrada
custom_df_original = pd.DataFrame()  # Variable para almacenar la tabla original

# Rutas generales

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subida')
def subida():
    return render_template('Tablas/subida.html')

@app.route('/chart')
def chart():
    return render_template('chart.html')

@app.route('/mapa')
def mapa():
    return render_template('mapa.html')

@app.route('/maule')
def maule():
    return render_template('mapa_maule.html')

@app.route('/changelog')
def changelog():
    return render_template('changelog.html')

# ////////////////////// Rutas de la pagina de tablas //////////////////////

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        uploaded_files = request.files.getlist('files[]')
        print("Archivos subidos:", uploaded_files)  # Agrega esto para ver el contenido de uploaded_files
        if not uploaded_files or all(file.filename == '' for file in uploaded_files):
            return jsonify({'error': 'No se subieron archivos.'}), 400

        global custom_df, custom_df_original
        custom_df = pd.DataFrame()
        eventos_set = set()  # Usamos un conjunto para eliminar duplicados
        codigo_eventos_set = set()  # Usamos un conjunto para eliminar duplicados
        tablaOperatividad = False
        tablaAfectacionC = False
        hora_inicio = int(request.form.get('horaInicio', 0))
        hora_fin = int(request.form.get('horaFin', 23))
        hora_inicio = time(hora_inicio,0)
        hora_fin = time(hora_fin,0)
        nuevo_df = []
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            df = pd.read_excel(filepath)
            if "EVENTO" in df.columns:
                eventos_set.update(df["EVENTO"].dropna().astype(str).unique())
            if "COD_EVENTO" in df.columns:
                codigo_eventos_set.update(df["COD_EVENTO"].dropna().astype(str).unique())
            for _, columna in df.iterrows():
                if columna['HORA_EDAN'] > hora_inicio and columna['HORA_EDAN']<hora_fin:
                    nuevo_df.append(columna)
            df = pd.DataFrame(nuevo_df)
            df = limpiar_df(df)

            if 'NOMBRE_COMUNA' in df.columns:
                df['PROVINCIA'] = df['NOMBRE_COMUNA'].apply(obtener_provincia)

            if 'COMUNA' in df.columns:
                df['PROVINCIA'] = df['COMUNA'].apply(obtener_provincia)
                # df = df.drop(columns={'COMUNA'})

            if 'NOMBRE_ESTABLECIMIENTO' in df.columns:
                df['TIPO_ESTABLECIMIENTO'] = df['NOMBRE_ESTABLECIMIENTO'].apply(obtener_tipo)

            reqTablaOperatividad = ['TIPO_ESTABLECIMIENTO', 'OPERATIVIDAD_ESTABLECIMIENTO', 'NOMBRE_ESTABLECIMIENTO']
            if all(columna in df.columns for columna in reqTablaOperatividad):
                tablaOperatividad = True

            reqTablaAfectacionC = ['COMUNA', 'OPERATIVIDAD_ESTABLECIMIENTO', 'TIPO_ESTABLECIMIENTO', 'NOMBRE_ESTABLECIMIENTO']
            if all(columna in df.columns for columna in reqTablaAfectacionC):
                tablaAfectacionC = True

            custom_df = pd.concat([custom_df, df], ignore_index=True)

        custom_df_original = custom_df.copy()

        # Generar tablas y almacenarlas en la sesión
        tablas_Operatividad = tabla_operatividad(custom_df) if tablaOperatividad else {}
        tablasAfectacionC = crear_tabla_comunas1(custom_df) if tablaAfectacionC else {} #({}, {})
        tabla_pabellones = crear_tabla_pabellones(custom_df) if tablaAfectacionC else {}
        tabla_energia = crear_tabla_energia(custom_df) if tablaAfectacionC else {}
        tabla_gases = crear_tabla_gases(custom_df) if tablaAfectacionC else {}
        tabla_vias = crear_tabla_vias_acceso(custom_df) if tablaAfectacionC else {}
        tabla_provincia = crear_tabla_provincia(custom_df) if tablaAfectacionC else {}
        tabla_bodegas = crear_tabla_bodegas(custom_df) if tablaAfectacionC else {}
        tabla_urgencias = crear_tabla_urgencia(custom_df) if tablaAfectacionC else {}
        tabla_alcantarillado = crear_tabla_alcantarillado(custom_df) if tablaAfectacionC else {}
        tabla_agua = crear_tabla_agua(custom_df) if tablaAfectacionC else {}
        tabla_vehiculos = crear_tabla_vehiculos(custom_df) if tablaAfectacionC else {}
        tabla_boxes = crear_tabla_boxes(custom_df) if tablaAfectacionC else {}
        tabla_sapu = crear_tabla_sapu(custom_df) if tablaAfectacionC else {}
        tabla_servicios = crear_tabla_servicios(custom_df) if tablaAfectacionC else {}
        tabla_medicamentos = crear_tabla_medicamentos(custom_df) if tablaAfectacionC else {}
        tabla_farmacia = crear_tabla_farmacia(custom_df) if tablaAfectacionC else {}
        tabla_rrhh = crear_tabla_rrhh(custom_df) if tablaAfectacionC else {}
        tabla_teleco = crear_tabla_teleco(custom_df) if tablaAfectacionC else {}
        tabla_vacunas = crear_tabla_vacunatorios(custom_df) if tablaAfectacionC else {}
        tabla_camas = crear_tabla_camas(custom_df) if tablaAfectacionC else {}
        tabla_UPC = crear_tabla_UPC(custom_df) if tablaAfectacionC else {}
        tabla_samu = crear_tabla_samu(custom_df) if tablaAfectacionC else {}
        tabla_evacuacion = crear_tabla_evacuacion(custom_df) if tablaAfectacionC else {}
        tabla_consultas = crear_tabla_consultas(custom_df) if tablaAfectacionC else {}
        tablasAfectacionC2 = crear_tabla_comunas2(custom_df) if tablaAfectacionC else {}
        tablasAfectacionC3 = crear_tabla_comunas3(custom_df) if tablaAfectacionC else {}

        session['tablas'] = tablas_Operatividad
        session['tablas'].update(tabla_samu)
        session['tablas'].update(tabla_provincia)
        session['tablas'].update(tablasAfectacionC)
        session['tablas'].update(tablasAfectacionC2)
        session['tablas'].update(tablasAfectacionC3)
        session['tablas'].update(tabla_consultas)
        session['tablas'].update(tabla_evacuacion)
        session['tablas'].update(tabla_vias)
        session['tablas'].update(tabla_agua)
        session['tablas'].update(tabla_energia)
        session['tablas'].update(tabla_teleco)
        session['tablas'].update(tabla_gases)
        session['tablas'].update(tabla_alcantarillado)
        session['tablas'].update(tabla_pabellones)
        session['tablas'].update(tabla_bodegas)
        session['tablas'].update(tabla_urgencias)
        session['tablas'].update(tabla_vehiculos)
        session['tablas'].update(tabla_boxes)
        session['tablas'].update(tabla_sapu)
        session['tablas'].update(tabla_servicios)
        session['tablas'].update(tabla_medicamentos)
        session['tablas'].update(tabla_farmacia)
        session['tablas'].update(tabla_rrhh)
        session['tablas'].update(tabla_vacunas)
        session['tablas'].update(tabla_camas)
        session['tablas'].update(tabla_UPC)
        session.modified = True  # 🔥 Fuerza a Flask a guardar la sesión
        listaTablas = [tablaOperatividad,tablaAfectacionC,tabla_pabellones, tabla_energia, tabla_gases,
                       tabla_vias, tabla_provincia, tabla_bodegas,tabla_urgencias,
                       tabla_alcantarillado,tabla_agua,tabla_vehiculos, tabla_boxes, tabla_sapu,
                       tabla_servicios, tabla_medicamentos, tabla_farmacia, tabla_rrhh,
                       tabla_teleco, tabla_vacunas, tabla_camas, tabla_UPC,tabla_samu,tabla_evacuacion,tabla_consultas,
                       tablasAfectacionC2,tablasAfectacionC3]
        tablaContainer = any(listaTablas)
        tablasPrincipales = [clave for clave in session.get('tablas',{}).keys() if 'principal' in clave]
        # print(tablasAfectacionC.keys())

        return jsonify({
            'message': 'Archivo(s) subido(s) exitosamente!',
            'tablasPrincipales': tablasPrincipales,
            'tablaContainer': tablaContainer,
            'eventos': list(eventos_set),  # Convertimos el conjunto en lista
            'codigo_eventos': list(codigo_eventos_set)  # Convertimos el conjunto en lista

        }), 200

    except Exception as e:
        return jsonify({'error': f'Ocurrió un error al procesar los archivos: {str(e)}'}), 500

@app.route('/get_table', methods=['GET'])
def get_table():
    try:
        table_name = request.args.get('table_name')
        #print("Tablas en sesión:", session.get('tablas', {}).keys())  # 🔥 Ver qué tablas existen
        if not table_name:
            return jsonify({"error": "Nombre de la tabla no proporcionado."}), 400

        tablas = session.get('tablas', {})

        if table_name not in tablas:
            return '', 200
            # return jsonify({"error": f"La tabla '{table_name}' no existe."}), 404

        return jsonify({"table": tablas[table_name]}), 200

    except Exception as e:
        return jsonify({"error": f"Error al obtener la tabla: {str(e)}"}), 500

@app.route('/filtro')
def filtro():
    global custom_df
    if custom_df is None or custom_df.empty:
        return "No hay datos disponibles para filtrar. Suba un archivo primero.", 400

    columnas = custom_df.columns.tolist()
    return render_template('Tablas/filtro.html', columnas=columnas)

@app.route('/obtener_valores', methods=['POST'])
def obtener_valores():
    global custom_df
    columna = request.json.get('columna')
    if columna and columna in custom_df.columns:
        valores = custom_df[columna].dropna().unique().tolist()
        return jsonify({'valores': valores})
    return jsonify({'valores': []})

@app.route('/filtrar', methods=['POST'])
def filtrar():
    global custom_df
    columna = request.json.get('columna')
    valor = request.json.get('valor')
    columnas_seleccionadas = request.json.get('columnas_seleccionadas')

    if columna and valor and columna in custom_df.columns:
        custom_df = custom_df[custom_df[columna] == valor]

    if columnas_seleccionadas:
        df_filtrado = custom_df[columnas_seleccionadas]
    else:
        df_filtrado = custom_df.copy()

    df_html = df_filtrado.to_html(classes='table table-striped', index=False)
    return jsonify({'tabla': df_html})

@app.route('/reset_filters', methods=['POST'])
def reset_filters():
    global custom_df, custom_df_original
    if custom_df_original.empty:
        return jsonify({'error': 'No hay datos originales para reiniciar.'}), 400

    # Restaurar custom_df a su estado original
    custom_df = custom_df_original.copy()

    # Obtener las columnas seleccionadas
    columnas_seleccionadas = request.json.get('columnas_seleccionadas', [])
    if columnas_seleccionadas:
        df_reseteado = custom_df[columnas_seleccionadas]
    else:
        df_reseteado = custom_df.copy()

    df_html = df_reseteado.to_html(classes='table table-striped', index=False)
    return jsonify({'tabla': df_html})


@app.route('/download_filtered', methods=['GET'])
def download_filtered():
    try:
        global custom_df
        if custom_df is None or custom_df.empty:
            return "No hay datos filtrados para descargar.", 404

        columnas_seleccionadas = request.args.get('columnas', '')
        columnas_seleccionadas = columnas_seleccionadas.split(',') if columnas_seleccionadas else custom_df.columns.tolist()

        df_seleccionado = custom_df[columnas_seleccionadas]

        output_filename = 'datos_filtrados.xlsx'
        output_path = os.path.join(app.root_path, output_filename)
        df_seleccionado.to_excel(output_path, index=False)

        response = send_file(output_path, as_attachment=True, download_name="datos_filtrados.xlsx")

        @response.call_on_close
        def remove_file():
            try:
                os.remove(output_path)
                print(f"Archivo {output_filename} eliminado.")
            except Exception as e:
                print(f"Error al eliminar el archivo {output_filename}: {e}")

        threading.Timer(2, remove_file).start()
        return response
    except Exception as e:
        return f"Error al generar el archivo: {str(e)}", 500

# ////////////////////// Rutas de la pagina de tablas //////////////////////

def crear_mapa(mapa):
    try:
        ruta_mapas = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mapas.py')
        print(f"Ejecutando el script mapas.py con el archivo: {mapa}")
        result = subprocess.run(["python", ruta_mapas, mapa], check=True, capture_output=True, text=True)
        print("El script mapas.py se ejecutó correctamente.")
        print(f"Salida del script: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar mapas.py: {e}")
        print(f"Salida de error: {e.stderr}")


@app.route('/upload_mapa', methods=['POST'])
def upload_mapa():
    try:
        delete_map()
        uploaded_files = request.files.getlist('files[]')
        if not uploaded_files or all(file.filename == '' for file in uploaded_files):
            return jsonify({'error': 'No se subieron archivos.'}), 400

        for file in uploaded_files:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            crear_mapa(filepath)

        return jsonify({'message': 'Archivo(s) subido(s) exitosamente!'}), 200

    except Exception as e:
        return jsonify({'error': f'Ocurrió un error al procesar los archivos: {str(e)}'}), 500

@app.route('/mostrar_mapa')
def mostrar_mapa():
    return send_file('templates/mapa_interactivo.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)