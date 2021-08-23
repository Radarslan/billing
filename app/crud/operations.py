from sqlalchemy.orm import Session  # type: ignore

from app.crud.base import CRUDBase
from app.models.operations import Operations
from app.schemas.v1.operation import OperationCreate
from app.schemas.v1.operation import OperationUpdate


class CRUDOperations(CRUDBase[Operations, OperationCreate, OperationUpdate]):
    pass


operations_crud = CRUDOperations(Operations)
