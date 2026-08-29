from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    gemini_api_key: str = ""
    admin_password: str

    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")


settings = Settings()