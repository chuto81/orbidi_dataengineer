import os
from dotenv import load_dotenv

# API Config
load_dotenv()
API_URL = 'https://api.clickup.com/api/v2/list/{list_id}/task'
API_KEY = os.environ['API_KEY']

# Dict of ID's list
dict_list_id = {
    'clientes':'900100953154',
    'kd-web': '900100953291',
    'kd-seo': '900100953296',
    'kd-rrss': '900100953297'
    }

# Database Config
dict_database_config = {
    'DB_USER':'migutie',
    'DB_PASSWORD':'123456',
    'DB_HOST':'127.0.0.1',
    'DB_PORT':'5432',
    'DB_NAME':'postgreSQL_database',
}

# ETL Config
ETL_BATCH_SIZE = 1000
ETL_DATE_FORMAT = '%Y-%m-%d'