from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, MetaData, insert, select, delete
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

class Database():

    def __init__(self, name):
        self.engine = create_engine(f'sqlite:///{name}')
        self.meta = MetaData()
        self.table = None

    def create_table(self):
        Base = declarative_base()

        class Users(Base):
            __tablename__="users"
            num = Column(Integer, primary_key=True, autoincrement=True)
            id = Column(Integer, unique=True)
        
        Base.metadata.create_all(self.engine)

        self.table = Users
    
    def insert_user(self, id_):
        query = insert(self.table).values({"id": id_})
        del_query = delete(self.table).where(self.table.id == id_)
        with self.engine.connect() as con:
            try:
                con.execute(query)
            except:
                con.execute(del_query)
                con.execute(query)
            con.commit()
            con.close()
            

    def get_users(self):
        query = select(self.table.id)
        with self.engine.connect() as con:
            res = con.execute(query)
            con.close()
            return res
    
    