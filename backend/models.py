from sqlalchemy import Column, Integer, String, Text, ARRAY, Float
from .database import Base

class Document(Base):
    __tablename__='documents'

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    content = Column(Text)
    page_number = Column(String)
    meaning = Column(ARRAY(Float), nullable = True)
