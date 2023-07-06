from sqlalchemy import ForeignKey, create_engine, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy import String, Integer, MetaData, Table
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, Session
from sqlalchemy.orm import mapped_column
from config import get_settings
from my_exeptions import UncorrectForeignKeyExeptions


settings = get_settings()


class Base(DeclarativeBase):
    pass


class TableFiles(Base):
    __tablename__ = 'files'

    id: Mapped[int] = mapped_column(primary_key=True)
    file_type: Mapped[str] = mapped_column(String(20))
    url: Mapped[str] = mapped_column(String(20))

    def __repr__(self) -> str:
        return f"files(id={self.id!r}, file_type={self.file_type!r}, url={self.url!r})"


class TableAvatars(Base):
    __tablename__ = 'avatars'

    id: Mapped[int] = mapped_column(primary_key=True)
    file_id: Mapped[int] = mapped_column(ForeignKey('files.id'))
    size: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"avatars(id={self.id!r}, files_id={self.files_id!r}, size={self.size!r})"


def create_tables():
    engine = create_engine(
        f'mysql+pymysql://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}'
    )
    Base.metadata.create_all(engine)


class DbTools():
    def __init__(self, user, password, host, db_name) -> None:
        self.engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{db_name}')
        # self.files_table = TableFiles()
        # self.avatars_table = TableAvatars()
        # self.Session = sessionmaker(bind=self.engine)
        # create_tables()

    def add_row_to_files_table(self, file_type: str, url: str) -> int:
        new_file = TableFiles(file_type=file_type, url=url)
        result = None
        with Session(self.engine) as session:
            session.add(new_file)
            session.commit()
            result = new_file.id
        return result



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

    def add_row_to_avatars_table(self, file_id: str, size: int) -> int:
        new_avatar = TableAvatars(file_id=file_id, size=size)
        result = None
        try:
            with Session(self.engine) as session:
                session.add(new_avatar)
                session.commit()
                result = new_avatar.id
        except IntegrityError:
            raise UncorrectForeignKeyExeptions()
        return result
