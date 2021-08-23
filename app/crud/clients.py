from typing import List

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.expression import and_  # type: ignore

from app.crud.base import CRUDBase
from app.models.clients import Clients
from app.schemas.v1.client import ClientCreate
from app.schemas.v1.client import ClientQueryParams
from app.schemas.v1.client import ClientUpdate


class CRUDClients(CRUDBase[Clients, ClientCreate, ClientUpdate]):
    def find_clients(
        self,
        db: Session,
        query: ClientQueryParams,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Clients]:
        filters = [
            getattr(Clients, parameter).like(f"%{getattr(query, parameter)}%")
            for parameter in query.__slots__
            if isinstance(getattr(query, parameter), str)
        ]
        return (
            db.query(self.model)
            .filter(and_(*filters))
            .order_by(
                self.model.first_name,
                self.model.last_name,
                self.model.phone_number,
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


clients_crud = CRUDClients(Clients)
