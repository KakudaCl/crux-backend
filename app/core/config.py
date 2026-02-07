"""
Application Configuration
環境変数から設定を読み込み、アプリケーション全体で使用する設定を管理
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """アプリケーション設定クラス"""
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://crux_user:crux_password@localhost:5432/crux_db"
    
    # Application Configuration
    APP_NAME: str = "CRUX Backend API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080"
    ]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# グローバル設定インスタンス
settings = Settings()
