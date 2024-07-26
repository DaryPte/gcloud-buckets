# app_buckets.py
from flask import Flask, request, send_from_directory, abort,jsonify
import os
app = Flask(__name__)
import requests

from google.cloud import storage
import settings

DOWNLOAD_DIR = r'descargas'
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def list_bucket_contents_and_generate_urls(prefix):
    storage_client = storage.Client(credentials=settings.GS_CREDENTIALS)
    bucket = storage_client.bucket(settings.GS_BUCKET_NAME)

    blobs = bucket.list_blobs(prefix=prefix, max_results=3000)

    file_urls = []
    for blob in blobs:
        file_urls.append(blob.name)

    return file_urls

def download_file_from_api(file_name):
    url = f"http://34.86.255.76:5000/get-file?path={file_name}"
    print(f"Downloading {file_name} from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join(DOWNLOAD_DIR, file_name)
        # Crear directorios si no existen
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {file_name} to {file_path}")  # Mensaje de depuración
        return file_path
    else:
        print(f"Failed to download {file_name}, status code: {response.status_code}")  # Mensaje de depuración
        raise Exception(f"Failed to download file: {file_name}, status code: {response.status_code}")

@app.route('/list-files')
def list_files():
    try:
        prefix = 'media/AgendamientoCita/'
        file_urls = list_bucket_contents_and_generate_urls(prefix)
        downloaded_files = []
        errors = []
        for file_url in file_urls:
            try:
                downloaded_file = download_file_from_api(file_url)
                downloaded_files.append(downloaded_file)
            except Exception as e:
                errors.append({"file": file_url, "error": str(e)})
        return jsonify({"downloaded_files": downloaded_files, "errors": errors})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


BASE_DIR = '/home/daltamirano/bucket-sga'


@app.route('/get-file')
def get_file():
    # Obtiene la ruta del archivo desde los parámetros de la URL
    file_path = request.args.get('path')

    if not file_path:
        return "Error: No file path provided. Please specify a file path.", 400

    # Construye la ruta completa al archivo
    full_path = os.path.join(BASE_DIR, file_path)

    # Verifica si el archivo existe
    if not os.path.exists(full_path):
        abort(404, description="File not found")

    # Devuelve el archivo
    return send_from_directory(BASE_DIR, file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

