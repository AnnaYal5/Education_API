from pydantic_settings import BaseSettings
from pathlib import Path

class AppConfig(BaseSettings):
    secret_key: str
    ai_model: str
    ai_api_key: str
    conspect_system_prompt: str = ""
    test_system_prompt: str = ""

    class Config:
        env_file = Path(__file__).parent / ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **data):
        super().__init__(**data)
        prompt_conspect_file = Path(__file__).parent / "AI" / "prompts" / "conspect_prompt.txt"
        prompt_test_file = Path(__file__).parent / "AI" / "prompts" / "test_prompt.txt"
        if prompt_conspect_file.exists():
            with open(prompt_conspect_file, "r", encoding="utf-8") as f:
                self.conspect_system_prompt = f.read()

        if prompt_test_file.exists():
            with open(prompt_test_file, "r", encoding="utf-8") as f:
                self.test_system_prompt = f.read()

config = AppConfig()