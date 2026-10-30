
import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    APP_NAME = os.getenv(
        "APP_NAME",
        "Banking Complaint App"
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///bank_complaint.db"
    )


settings = Settings()
