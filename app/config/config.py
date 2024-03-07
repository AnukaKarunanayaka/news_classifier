import os

from dotenv import load_dotenv

load_dotenv('.env')

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
