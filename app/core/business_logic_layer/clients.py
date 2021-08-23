from decimal import Decimal
from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app.core.utils.get_entity import get_entity_instance
from app.crud.clients import clients_crud
from app.models.clients import Clients
from app.schemas.v1.client import ClientBase
from app.schemas.v1.client import ClientCreate
from app.schemas.v1.client import ClientQueryParams
from app.schemas.v1.client import ClientUpdate


def check_phone_number_duplication(db: Session, client: ClientBase) -> None:
    query = ClientQueryParams(phone_number=client.phone_number)
    found_by_phone_number = clients_crud.find_clients(db=db, query=query)
    if found_by_phone_number:
        raise HTTPException(
            status_code=400,
            detail="client with this phone number already exists",
        )


def bl_create_client(db: Session, client: ClientCreate) -> Any:
    check_phone_number_duplication(db, client)
    return clients_crud.create(db, obj_in=client)


def bl_update_client(
    db: Session, client_id: int, update_client: ClientUpdate
) -> Any:
    if (
        update_client.wallet_balance is not None
        and update_client.wallet_balance >= Decimal("0.0")
    ):
        raise HTTPException(
            status_code=400,
            detail="wallet update operation is prohibited, "
            "use operations to change wallet balance",
        )
    check_phone_number_duplication(db, update_client)
    client: Clients = get_entity_instance(db, clients_crud, client_id)
    return clients_crud.update(db, db_obj=client, obj_in=update_client)
