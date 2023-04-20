import os
from dotenv import load_dotenv

# API Config
load_dotenv()
API_URL = 'https://api.clickup.com/api/v2/list/{list_id}/task'
API_KEY = os.environ['API_KEY']

# Database Config
DB_HOST = 'localhost'
DB_NAME = 'my_database'
DB_USER = 'my_username'
DB_PASSWORD = 'my_password'

# ETL Config
ETL_BATCH_SIZE = 1000
ETL_DATE_FORMAT = '%Y-%m-%d'