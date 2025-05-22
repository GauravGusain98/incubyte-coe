from pydantic_settings import BaseSettings, SettingsConfigDict
import os

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
    model_config = SettingsConfigDict(env_file=".env")

    @property
    def database_url(self):
        print(os.getenv("DATABASE_URL"))
        if os.getenv("DATABASE_URL"):
            return os.getenv("DATABASE_URL")

        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()