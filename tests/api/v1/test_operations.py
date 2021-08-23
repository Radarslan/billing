from decimal import Decimal

from sqlalchemy.orm import Session  # type: ignore
from starlette.testclient import TestClient

from app.core.settings.settings import settings
from app.crud.clients import clients_crud
from app.models.clients import Clients as ClientModel
from app.models.operations import Operations as OperationModel
from app.schemas.v1.operation import Operation


def test_withdraw_operations(
    another_session_db: Session,
    test_client: TestClient,
    benefactor: ClientModel,
    withdraw_operation_dict: dict,
) -> None:
    response = test_client.post(
        f"{settings.API_VERSION}/operations/", json=withdraw_operation_dict
    )
    if response.status_code == 400:
        assert response.json().get("detail", None) == "non-sufficient funds"
    else:
        assert response.status_code == 201
        assert withdraw_operation_dict.get(
            "benefactor_client_id", None
        ) == response.json().get("benefactor_client_id", None)
        assert withdraw_operation_dict.get(
            "beneficiary_client_id", None
        ) == response.json().get("beneficiary_client_id", None)
        assert withdraw_operation_dict.get(
            "is_active", None
        ) == response.json().get("is_active", None)
        assert withdraw_operation_dict.get(
            "transfer_amount", 0.0
        ) == response.json().get("transfer_amount", 0.0)
        updated_benefactor = clients_crud.read(
            db=another_session_db,
            entity_id=withdraw_operation_dict.get(
                "benefactor_client_id", None
            ),
        )
        assert updated_benefactor is not None
        assert (
            updated_benefactor.wallet_balance
            == benefactor.wallet_balance
            - Decimal(
                str(withdraw_operation_dict.get("transfer_amount", 0.0))
            )
        )


def test_deposit_operations(
    another_session_db: Session,
    test_client: TestClient,
    beneficiary: ClientModel,
    deposit_operation_dict: dict,
) -> None:
    response = test_client.post(
        f"{settings.API_VERSION}/operations/", json=deposit_operation_dict
    )
    assert response.status_code == 201
    assert deposit_operation_dict.get(
        "benefactor_client_id", None
    ) == response.json().get("benefactor_client_id", None)
    assert deposit_operation_dict.get(
        "beneficiary_client_id", None
    ) == response.json().get("beneficiary_client_id", None)
    assert deposit_operation_dict.get(
        "is_active", None
    ) == response.json().get("is_active", None)
    assert deposit_operation_dict.get(
        "transfer_amount", 0.0
    ) == response.json().get("transfer_amount", 0.0)
    updated_beneficiary = clients_crud.read(
        db=another_session_db,
        entity_id=deposit_operation_dict.get("beneficiary_client_id", None),
    )
    assert updated_beneficiary is not None
    assert (
        updated_beneficiary.wallet_balance
        == beneficiary.wallet_balance
        + Decimal(str(deposit_operation_dict.get("transfer_amount", 0.0)))
    )


def test_send_operations(
    another_session_db: Session,
    test_client: TestClient,
    benefactor: ClientModel,
    beneficiary: ClientModel,
    send_operation_dict: dict,
) -> None:
    response = test_client.post(
        f"{settings.API_VERSION}/operations/", json=send_operation_dict
    )
    if response.status_code == 400:
        assert response.json().get("detail", None) == "non-sufficient funds"
    else:
        assert response.status_code == 201
        assert send_operation_dict.get(
            "benefactor_client_id", None
        ) == response.json().get("benefactor_client_id", None)
        assert send_operation_dict.get(
            "beneficiary_client_id", None
        ) == response.json().get("beneficiary_client_id", None)
        assert send_operation_dict.get(
            "is_active", None
        ) == response.json().get("is_active", None)
        assert send_operation_dict.get(
            "transfer_amount", 0.0
        ) == response.json().get("transfer_amount", 0.0)
        updated_benefactor = clients_crud.read(
            db=another_session_db,
            entity_id=send_operation_dict.get("benefactor_client_id", None),
        )
        assert updated_benefactor is not None
        assert (
            updated_benefactor.wallet_balance
            == benefactor.wallet_balance
            - Decimal(str(send_operation_dict.get("transfer_amount", 0.0)))
        )
        updated_beneficiary = clients_crud.read(
            db=another_session_db,
            entity_id=send_operation_dict.get("beneficiary_client_id", None),
        )
        assert updated_beneficiary is not None
        assert (
            updated_beneficiary.wallet_balance
            == beneficiary.wallet_balance
            + Decimal(str(send_operation_dict.get("transfer_amount", 0.0)))
        )


def test_read_operations(
    test_client: TestClient, send_operation: OperationModel
) -> None:
    response = test_client.get(url=f"{settings.API_VERSION}/operations/")
    assert response.status_code == 200
    for operation in response.json():
        Operation(**operation)


def test_read_client(
    test_client: TestClient, send_operation: OperationModel
) -> None:
    response = test_client.get(
        f"{settings.API_VERSION}/operations/{send_operation.id}"
    )
    assert response.status_code == 200
    assert send_operation.id == response.json().get("id", None)
    assert send_operation.benefactor_client_id == response.json().get(
        "benefactor_client_id", None
    )
    assert send_operation.beneficiary_client_id == response.json().get(
        "beneficiary_client_id", None
    )
    assert send_operation.is_active == response.json().get("is_active", None)
    assert send_operation.transfer_amount == Decimal(
        str(response.json().get("transfer_amount", 0.0))
    )


def test_delete_client(
    test_client: TestClient, send_operation: OperationModel
) -> None:
    response = test_client.delete(
        f"{settings.API_VERSION}/operations/{send_operation.id}"
    )
    assert response.status_code == 200
    assert send_operation.id == response.json().get("id", None)
    assert send_operation.benefactor_client_id == response.json().get(
        "benefactor_client_id", None
    )
    assert send_operation.beneficiary_client_id == response.json().get(
        "beneficiary_client_id", None
    )
    assert response.json().get("is_active", None) is False
    assert send_operation.transfer_amount == Decimal(
        str(response.json().get("transfer_amount", 0.0))
    )
