from decimal import Decimal
from typing import Any
from typing import Dict
from typing import Optional
from typing import Type

from fastapi import Query
from pydantic import BaseModel
from pydantic import condecimal
from pydantic import constr

from app.core.settings.settings import data_validation


class ClientQueryParams:
    __slots__ = ["first_name", "last_name", "phone_number"]

    def __init__(
        self,
        first_name: Optional[str] = Query(
            None,
            alias="first name",
            min_length=data_validation.names_minimum_length,
            max_length=data_validation.first_name_maximum_length,
        ),
        last_name: Optional[str] = Query(
            None,
            alias="last name",
            min_length=data_validation.names_minimum_length,
            max_length=data_validation.last_name_maximum_length,
        ),
        phone_number: Optional[str] = Query(
            None,
            alias="phone number",
            min_length=data_validation.find_phone_number_minimum_length,
            max_length=data_validation.phone_number_maximum_length,
            example="9991112222",
        ),
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number


class ClientBase(BaseModel):
    first_name: Optional[  # type: ignore
        constr(
            min_length=data_validation.names_minimum_length,
            max_length=data_validation.first_name_maximum_length,
        )
    ]
    last_name: Optional[  # type: ignore
        constr(
            min_length=data_validation.names_minimum_length,
            max_length=data_validation.last_name_maximum_length,
        )
    ]
    phone_number: Optional[  # type: ignore
        constr(
            min_length=data_validation.phone_number_minimum_length,
            max_length=data_validation.phone_number_maximum_length,
        )
    ]
    wallet_balance: Optional[  # type: ignore
        condecimal(
            ge=data_validation.wallet_minimum_amount,
            le=data_validation.wallet_maximum_amount,
            max_digits=data_validation.wallet_maximum_number_of_digits,
            decimal_places=data_validation.wallet_maximum_number_of_decimal_places,
        )
    ] = Decimal("0.0")


# Properties to receive via API on creation
class ClientCreate(ClientBase):
    first_name: constr(  # type: ignore
        min_length=data_validation.names_minimum_length,
        max_length=data_validation.first_name_maximum_length,
    )
    last_name: constr(  # type: ignore
        min_length=data_validation.names_minimum_length,
        max_length=data_validation.last_name_maximum_length,
    )
    phone_number: constr(  # type: ignore
        min_length=data_validation.phone_number_minimum_length,
        max_length=data_validation.phone_number_maximum_length,
        regex=r"[0-9]{10}",
    )
    wallet_balance: condecimal(  # type: ignore
        ge=data_validation.wallet_minimum_amount,
        le=data_validation.wallet_maximum_amount,
        max_digits=data_validation.wallet_maximum_number_of_digits,
        decimal_places=data_validation.wallet_maximum_number_of_decimal_places,
    ) = Decimal("0.0")


# Properties to receive via API on update
class ClientUpdate(ClientBase):
    first_name: Optional[  # type: ignore
        constr(
            min_length=data_validation.names_minimum_length,
            max_length=data_validation.first_name_maximum_length,
        )
    ]
    last_name: Optional[  # type: ignore
        constr(
            min_length=data_validation.names_minimum_length,
            max_length=data_validation.last_name_maximum_length,
        )
    ]
    phone_number: Optional[  # type: ignore
        constr(
            min_length=data_validation.phone_number_minimum_length,
            max_length=data_validation.phone_number_maximum_length,
        )
    ]
    wallet_balance: Optional[  # type: ignore
        condecimal(
            ge=data_validation.wallet_minimum_amount,
            le=data_validation.wallet_maximum_amount,
            max_digits=data_validation.transfer_maximum_number_of_digits,
            decimal_places=data_validation.transfer_maximum_number_of_decimal_places,
        )
    ]

    class Config:
        @staticmethod
        def schema_extra(
            schema: Dict[str, Any], model: Type["ClientUpdate"]
        ) -> None:
            schema["properties"].pop("wallet_balance", None)


class ClientInDBBase(ClientBase):
    id: int
    first_name: constr(  # type: ignore
        min_length=data_validation.names_minimum_length,
        max_length=data_validation.first_name_maximum_length,
    )
    last_name: constr(  # type: ignore
        min_length=data_validation.names_minimum_length,
        max_length=data_validation.last_name_maximum_length,
    )
    phone_number: constr(  # type: ignore
        min_length=data_validation.phone_number_minimum_length,
        max_length=data_validation.phone_number_maximum_length,
    )
    wallet_balance: condecimal(  # type: ignore
        ge=data_validation.wallet_minimum_amount,
        le=data_validation.wallet_maximum_amount,
        max_digits=data_validation.wallet_maximum_number_of_digits,
        decimal_places=data_validation.wallet_maximum_number_of_decimal_places,
    )

    class Config:
        orm_mode = True


# Additional properties to return via API
class Client(ClientInDBBase):
    pass
