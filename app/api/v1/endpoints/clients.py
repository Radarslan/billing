from typing import Any
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from sqlalchemy.orm import Session  # type: ignore

from app.api.deps import get_db
from app.core.business_logic_layer.clients import bl_create_client
from app.core.business_logic_layer.clients import bl_update_client
from app.core.utils.get_entity import get_entity_instance
from app.crud.clients import clients_crud
from app.schemas.v1.client import Client
from app.schemas.v1.client import ClientCreate
from app.schemas.v1.client import ClientQueryParams
from app.schemas.v1.client import ClientUpdate

router = APIRouter()


@router.post("/", response_model=Client, status_code=201, tags=["clients"])
async def create_client(
    *, db: Session = Depends(get_db), obj_in: ClientCreate
) -> Any:
    return bl_create_client(db=db, client=obj_in)


@router.get("/", response_model=List[Client], tags=["clients"])
async def find_clients(
    *,
    db: Session = Depends(get_db),
    query: ClientQueryParams = Depends(),
    skip: int = 0,
    limit: int = 10000,
) -> Any:

    clients = clients_crud.find_clients(db, query, skip, limit)
    if not clients:
        return []
    return clients


@router.get("/{id}", response_model=Client, tags=["client"])
async def read_client(
    *, id: int = Path(...), db: Session = Depends(get_db)
) -> Any:
    return get_entity_instance(db, clients_crud, id)


@router.put("/{id}", response_model=Client, tags=["client"])
async def update_client(
    *,
    id: int = Path(...),
    db: Session = Depends(get_db),
    obj_in: ClientUpdate,
) -> Any:
    return bl_update_client(db=db, client_id=id, update_client=obj_in)


@router.delete("/{id}", response_model=Client, tags=["client"])
async def delete_client(
    *, id: int = Path(...), db: Session = Depends(get_db)
) -> Any:
    get_entity_instance(db, clients_crud, id)
    return clients_crud.delete(db, entity_id=id)
