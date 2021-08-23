from decimal import Decimal

from sqlalchemy.orm import Session  # type: ignore

from app.crud.operations import operations_crud
from app.models.operations import Operations as OperationModel


def test_create_operations(db: Session, send_operation_dict: dict) -> None:
    client = operations_crud.create(db=db, obj_in=send_operation_dict)
    assert (
        send_operation_dict.get("benefactor_client_id", None)
        == client.benefactor_client_id
    )
    assert (
        send_operation_dict.get("beneficiary_client_id", None)
        == client.beneficiary_client_id
    )
    assert send_operation_dict.get("is_active", None) == client.is_active
    assert (
        Decimal(str(send_operation_dict.get("transfer_amount", 0.0)))
        == client.transfer_amount
    )


def test_read_operations(db: Session, send_operation: OperationModel) -> None:
    operations = operations_crud.read_many(db=db)
    for client in operations:
        assert isinstance(client, OperationModel)


def test_read_operation(db: Session, send_operation: OperationModel) -> None:
    operations = operations_crud.read(db=db, entity_id=send_operation.id)
    assert operations is not None
    assert send_operation.id == operations.id
    assert (
        send_operation.benefactor_client_id == operations.benefactor_client_id
    )
    assert (
        send_operation.beneficiary_client_id
        == operations.beneficiary_client_id
    )
    assert send_operation.is_active == operations.is_active
    assert send_operation.transfer_amount == operations.transfer_amount


def test_update_operation(
    db: Session, send_operation: OperationModel, send_operation_dict: dict
) -> None:
    operation = operations_crud.update(
        db=db, db_obj=send_operation, obj_in=send_operation_dict
    )
    assert send_operation.id == operation.id
    assert (
        send_operation_dict.get("benefactor_client_id", None)
        == operation.benefactor_client_id
    )
    assert (
        send_operation_dict.get("beneficiary_client_id", None)
        == operation.beneficiary_client_id
    )
    assert send_operation_dict.get("is_active", None) == operation.is_active
    assert (
        Decimal(str(send_operation_dict.get("transfer_amount", 0.0)))
        == operation.transfer_amount
    )


def test_delete_operation(
    db: Session, send_operation: OperationModel
) -> None:
    operations = operations_crud.delete(db=db, entity_id=send_operation.id)
    assert operations is not None
    assert send_operation.id == operations.id
    assert (
        send_operation.benefactor_client_id == operations.benefactor_client_id
    )
    assert (
        send_operation.beneficiary_client_id
        == operations.beneficiary_client_id
    )
    assert send_operation.is_active == operations.is_active
    assert send_operation.transfer_amount == operations.transfer_amount
