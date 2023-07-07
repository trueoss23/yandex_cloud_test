from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, Session
from sqlalchemy.orm import mapped_column
from config import get_settings
from common.my_exeptions import UncorrectForeignKeyExeptions


settings = get_settings()


class Base(DeclarativeBase):
    pass


class TableFiles(Base):
    __tablename__ = 'files'

    id: Mapped[int] = mapped_column(primary_key=True)
    file_type: Mapped[str] = mapped_column(String(40))
    url: Mapped[str] = mapped_column(String(256))

    def __repr__(self) -> str:
        return f"files(id={self.id!r}, file_type={self.file_type!r}, url={self.url!r})"


class TableAvatars(Base):
    __tablename__ = 'avatars'

    id: Mapped[int] = mapped_column(primary_key=True)
    file_id: Mapped[int] = mapped_column(ForeignKey('files.id'))
    size: Mapped[str] = mapped_column(String(20))
    url: Mapped[str] = mapped_column(String(256))

    def __repr__(self) -> str:
        return f"avatars(id={self.id!r}, files_id={self.files_id!r}, size={self.size!r}, url={self.url!r})"


def create_tables():
    engine = create_engine(
        f'mysql+pymysql://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}'
    )
    Base.metadata.create_all(engine)


class DbTools():
    def __init__(self, user, password, host, db_name) -> None:
        self.engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{db_name}')
        create_tables()

    def add_row_to_files_table(self, file_type: str, url: str) -> int | None:
        new_file = TableFiles(file_type=file_type, url=url)
        result = None
        with Session(self.engine) as session:
            session.add(new_file)
            session.commit()
            result = new_file.id
        return result

    def add_row_to_avatars_table(self,
                                 file_id: str,
                                 size: int,
                                 url: str) -> int | None:
        new_avatar = TableAvatars(file_id=file_id, size=size, url=url)
        result = None
        try:
            with Session(self.engine) as session:
                session.add(new_avatar)
                session.commit()
                result = new_avatar.id
        except IntegrityError:
            raise UncorrectForeignKeyExeptions()
        return result
