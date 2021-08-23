from decimal import Decimal

from starlette.testclient import TestClient

from app.core.settings.settings import settings
from app.models.clients import Clients as ClientModel
from app.schemas.v1.client import Client


def test_create_clients(
    test_client: TestClient, benefactor_dict: dict
) -> None:
    response = test_client.post(
        f"{settings.API_VERSION}/clients/", json=benefactor_dict
    )
    if response.status_code == 400:
        assert (
            response.json().get("detail", None)
            == "client with this phone number already exists"
        )
    else:
        assert response.status_code == 201
        assert benefactor_dict.get("first_name", None) == response.json().get(
            "first_name", None
        )
        assert benefactor_dict.get("last_name", None) == response.json().get(
            "last_name", None
        )
        assert benefactor_dict.get(
            "phone_number", None
        ) == response.json().get("phone_number", None)
        assert benefactor_dict.get(
            "wallet_balance", None
        ) == response.json().get("wallet_balance", 0.0)


def test_find_clients(
    test_client: TestClient, benefactor: ClientModel
) -> None:
    params = {
        "first_name": benefactor.first_name[1:3],
        "last_name": benefactor.last_name[1:3],
        "phone_number": benefactor.phone_number[2:6],
    }
    response = test_client.get(
        url=f"{settings.API_VERSION}/clients/", params=params
    )
    assert response.status_code == 200
    found = False
    for client in response.json():
        Client(**client)
        if (
            benefactor.first_name == client.get("first_name", None)
            and benefactor.last_name == client.get("last_name", None)
            and benefactor.phone_number == client.get("phone_number", None)
        ):
            found = True

    assert found


def test_read_client(
    test_client: TestClient, benefactor: ClientModel
) -> None:
    response = test_client.get(
        f"{settings.API_VERSION}/clients/{benefactor.id}"
    )
    assert response.status_code == 200
    assert benefactor.id == response.json().get("id", None)
    assert benefactor.first_name == response.json().get("first_name", None)
    assert benefactor.last_name == response.json().get("last_name", None)
    assert benefactor.phone_number == response.json().get(
        "phone_number", None
    )
    assert benefactor.wallet_balance == Decimal(
        str(response.json().get("wallet_balance", 0.0))
    )


def test_update_client(
    test_client: TestClient, benefactor: ClientModel, benefactor_dict: dict
) -> None:
    del benefactor_dict["wallet_balance"]
    response = test_client.put(
        f"{settings.API_VERSION}/clients/{benefactor.id}",
        json=benefactor_dict,
    )

    if response.status_code == 400:
        assert (
            response.json().get("detail", None)
            == "client with this phone number already exists"
            or response.json().get("detail", None)
            == "wallet update operation is prohibited, "
            "use operations to change wallet balance"
        )
    else:
        assert response.status_code == 200
        assert benefactor.id == response.json().get("id", None)
        assert benefactor_dict.get("first_name", None) == response.json().get(
            "first_name", None
        )
        assert benefactor_dict.get("last_name", None) == response.json().get(
            "last_name", None
        )
        assert benefactor_dict.get(
            "phone_number", None
        ) == response.json().get("phone_number", None)
        assert benefactor.wallet_balance == Decimal(
            str(response.json().get("wallet_balance", 0.0))
        )


def test_delete_client(
    test_client: TestClient, benefactor: ClientModel
) -> None:
    response = test_client.delete(
        f"{settings.API_VERSION}/clients/{benefactor.id}"
    )
    assert response.status_code == 200
    assert benefactor.id == response.json().get("id", None)
    assert benefactor.first_name == response.json().get("first_name", None)
    assert benefactor.last_name == response.json().get("last_name", None)
    assert benefactor.phone_number == response.json().get(
        "phone_number", None
    )
    assert benefactor.wallet_balance == Decimal(
        str(response.json().get("wallet_balance", 0.0))
    )
