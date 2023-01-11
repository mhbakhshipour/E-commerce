from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_PORT: int = None
    DATABASE_PASSWORD: str = None
    DATABASE_USER: str = None
    DATABASE_DB: str = None
    DATABASE_HOST: str = None
    DATABASE_HOSTNAME: str = None

    JWT_PUBLIC_KEY: str = None
    JWT_PRIVATE_KEY: str = None
    REFRESH_TOKEN_EXPIRES_IN: int = None
    ACCESS_TOKEN_EXPIRES_IN: int = None
    JWT_ALGORITHM: str = None

    CLIENT_ORIGIN: str = None

    class Config:
        env_file = ".env"


settings = Settings()
