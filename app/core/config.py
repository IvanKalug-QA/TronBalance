from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret: str
    trongrid_api_key: str
    test_wallet: str

    class Config:
        env_file = '.env'


settings = Settings()
