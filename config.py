from pydantic_settings import BaseSettings, SettingsConfigDict
import os

env_file_path = ".env.test" if os.getenv("ENV") == "test" else ".env"
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
    model_config = SettingsConfigDict(env_file=env_file_path, extra="allow")

    @property
    def database_url(self):
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()