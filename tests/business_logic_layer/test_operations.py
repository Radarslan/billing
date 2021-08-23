from copy import deepcopy
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app.core.business_logic_layer.operations import _create_operation
from app.core.business_logic_layer.operations import (
    _deposit_money_for_beneficiary,
)
from app.core.business_logic_layer.operations import _get_client
from app.core.business_logic_layer.operations import (
    _withdraw_money_from_benefactor,
)
from app.core.business_logic_layer.operations import bl_create_operation
from app.models.clients import Clients as ClientModel
from app.schemas.v1.operation import OperationCreate


def test_create_operation(db: Session, send_operation_dict: dict) -> None:
    operation = OperationCreate(**send_operation_dict)
    try:
        created_operation = bl_create_operation(db=db, operation=operation)
    except HTTPException as e:
        assert e.status_code == 400
        assert e.detail == "non-sufficient funds"
    else:
        assert (
            send_operation_dict.get("benefactor_client_id", None)
            == created_operation.benefactor_client_id
        )
        assert (
            send_operation_dict.get("beneficiary_client_id", None)
            == created_operation.beneficiary_client_id
        )
        assert (
            send_operation_dict.get("is_active", None)
            == created_operation.is_active
        )
        assert (
            Decimal(str(send_operation_dict.get("transfer_amount", 0.0)))
            == created_operation.transfer_amount
        )


def test__create_operation(db: Session, send_operation_dict: dict) -> None:
    operation = OperationCreate(**send_operation_dict)
    created_operation = _create_operation(db=db, operation=operation)
    assert (
        send_operation_dict.get("benefactor_client_id", None)
        == created_operation.benefactor_client_id
    )
    assert (
        send_operation_dict.get("beneficiary_client_id", None)
        == created_operation.beneficiary_client_id
    )
    assert (
        send_operation_dict.get("is_active", None)
        == created_operation.is_active
    )
    assert (
        Decimal(str(send_operation_dict.get("transfer_amount", 0.0)))
        == created_operation.transfer_amount
    )


def test__deposit_money_for_beneficiary(
    db: Session, beneficiary: ClientModel, deposit_operation_dict: dict
) -> None:
    beneficiary_wallet_balance = deepcopy(beneficiary.wallet_balance)
    operation = OperationCreate(**deposit_operation_dict)
    updated_beneficiary = _deposit_money_for_beneficiary(
        db=db, beneficiary=beneficiary, operation=operation
    )
    assert beneficiary.first_name == updated_beneficiary.first_name
    assert beneficiary.last_name == updated_beneficiary.last_name
    assert beneficiary.phone_number == updated_beneficiary.phone_number
    assert (
        updated_beneficiary.wallet_balance
        == beneficiary_wallet_balance
        + Decimal(str(deposit_operation_dict.get("transfer_amount", 0.0)))
    )


def test__get_client(db: Session, beneficiary: ClientModel) -> None:
    got_client = _get_client(db=db, client_id=beneficiary.id)
    assert got_client is not None
    assert beneficiary.first_name == got_client.first_name
    assert beneficiary.last_name == got_client.last_name
    assert beneficiary.phone_number == got_client.phone_number
    assert got_client.wallet_balance == beneficiary.wallet_balance


def test__withdraw_money_for_beneficiary(
    db: Session, benefactor: ClientModel, withdraw_operation_dict: dict
) -> None:
    benefactor_wallet_balance = deepcopy(benefactor.wallet_balance)
    operation = OperationCreate(**withdraw_operation_dict)
    try:
        updated_benefactor = _withdraw_money_from_benefactor(
            db=db, benefactor=benefactor, operation=operation
        )
    except HTTPException as e:
        assert e.status_code == 400
        assert e.detail == "non-sufficient funds"
    else:
        assert benefactor.first_name == updated_benefactor.first_name
        assert benefactor.last_name == updated_benefactor.last_name
        assert benefactor.phone_number == updated_benefactor.phone_number
        assert (
            updated_benefactor.wallet_balance
            == benefactor_wallet_balance
            - Decimal(
                str(withdraw_operation_dict.get("transfer_amount", 0.0))
            )
        )
