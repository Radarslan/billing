from copy import deepcopy
from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session  # type: ignore

from app.core.settings.settings import data_validation
from app.core.utils.get_entity import get_entity_instance
from app.crud.clients import clients_crud
from app.crud.operations import operations_crud
from app.models.clients import Clients
from app.models.operations import Operations
from app.schemas.v1.operation import OperationCreate


def bl_create_operation(
    db: Session, operation: OperationCreate
) -> Operations:
    benefactor = _get_client(db, operation.benefactor_client_id)
    beneficiary = _get_client(db, operation.beneficiary_client_id)

    if benefactor is not None and beneficiary is None:
        _withdraw_money_from_benefactor(db, benefactor, operation)

    if benefactor is None and beneficiary is not None:
        _deposit_money_for_beneficiary(db, beneficiary, operation)

    if benefactor is not None and beneficiary is not None:
        operation.beneficiary_client_id = None
        _withdraw_money_from_benefactor(db, benefactor, operation)
        operation.benefactor_client_id = None
        operation.beneficiary_client_id = beneficiary.id
        _deposit_money_for_beneficiary(db, beneficiary, operation)
        operation.benefactor_client_id = benefactor.id
    return _create_operation(db, operation)


def _get_client(db: Session, client_id: Optional[int]) -> Optional[Clients]:
    if client_id is not None:
        return get_entity_instance(db, clients_crud, client_id)
    return None


def _deposit_money_for_beneficiary(
    db: Session, beneficiary: Clients, operation: OperationCreate
) -> Clients:
    updated_beneficiary = deepcopy(beneficiary)
    updated_beneficiary.wallet_balance += operation.transfer_amount
    return clients_crud.update(
        db=db, db_obj=beneficiary, obj_in=updated_beneficiary  # type: ignore
    )


def _withdraw_money_from_benefactor(
    db: Session, benefactor: Clients, operation: OperationCreate
) -> Clients:
    updated_benefactor = deepcopy(benefactor)
    if (
        updated_benefactor.wallet_balance - operation.transfer_amount
        <= data_validation.wallet_minimum_amount
    ):
        raise HTTPException(status_code=400, detail="non-sufficient funds")
    updated_benefactor.wallet_balance -= operation.transfer_amount
    return clients_crud.update(
        db=db, db_obj=benefactor, obj_in=updated_benefactor  # type: ignore
    )


def _create_operation(db: Session, operation: OperationCreate):
    operation.is_active = True
    operation.operation_date = datetime.utcnow()
    return operations_crud.create(db=db, obj_in=operation)


def bl_delete_operation(db: Session, id: int) -> Operations:
    """
    sets operation to inactive
    """
    operation: Operations = get_entity_instance(db, operations_crud, id)
    obj_in = jsonable_encoder(operation)
    obj_in["is_active"] = False
    return operations_crud.update(db, db_obj=operation, obj_in=obj_in)
