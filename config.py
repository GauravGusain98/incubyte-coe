import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


env = os.getenv("ENV", "development")
if env == "test":
    print('here')
    load_dotenv(".env.test", override=True)
else:
    print('here 1')
    load_dotenv(".env", override=True)

env_file_path = ".env.test" if env == "test" else ".env"

class Settings(BaseSettings):
    app_name: str = "COE FastAPI App"
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    allowed_origins: str
    model_config = SettingsConfigDict(env_file=env_file_path, extra="allow")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Converting comma separated allowed origins from .env to list
        if isinstance(self.allowed_origins, str):
            self.allowed_origins = [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]

    @property
    def database_url(self):
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()