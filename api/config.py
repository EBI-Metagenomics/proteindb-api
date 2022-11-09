from pydantic import BaseSettings


class Settings(BaseSettings):
    mysql_host: str
    mysql_port: str
    mysql_db: str
    mysql_user: str
    mysql_pass: str

    class Config:
        env_file = ".env"
