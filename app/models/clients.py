from decimal import Decimal

from sqlalchemy import CHAR  # type: ignore
from sqlalchemy import VARCHAR  # type: ignore
from sqlalchemy import BigInteger  # type: ignore
from sqlalchemy import CheckConstraint  # type: ignore
from sqlalchemy import Column  # type: ignore
from sqlalchemy import Float  # type: ignore
from sqlalchemy import ForeignKey  # type: ignore
from sqlalchemy import Index  # type: ignore
from sqlalchemy import Numeric  # type: ignore
from sqlalchemy import String  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.core.settings.settings import data_validation
from app.db.base_class import Base


class Clients(Base):
    # columns
    id = Column(
        BigInteger,
        autoincrement=True,
        nullable=False,
        primary_key=True,
        unique=True,
    )
    first_name = Column(
        VARCHAR(data_validation.first_name_maximum_length), nullable=False
    )
    last_name = Column(
        VARCHAR(data_validation.last_name_maximum_length), nullable=False
    )
    phone_number = Column(
        CHAR(data_validation.phone_number_maximum_length),
        nullable=False,
        unique=True,
    )
    wallet_balance = Column(
        Numeric(
            data_validation.wallet_maximum_number_of_digits,
            data_validation.wallet_maximum_number_of_decimal_places,
        ),
        nullable=False,
        default=Decimal("0.0"),
    )

    # relationships
    send_operations = relationship(
        "Operations",
        foreign_keys="[Operations.benefactor_client_id]",
        back_populates="benefactor",
        cascade="all, delete-orphan",
    )
    receive_operations = relationship(
        "Operations",
        foreign_keys="[Operations.beneficiary_client_id]",
        back_populates="beneficiary",
        cascade="all, delete-orphan",
    )

    # constraints
    CheckConstraint(
        f"length(first_name) >= {data_validation.names_minimum_length}"
    )
    CheckConstraint(
        f"length(last_name) >= {data_validation.names_minimum_length}"
    )
    CheckConstraint(
        f"length(phone_number) = {data_validation.phone_number_maximum_length}"
    )
    CheckConstraint(
        f"wallet_balance >= {data_validation.wallet_minimum_amount}"
        f"and wallet_balance <= {data_validation.wallet_maximum_amount}"
    )


# indexes
"""
We assume client creation will be occurring to the significantly less
margin than transactions. Therefore, indexes for names are added and
there is no index for wallet amount (that is done to speed up write). 
"""
Index(
    f"{Clients.__tablename__}_first_name",
    Clients.first_name,
    postgresql_using="btree",
)
Index(
    f"{Clients.__tablename__}_last_name",
    Clients.last_name,
    postgresql_using="btree",
)
Index(
    f"{Clients.__tablename__}_first_name_last_name",
    Clients.first_name,
    Clients.last_name,
    postgresql_using="btree",
)
