# app_buckets.py
from flask import Flask
from flask import Flask, request, send_from_directory, abort
import os
app = Flask(__name__)

from google.cloud import storage
from settings import GS_CREDENTIALS

def generate_signed_url(blob_name, expiration=3600):
    storage_client = storage.Client(credentials=settings.GS_CREDENTIALS)
    bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(seconds=expiration),
        method="GET",
    )
    return url


@app.route('/')
def hello_world():
    client = storage.Client(credentials=GS_CREDENTIALS)
    bucket = client.get_bucket('bucket-sga')
    # bucket = client.bucket('bucket-sga')

    # link = bucket.blob(f'media/chayanne.png')
    # link = generate_signed_url("media/Imagen/2022/05/03/estadohelpdesk_20225316361.png")
    link = generate_signed_url("media/03.jpg")

    return f"Archivos en el bucket: {link}"



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
    app.run(host='0.0.0.0', port=5000)

