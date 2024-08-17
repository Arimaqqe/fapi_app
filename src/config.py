from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_host: str
    redis_port: int

    model_config = {
        "env_file": ".env"
    }


settings = Settings()
