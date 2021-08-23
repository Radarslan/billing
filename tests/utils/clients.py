from random import randint
from random import uniform
from typing import Any
from typing import Dict

from sqlalchemy.orm import Session  # type: ignore

from app.core.business_logic_layer.clients import bl_create_client
from app.core.settings.settings import data_validation
from app.models.clients import Clients
from app.schemas.v1.client import ClientCreate
from tests.utils.common import get_random_lower_string
from tests.utils.common import get_random_numeric_string


def create_random_client_dict() -> Dict[str, Any]:
    return {
        "first_name": get_random_lower_string(
            randint(
                data_validation.names_minimum_length + 2,
                data_validation.first_name_maximum_length,
            )
        ),
        "last_name": get_random_lower_string(
            randint(
                data_validation.names_minimum_length + 2,
                data_validation.last_name_maximum_length,
            )
        ),
        "phone_number": get_random_numeric_string(
            randint(
                data_validation.phone_number_minimum_length,
                data_validation.phone_number_maximum_length,
            )
        ),
        "wallet_balance": round(
            uniform(
                float(data_validation.wallet_minimum_amount) + 10.00,
                float(data_validation.wallet_maximum_amount) / 10000000,
            ),
            data_validation.wallet_maximum_number_of_decimal_places,
        ),
    }


def create_random_client(db: Session, client_dict: dict) -> Clients:
    client = ClientCreate(**client_dict)
    return bl_create_client(db=db, client=client)
