from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_ASMI: str
    DB_TM: str
    API_URL: str

    @property
    def ASMI_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_ASMI}"

    @property
    def TM_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_TM}"

    @property
    def API_URL(self) -> str:
        return self.API_URL

    model_config = SettingsConfigDict(env_file=".env-non-dev")


settings = Settings()
