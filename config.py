import os
from dotenv import load_dotenv, find_dotenv

class DevConfig:
	load_dotenv(find_dotenv())
	user = os.environ.get('POSTGRES_USER')
	password = os.environ.get('POSTGRES_PASSWORD')
	database_name = os.environ.get('POSTGRES_DB')
	SECRET_KEY = os.environ.get('SECRET_KEY')	
	AWS_ID = os.environ.get('AWS_ID')
	AWS_KEY = os.environ.get('AWS_KEY')
	database_connection_string = f"postgresql://{user}:{password}@172.18.0.2:5432/{database_name}"
	dotenv_path = find_dotenv()
	if dotenv_path:
		load_dotenv(dotenv_path)
		os.remove(dotenv_path)
