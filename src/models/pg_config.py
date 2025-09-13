from pydantic import BaseModel


class PGConfig(BaseModel):
    host: str
    dbname: str
    user: str
    password: str
    port: int
