from typing import Any
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session  # type: ignore

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


def exclude_unset(obj_data: dict):
    return {
        key: value for key, value in obj_data.items() if value is not None
    }


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def create(
        self, db: Session, *, obj_in: Union[CreateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore

        # prevent id collisions
        entity = (
            db.query(self.model)
            .filter(self.model.id == obj_in_data.get("id", 0))  # type: ignore
            .first()
        )
        if entity:
            db.merge(db_obj)
            db.commit()
            return db_obj

        # normal behavior
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def read_many(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        db_objs = db.query(self.model).offset(skip).limit(limit).all()
        return db_objs

    def read(self, db: Session, entity_id: Any) -> Optional[ModelType]:
        return db.query(self.model).get(entity_id)

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = exclude_unset(obj_in)
        else:
            update_data = jsonable_encoder(obj_in, exclude_unset=True)

        # prevent id collisions
        entity_id = update_data.get("id", "")
        if entity_id and entity_id != db_obj.id:
            update_data["id"] = db_obj.id

        # normal behavior
        for field in db_obj.__dict__:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, entity_id: Any) -> Optional[ModelType]:
        db_obj = db.query(self.model).get(entity_id)
        db.delete(db_obj)
        db.commit()
        return db_obj
