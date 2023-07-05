from sqlalchemy import create_engine, Integer, String, Column, Table
from sqlalchemy import MetaData, insert, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql


Base = declarative_base()


class TableFiles(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    type = Column(String(20))
    url = Column(String(255))


class TableAvatars(Base):
    __tablename__ = 'avatars'

    id = Column(Integer, primary_key=True)
    files_id = Column(ForeignKey('files.id'), )
    type = Column(String(20))
    size = Column(Integer)


class DbTools():
    def __init__(self, user, password, host, db_name) -> None:
        self.engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{db_name}')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.files_table = TableFiles()
        self.avatars_table = TableAvatars()

    def add_new_row_in_files(self, new_row: TableFiles):
        self.session.add(new_row)
        self.session.commit()
        return new_row.id

    def add_new_row_in_avatars(self, new_row: TableAvatars):
        self.session.add(new_row)
        self.session.commit()
        return new_row.id

    def get_list_table(self, table_name):
        meta = MetaData()
        table = Table(table_name,
                      meta,
                      autoload_with=self.engine,
                      mysql_autoload=True)
        with self.engine.connect() as conn:
            select_query = table.select()
            result = conn.execute(select_query)
            rows = result.fetchall()
            return rows

    def delete_row(self, id_, table):
        condition = self.table.c.id == id_
        delete_statement = self.task_table.delete().where(condition)
        with self.engine.connect() as conn:
            conn.execute(delete_statement)
