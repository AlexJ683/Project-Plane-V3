from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_Database =  "mysql+pymysql://admin:Password@planes.cfsqco2gobb2.eu-north-1.rds.amazonaws.com:3306/planes"

engine = create_engine(URL_Database)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


