from .database import Base # This is to import Base class model from database file'
from sqlalchemy import Boolean, Column, Integer, String # This is to import column which can be sed to create columns in the postgres database
from sqlalchemy.sql.expression import null,text
from sqlalchemy.sql.sqltypes import TIMESTAMP


#### SQL alchemy model (ORM Model)
# Diff between ORM and Pydantic model --> pydantic model is the model is which used to receive information format from the user 
# whereas ORM model is the model defined to build a database

class Post(Base):
    __tablename__ = 'posts'  # Table name to be created in postgres sql
    # <Columnname> = column(<DataType>, primary_key = <Boolean>, nullable = <boolean>)
    # In the above command the user need to se column name, datatype, Primary_key, is_null etc
    id = Column(Integer ,primary_key=True, nullable=False)  
    title = Column(String, nullable=False)    
    content = Column(String, nullable=False)    
    published = Column(Boolean, nullable=True,server_default= 'TRUE')    
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

# class User(Base):
#     __tablename__ = "Users"
#     id = 
