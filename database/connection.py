from config import DevConfig
from sqlmodel import SQLModel, Session, create_engine

engine_url = create_engine(DevConfig.database_connection_string, echo=True)

def conn():
	"""
	The conn function is responsible for creating the database tables
 	"""
	SQLModel.metadata.create_all(engine_url)


def get_session():
	"""
	This provides a session object that can be used for database operations within a context. 
	These functions can be called when needed to perform database-related tasks.
	"""
	with Session(engine_url) as session:
		yield session

