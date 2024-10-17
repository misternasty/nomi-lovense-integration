# # # # # # # # # 
# # models.py # # 
# # # # # # # # # 
from sqlalchemy import Column, String, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    uid = Column(String, primary_key=True)
    data = Column(JSON)