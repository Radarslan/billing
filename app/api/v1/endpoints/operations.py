from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from sqlalchemy.orm import Session  # type: ignore

from app.api.deps import get_db
from app.core.business_logic_layer.operations import bl_create_operation
from app.core.business_logic_layer.operations import bl_delete_operation
from app.core.utils.get_entity import get_entity_instance
from app.crud.operations import operations_crud
from app.schemas.v1.operation import Operation
from app.schemas.v1.operation import OperationCreate

router = APIRouter()


@router.post(
    "/", response_model=Operation, status_code=201, tags=["operations"]
)
async def create_operation(
    *, db: Session = Depends(get_db), obj_in: OperationCreate
) -> Any:
    return bl_create_operation(db=db, operation=obj_in)


@router.get("/", response_model=List[Operation], tags=["operations"])
async def read_operations(
    *, db: Session = Depends(get_db), skip: int = 0, limit: int = 10000
) -> Any:
    """
    find operation was omitted to emphasize write operations
    """

    operations = operations_crud.read_many(db, skip=skip, limit=limit)
    if not operations:
        return []
    return operations


@router.get("/{id}", response_model=Operation, tags=["operation"])
async def read_operation(
    *, id: int = Path(...), db: Session = Depends(get_db)
) -> Any:
    return get_entity_instance(db, operations_crud, id)


@router.delete("/{id}", response_model=Operation, tags=["operation"])
async def delete_operation(
    *, id: int = Path(...), db: Session = Depends(get_db)
) -> Any:
    return bl_delete_operation(db, id)
