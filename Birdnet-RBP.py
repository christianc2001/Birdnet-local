import pandas as pd
import threading
import datetime as dt
import config as cfg
import sounddevice as sd
from scipy.io.wavfile import write
import os

def verificar_y_crear_directorio(ruta_directorio):

    # Verificar si el directorio ya existe
    if not os.path.exists(ruta_directorio):
        try:
            # Intentar crear el directorio si no existe
            os.makedirs(ruta_directorio)
            print(f"Directorio '{ruta_directorio}' creado exitosamente.")
        except OSError as error:
            print(f"Error al crear el directorio '{ruta_directorio}': {error}")
    else:
        print(f"El directorio '{ruta_directorio}' ya existe.")

def grabar_audio(nombre_archivo, duracion=10):
    
    print(f"Grabando audio por {duracion} segundos...")

    # Configurar la grabación
    sr = cfg.SAMPLE_RATE 
    recording = sd.rec(int(duracion * sr), samplerate=sr, channels=2)
    sd.wait()

    # Guardar la grabación en un archivo WAV
    nombre_completo = f"recordings/{nombre_archivo}.wav"
    write(nombre_completo, sr, recording)

    print(f"Audio guardado como {nombre_completo}")

def borrar_audio(nombre_archivo):
    
    try:
        os.remove(f"recordings/{nombre_archivo}.wav")
        print(f"Archivo {nombre_archivo}.wav eliminado.")
    except FileNotFoundError:
        print(f"Archivo {nombre_archivo}.wav no encontrado.")

def borrar_archivos_si_no_cumplen_condicion(input_file, columna, valor_umbral):
    
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"El archivo {input_file} no fue encontrado.")
        return False  

    # Verificar si las columnas especificadas existen en el DataFrame
    if columna not in df.columns or 'Filename' not in df.columns:
        print("Una o ambas columnas especificadas no existen en el archivo CSV.")
        return False

    # Iterar sobre cada fila del DataFrame
    for index, row in df.iterrows():
        archivo = row['Filename']
        condicion = row[columna]

        # Verificar la condición
        if condicion < valor_umbral:
            # Eliminar el archivo si no cumple la condición
            if os.path.exists(archivo):
                os.remove(archivo)
                print(f"Se ha eliminado el archivo '{archivo}' porque '{columna}' < {valor_umbral}.")

    return True

# Creación de los directorios para grabaciones e inferencias

verificar_y_crear_directorio("recordings")
verificar_y_crear_directorio("inferences")

# Creación del archivo CSV para guardar los resultados de las inferencias

header = "Filename,Start (s),End (s),Scientific name,Common name,Confidence\n"
resultsPath = "inferences/results.csv"

if os.path.dirname(resultsPath):
    os.makedirs(os.path.dirname(resultsPath), exist_ok=True)

with open(resultsPath, "w", encoding="utf-8") as rfile:
    rfile.write(header)

# Definición del hilo para las inferencias en simultanea con la grabación
    
def inference():
    comando_a_ejecutar = f"python3 analyze.py --i recordings/{nombre_archivo}.wav --o {resultsPath} --locale es --rtype csv --min_conf 0.5"
    os.system(comando_a_ejecutar) 

    borrar_archivos_si_no_cumplen_condicion(resultsPath, 'Confidence', 0.8)

# Hilo principal de ejecución que graba audios de N segundos

def run():

    global nombre_archivo
    
    while True:

        current_date = dt.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

        nombre_archivo = str(current_date)    
        duracion_grabacion = 10

        grabar_audio(nombre_archivo, duracion_grabacion)

        p = threading.Thread(target=inference)
        p.start()


def main():
    run()

if __name__ == "__main__":
    main()