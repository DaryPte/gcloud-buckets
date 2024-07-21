# settings.py
from google.oauth2 import service_account


#DEFAULT_FILE_STORAGE = 'custom_storages.GoogleCloudMediaStorage'
GS_BUCKET_NAME = 'bucket-sga'
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    './conf/sga-unemi-cxu-b85a58b12cb2.json'
)
GS_PROJECT_ID = 'sga-unemi-cxu'
GS_DEFAULT_ACL = 'publicRead'

MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/media/'