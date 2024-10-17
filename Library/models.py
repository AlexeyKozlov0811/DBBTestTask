from sqlmodel import Field, SQLModel


class Books(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)

