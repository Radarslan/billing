from datetime import datetime

from sqlalchemy import TIMESTAMP  # type: ignore
from sqlalchemy import BigInteger  # type: ignore
from sqlalchemy import Boolean  # type: ignore
from sqlalchemy import CheckConstraint  # type: ignore
from sqlalchemy import Column  # type: ignore
from sqlalchemy import Float  # type: ignore
from sqlalchemy import ForeignKey  # type: ignore
from sqlalchemy import ForeignKeyConstraint  # type: ignore
from sqlalchemy import Index  # type: ignore
from sqlalchemy import Numeric  # type: ignore
from sqlalchemy import String  # type: ignore
from sqlalchemy import func  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.core.settings.settings import data_validation
from app.db.base_class import Base


class Operations(Base):
    # columns
    id = Column(
        BigInteger,
        autoincrement=True,
        nullable=False,
        primary_key=True,
        unique=True,
    )

    # benefactor could be nullable for deposit operations
    benefactor_client_id = Column(
        BigInteger, ForeignKey("clients.id"), nullable=True
    )

    # beneficiary could be nullable for withdrawal operations
    beneficiary_client_id = Column(
        BigInteger, ForeignKey("clients.id"), nullable=True
    )

    transfer_amount = Column(
        Numeric(
            data_validation.transfer_maximum_number_of_digits,
            data_validation.transfer_maximum_number_of_decimal_places,
        ),
        nullable=False,
    )
    operation_date = Column(
        TIMESTAMP, nullable=False, default=datetime.utcnow()
    )
    is_active = Column(Boolean, nullable=False, default=True)

    # relationships
    benefactor = relationship(
        "Clients",
        back_populates="send_operations",
        foreign_keys=benefactor_client_id,
    )
    beneficiary = relationship(
        "Clients",
        back_populates="receive_operations",
        foreign_keys=benefactor_client_id,
    )

    # constraints
    CheckConstraint(
        f"transfer_amount >= {data_validation.transfer_minimum_amount}"
        f"and transfer_amount <= {data_validation.transfer_maximum_amount}"
    )


# indexes
"""
We assume operation creation will be occurring pretty frequently.
Therefore, all indexes for any column bot added by default (that is
done to speed up write). If fast read is required read-only standby
replica server creation will be way to go, where all the following
indexes will be present.
"""
# Index(
#     f"{Operations.__tablename__}_benefactor_client_id",
#     Operations.benefactor_client_id,
#     postgresql_using="hash",
# )
# Index(
#     f"{Operations.__tablename__}_beneficiary_client_id",
#     Operations.beneficiary_client_id,
#     postgresql_using="hash",
# )
# Index(
#     f"{Operations.__tablename__}_benefactor_client_id_beneficiary_client_id",
#     Operations.benefactor_client_id,
#     Operations.beneficiary_client_id,
#     postgresql_using="btree",
# )
# Index(
#     f"{Operations.__tablename__}_transfer_amount",
#     Operations.transfer_amount,
#     postgresql_using="btree",
# )
# Index(
#     f"{Operations.__tablename__}_operation_date",
#     Operations.operation_date,
#     postgresql_using="btree",
# )
