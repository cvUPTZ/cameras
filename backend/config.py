import os
from dotenv import load_dotenv

load_dotenv()

ROBOFLOW_API_KEY = os.getenv('ROBOFLOW_API_KEY')
MODEL_WORKSPACE = os.getenv('ROBOFLOW_WORKSPACE')
MODEL_NAME = os.getenv('ROBOFLOW_MODEL')
MODEL_VERSION = os.getenv('ROBOFLOW_VERSION', '1')

CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', '0.5'))
OVERLAP_THRESHOLD = float(os.getenv('OVERLAP_THRESHOLD', '0.5'))
DB_AUTH_TOKEN=os.getenv('DB_AUTH_TOKEN')
