from sqlmodel import Session, SQLModel, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


# Create database and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# def init_db():
#     with engine.begin() as connection:
#         connection.run(SQLModel.metadata.create_all)
#         SQLModel.metadata.create_all(engine)


# Dependency to get a session
def get_session() -> Session:
    with Session(engine) as session:
        yield session
