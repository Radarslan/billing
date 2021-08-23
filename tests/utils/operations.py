from random import uniform
from typing import Any
from typing import Dict

from sqlalchemy.orm import Session  # type: ignore

from app.core.settings.settings import data_validation
from app.crud.operations import operations_crud
from app.models.clients import Clients
from app.models.operations import Operations
from tests.utils.common import get_random_date_string


def create_random_operation_dict(
    benefactor: Clients = None, beneficiary: Clients = None
) -> Dict[str, Any]:
    return {
        "benefactor_client_id": (
            None if benefactor is None else benefactor.id
        ),
        "beneficiary_client_id": (
            None if beneficiary is None else beneficiary.id
        ),
        "transfer_amount": round(
            uniform(
                float(data_validation.transfer_minimum_amount) + 10.00,
                float(data_validation.transfer_maximum_amount),
            ),
            data_validation.transfer_maximum_number_of_decimal_places,
        ),
        "operation_date": get_random_date_string(),
        "is_active": True,
    }


def create_random_operation(db: Session, operation_dict: dict) -> Operations:
    return operations_crud.create(db=db, obj_in=operation_dict)
