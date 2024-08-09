from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/RemainderSystem"
Engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=Engine)

session = Session()

Base = declarative_base()

def init_db():
    Base.metadata.create_all(engine)