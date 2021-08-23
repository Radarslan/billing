from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app.crud.base import CRUDBase
from app.crud.base import ModelType


def get_entity_instance(
    db: Session, crud: CRUDBase, entity_id: Any
) -> ModelType:
    entity_instance = crud.read(db, entity_id)
    if not entity_instance:
        error = f"Object with id {entity_id} does not exist"
        raise HTTPException(status_code=404, detail=error)
    return entity_instance
