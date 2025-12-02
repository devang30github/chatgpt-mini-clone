from pydantic import  Field
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App
    ENV: str = Field("development", env="ENV")
    LOG_LEVEL: str = Field("info", env="LOG_LEVEL")

    # MongoDB
    MONGO_URI: str = Field(..., env="MONGO_URI")
    MONGO_DB: str = Field(env="MONGO_DB")

    # Uploads
    UPLOADS_PATH: str = Field("./data/uploads", env="UPLOADS_PATH")
    MAX_UPLOAD_SIZE_MB: int = Field(10, env="MAX_UPLOAD_SIZE_MB")
    USE_S3: bool = Field(False, env="USE_S3")

    # OpenAI / LLM
    OPENAI_API_KEY: Optional[str] = Field(None, env="OPENAI_API_KEY")
    LLM_MODEL: str = Field("gpt-4o", env="LLM_MODEL")

    # Embeddings
    EMBEDDING_MODEL: str = Field("sentence-transformers/all-mpnet-base-v2", env="EMBEDDING_MODEL")
    EMBEDDING_BATCH_SIZE: int = Field(32, env="EMBEDDING_BATCH_SIZE")
    EMBEDDING_DIM: int = Field(768, env="EMBEDDING_DIM")

    # Auth / JWT
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60*24*7, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# instantiate once and import
settings = Settings()
