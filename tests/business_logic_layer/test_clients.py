from decimal import Decimal

from sqlalchemy.orm import Session  # type: ignore

from app.core.business_logic_layer.clients import bl_create_client
from app.schemas.v1.client import ClientCreate


def test_create_client(db: Session, benefactor_dict: dict) -> None:
    client = ClientCreate(**benefactor_dict)
    created_client = bl_create_client(db=db, client=client)
    assert (
        benefactor_dict.get("first_name", None) == created_client.first_name
    )
    assert benefactor_dict.get("last_name", None) == created_client.last_name
    assert (
        benefactor_dict.get("phone_number", None)
        == created_client.phone_number
    )
    assert (
        Decimal(str(benefactor_dict.get("wallet_balance", 0.0)))
        == created_client.wallet_balance
    )
