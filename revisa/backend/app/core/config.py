from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Vet Clinic API"
    database_url: str
    db_ssl: bool = True
    cors_origins: str = "http://localhost:4200"

    # JWT (SECRET_KEY es obligatoria: no hay valor por defecto a propósito)
    secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()