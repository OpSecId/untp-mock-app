from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Settings(BaseSettings):
    PROJECT_TITLE: str = "orgbook-publisher"
    PROJECT_VERSION: str = "v0"

    DOMAIN: str = os.environ["DOMAIN"]
    SECRET_KEY: str = os.environ["SECRET_KEY"]
    AGENT_ENDPOINT: str = os.environ["AGENT_ENDPOINT"]
    ASKAR_DB: str = "sqlite://app.db"


settings = Settings()
