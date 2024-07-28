from flask import Flask, jsonify
import os
import requests
import json

app = Flask(__name__)

DOWNLOAD_DIR = r'descargas'
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def download_file(url, file_name):
    response = requests.get(url)
    response.raise_for_status()  # Verificar si la solicitud fue exitosa
    file_path = os.path.join(DOWNLOAD_DIR, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path

@app.route('/download-files', methods=['GET'])
def download_files_route():
    json_file_name = './archivo.json'  # Asegúrate de que este archivo JSON está en el mismo directorio que tu script Flask

    try:
        # Leer el archivo JSON localmente
        with open(json_file_name, 'r') as json_file:
            json_data = json.load(json_file)

        file_urls = json_data

        if not file_urls:
            return jsonify({'error': 'No se encontraron URLs en el archivo JSON'}), 400

        for file_url in file_urls:
            # Ajustar la ruta eliminando el primer segmento "/mnt/disk/descargas/media/"
            base_path = "/mnt/disk/descargas/"
            if file_url.startswith(base_path):
                file_url = file_url[len(base_path):]

            # Reconstruir la URL completa para GCS
            gcs_url = f"https://storage.googleapis.com/bucket-sga/{file_url}"

            # Descargar el archivo desde la URL y guardarlo en la carpeta de descargas
            download_file(gcs_url, file_url)

        return jsonify({'message': 'Todos los archivos se han descargado correctamente.'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
