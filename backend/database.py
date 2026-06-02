import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
load_dotenv()



DATABASE_URL = (

f"mysql+pymysql://"

f"{os.getenv('MYSQLUSER')}:"

f"{os.getenv('MYSQLPASSWORD')}@"

f"{os.getenv('MYSQLHOST')}:"

f"{os.getenv('MYSQLPORT')}/"

f"{os.getenv('MYSQLDATABASE')}"

)



engine = create_engine(
DATABASE_URL

)


SessionLocal = sessionmaker(
autocommit=False,
autoflush=False,
bind=engine

)


Base = declarative_base()