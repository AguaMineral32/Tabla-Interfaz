import pandas as pd
from dash import Dash, html, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
from pandas.plotting import table

curico_diccionario_operativos = {'curico' : []}
curico_diccionario_inoperativos = {'curico' : []}
curico_diccionario_semi = {'curico' : []}

talca_diccionario_operativos = {'talca' : []}
talca_diccionario_inoperativos = {'talca' : []}
talca_diccionario_semi = {'talca' : []}

linares_diccionario_operativos = {'linares' : []}
linares_diccionario_inoperativos = {'linares' : []}
linares_diccionario_semi = {'linares' : []}

cauquenes_diccionario_operativos = {'cauquenes' : []}
cauquenes_diccionario_inoperativos = {'cauquenes' : []}
cauquenes_diccionario_semi = {'cauquenes' : []}

curico_operativos = 0
curico_inoperativos = 0
curico_semioperativos = 0

talca_operativos = 0
talca_inoperativos = 0
talca_semioperativos = 0

linares_operativos = 0
linares_inoperativos = 0
linares_semioperativos = 0

cauquenes_operativos = 0
cauquenes_inoperativos = 0
cauquenes_semioperativos = 0
def crear_tabla_provincia(archivo):
  pd.set_option('display.max_rows', None)  # Muestra todas las filas
  pd.set_option('display.max_columns', None)  # Muestra todas las columnas
  data = []

  def separacion_instalaciones(tipoDeInstalacion):
      data = {
          'ID_EDAN': [],
          'NOMBRE_ESTABLECIMIENTO': [],
          'COMUNA': [],
          'operatividad_establecimiento': [],
      }
      for _, raw in archivo.iterrows():

          edan = raw['ID_EDAN']
          nombre = raw['NOMBRE_ESTABLECIMIENTO']
          comuna = raw['COMUNA']
          operatividad = raw['OPERATIVIDAD_ESTABLECIMIENTO']
          tipo = tipoDeInstalacion

          if tipo in nombre:
              data['ID_EDAN'].append(edan)
              data['NOMBRE_ESTABLECIMIENTO'].append(nombre)
              data['COMUNA'].append(comuna)
              data['operatividad_establecimiento'].append(operatividad)

      datos = pd.DataFrame(data)
      return datos

  hospital=separacion_instalaciones('HOSPITAL')
  centro=separacion_instalaciones('CENTRO_DE_SALUD_FAMILIAR')
  comunitario=separacion_instalaciones('CENTRO_COMUNITARIO_DE_SALUD_FAMILIAR')
  psr=separacion_instalaciones('POSTA_DE_SALUD_RURAL')
  csmc=separacion_instalaciones('CENTRO_DE_SALUD_MENTAL_COMUNITARIO')
  sur=separacion_instalaciones('SUR')
  sar=separacion_instalaciones('SAR')
  sapu=separacion_instalaciones('SAPU')

  datos = {
      'Provincias': [],
      'Operativos': [],
      'Inoperativos': [],
      'Semioperativos': [],
  }





  def recolectar_datos_establecimientos(nombre):
    global curico_operativos, curico_inoperativos, curico_semioperativos
    global talca_operativos, talca_inoperativos, talca_semioperativos
    global linares_operativos, linares_inoperativos, linares_semioperativos
    global cauquenes_operativos, cauquenes_inoperativos, cauquenes_semioperativos

    global curico_diccionario_operativos, curico_diccionario_inoperativos, curico_diccionario_semi
    global talca_diccionario_operativos, talca_diccionario_inoperativos, talca_diccionario_semi
    global linares_diccionario_operativos, linares_diccionario_inoperativos, linares_diccionario_semi
    global cauquenes_diccionario_operativos, cauquenes_diccionario_inoperativos, cauquenes_diccionario_semi
    for _, raw in nombre.iterrows():

      if raw['COMUNA'] == "CURICO" or raw['COMUNA'] == 'ROMERAL' or raw['COMUNA'] == 'TENO' or raw['COMUNA'] == 'MOLINA' or raw['COMUNA'] == 'SAGRADA_FAMILIA' or raw['COMUNA'] == 'RAUCO' or raw['COMUNA'] == 'HUALAÑE' or raw['COMUNA'] == 'HUALANE' or raw['COMUNA'] == 'LICANTEN' or raw['COMUNA'] == 'VICHUQUEN' :

        if raw['OPERATIVIDAD_ESTABLECIMIENTO'] == 'INOPERATIVO':
          curico_inoperativos += 1
          curico_diccionario_inoperativos['curico'].append(raw['NOMBRE_ESTABLECIMIENTO'])

        elif raw['OPERATIVIDAD_ESTABLECIMIENTO'] == 'SEMIOPERATIVO':
          curico_semioperativos += 1
          curico_diccionario_semi['curico'].append(raw['NOMBRE_ESTABLECIMIENTO'])

        elif raw['OPERATIVIDAD_ESTABLECIMIENTO'] == 'OPERATIVO':
          curico_operativos += 1
          curico_diccionario_operativos['curico'].append(raw['NOMBRE_ESTABLECIMIENTO'])


      if raw['COMUNA'] == "TALCA" or raw['COMUNA'] =='EMPEDRADO' or raw['COMUNA'] =='PELARCO' or raw['COMUNA'] =='PENCAHUE' or raw['COMUNA'] =='RIO_CLARO' or raw['COMUNA'] =='SAN_CLEMENTE' or raw['COMUNA'] =='SAN_RAFAEL' or raw['COMUNA'] =='CONSTITUCION' or raw['COMUNA'] =='CUREPTO' or raw['COMUNA'] =='MAULE' :
        if raw['OPERATIVIDAD_ESTABLECIMIENTO'] == 'INOPERATIVO':
          talca_inoperativos += 1
          talca_diccionario_inoperativos['talca'].append(raw['NOMBRE_ESTABLECIMIENTO'])

        elif raw['OPERATIVIDAD_ESTABLECIMIENTO'] == 'SEMIOPERATIVO':
          talca_semioperativos += 1
          talca_diccionario_semi['talca'].append(raw['NOMBRE_ESTABLECIMIENTO'])
        elif raw['OPERATIVIDAD_ESTABLECIMIENTO'] == 'OPERATIVO':
          talca_operativos += 1
          talca_diccionario_operativos['talca'].append(raw['NOMBRE_ESTABLECIMIENTO'])

      if raw['COMUNA'] =="LINARES" or raw['COMUNA'] =='COLBUN' or raw['COMUNA'] =='LONGAVI' or raw['COMUNA'] =='PARRAL' or raw['COMUNA'] =='RETIRO' or raw['COMUNA'] =='SAN_JAVIER' or raw['COMUNA'] =='VILLA_ALEGRE' or raw['COMUNA'] =='YERBAS_BUENAS':
        if raw['OPERATIVIDAD_ESTABLECIMIENTO'] == 'INOPERATIVO':
          linares_inoperativos += 1
          linares_diccionario_inoperativos['linares'].append(raw['NOMBRE_ESTABLECIMIENTO'])

        elif raw['OPERATIVIDAD_ESTABLECIMIENTO'] == 'SEMIOPERATIVO':
          linares_semioperativos += 1
          linares_diccionario_semi['linares'].append(raw['NOMBRE_ESTABLECIMIENTO'])

        elif raw['OPERATIVIDAD_ESTABLECIMIENTO'] == 'OPERATIVO':
          linares_operativos += 1
          linares_diccionario_operativos['linares'].append(raw['NOMBRE_ESTABLECIMIENTO'])

      if  raw['COMUNA'] =="CAUQUENES" or raw['COMUNA'] =='CHANCO' or raw['COMUNA'] =='PELLUHUE':
        if raw['OPERATIVIDAD_ESTABLECIMIENTO'] == 'INOPERATIVO':
          cauquenes_inoperativos += 1
          cauquenes_diccionario_inoperativos['cauquenes'].append(raw['NOMBRE_ESTABLECIMIENTO'])

        elif raw['OPERATIVIDAD_ESTABLECIMIENTO'] == 'SEMIOPERATIVO':
          cauquenes_semioperativos += 1
          cauquenes_diccionario_semi['cauquenes'].append(raw['NOMBRE_ESTABLECIMIENTO'])

        elif raw['OPERATIVIDAD_ESTABLECIMIENTO'] == 'OPERATIVO':
          cauquenes_operativos += 1
          cauquenes_diccionario_operativos['cauquenes'].append(raw['NOMBRE_ESTABLECIMIENTO'])
    return None

  recolectar_datos_establecimientos(hospital)
  recolectar_datos_establecimientos(sur)
  recolectar_datos_establecimientos(sar)
  recolectar_datos_establecimientos(sapu)
  recolectar_datos_establecimientos(centro)
  recolectar_datos_establecimientos(comunitario)
  recolectar_datos_establecimientos(psr)
  datos['Provincias'].append('Curicó')
  datos['Operativos'].append(curico_operativos)
  datos['Inoperativos'].append(curico_inoperativos)
  datos['Semioperativos'].append(curico_semioperativos)

  datos['Provincias'].append('Talca')
  datos['Operativos'].append(talca_operativos)
  datos['Inoperativos'].append(talca_inoperativos)
  datos['Semioperativos'].append(talca_semioperativos)

  datos['Provincias'].append('Linares')
  datos['Operativos'].append(linares_operativos)
  datos['Inoperativos'].append(linares_inoperativos)
  datos['Semioperativos'].append(linares_semioperativos)

  datos['Provincias'].append('Cauquenes')
  datos['Operativos'].append(cauquenes_operativos)
  datos['Inoperativos'].append(cauquenes_inoperativos)
  datos['Semioperativos'].append(cauquenes_semioperativos)

  tabla = pd.DataFrame(datos)
  return tabla
