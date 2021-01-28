from pydantic import BaseSettings


class Settings(BaseSettings):
    docker_host: str
    docker_registry: str
    mysql_server: str
    mysql_database: str
    mysql_user: str
    mysql_password: str
    warm_duration: int
    purge_every: int
