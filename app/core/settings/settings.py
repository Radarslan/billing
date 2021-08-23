import os
from decimal import Decimal

from pydantic import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "billing")
    API_VERSION: str = "/api/v1"
    BACKEND_CORS_ORIGINS: str = os.getenv("BACKEND_CORS_ORIGINS", "*")
    SQLALCHEMY_DATABASE_URI: str = PostgresDsn.build(
        scheme="postgresql",
        user=os.getenv("DATABASE_USERNAME", "postgres"),
        password=os.getenv("DATABASE_PASSWORD", "postgres"),
        host=os.getenv("DATABASE_HOST", "127.0.0.1"),
        port=os.getenv("DATABASE_PORT", "5000"),
        path=f"/{os.getenv('DATABASE_NAME', 'postgres')}",
    )


class DataValidation(BaseSettings):

    # client
    names_minimum_length = 1
    first_name_maximum_length = 50
    last_name_maximum_length = 100
    find_phone_number_minimum_length = 2
    phone_number_minimum_length = 10
    phone_number_maximum_length = 10
    wallet_maximum_number_of_digits = 14
    wallet_maximum_number_of_decimal_places = 2
    wallet_minimum_amount = Decimal("10.00")
    wallet_maximum_amount = Decimal("999999999999.99")

    # operations
    transfer_maximum_number_of_digits = 6
    transfer_maximum_number_of_decimal_places = 2
    transfer_minimum_amount = Decimal("10.00")
    transfer_maximum_amount = Decimal("9999.99")


settings = Settings()
data_validation = DataValidation()
