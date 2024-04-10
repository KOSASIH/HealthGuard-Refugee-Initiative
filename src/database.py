from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection string
DATABASE_URI = "postgresql://username:password@localhost/dbname"

# Create an engine for the database connection
engine = create_engine(DATABASE_URI)

# Create a session factory for the engine
Session = sessionmaker(bind=engine)

# Create a declarative base for the models
Base = declarative_base()

# Connect to the database and create the schema if it doesn't exist
engine.connect()
Base.metadata.create_all(engine)
