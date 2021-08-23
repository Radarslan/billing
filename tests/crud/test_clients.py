from decimal import Decimal

from sqlalchemy.orm import Session  # type: ignore

from app.crud.clients import clients_crud
from app.models.clients import Clients as ClientModel
from app.schemas.v1.client import ClientQueryParams


def test_create_clients(db: Session, benefactor_dict: dict) -> None:
    client = clients_crud.create(db=db, obj_in=benefactor_dict)
    assert benefactor_dict.get("first_name", None) == client.first_name
    assert benefactor_dict.get("last_name", None) == client.last_name
    assert benefactor_dict.get("phone_number", None) == client.phone_number
    assert (
        Decimal(str(benefactor_dict.get("wallet_balance", 0.0)))
        == client.wallet_balance
    )


def test_find_clients(db: Session, benefactor: ClientModel) -> None:

    query = ClientQueryParams(
        first_name=benefactor.first_name[1:3],
        last_name=benefactor.last_name[1:3],
        phone_number=benefactor.phone_number[2:6],
    )
    clients = clients_crud.find_clients(db=db, query=query)
    found = False
    for client in clients:
        if (
            benefactor.first_name == client.first_name
            and benefactor.last_name == client.last_name
            and benefactor.phone_number == client.phone_number
        ):
            found = True

    assert found


def test_read_clients(db: Session, benefactor: ClientModel) -> None:
    clients = clients_crud.read_many(db=db)
    for client in clients:
        assert isinstance(client, ClientModel)


def test_read_client(db: Session, benefactor: ClientModel) -> None:
    client = clients_crud.read(db=db, entity_id=benefactor.id)
    assert client is not None
    assert benefactor.id == client.id
    assert benefactor.first_name == client.first_name
    assert benefactor.last_name == client.last_name
    assert benefactor.phone_number == client.phone_number
    assert benefactor.wallet_balance == client.wallet_balance


def test_update_client(
    db: Session, benefactor: ClientModel, benefactor_dict: dict
) -> None:
    client = clients_crud.update(
        db=db, db_obj=benefactor, obj_in=benefactor_dict
    )
    assert benefactor.id == client.id
    assert benefactor_dict.get("first_name", None) == client.first_name
    assert benefactor_dict.get("last_name", None) == client.last_name
    assert benefactor_dict.get("phone_number", None) == client.phone_number
    assert (
        Decimal(str(benefactor_dict.get("wallet_balance", 0.0)))
        == client.wallet_balance
    )


def test_delete_client(db: Session, benefactor: ClientModel) -> None:
    client = clients_crud.delete(db=db, entity_id=benefactor.id)
    assert client is not None
    assert benefactor.id == client.id
    assert benefactor.first_name == client.first_name
    assert benefactor.last_name == client.last_name
    assert benefactor.phone_number == client.phone_number
    assert benefactor.wallet_balance == client.wallet_balance
