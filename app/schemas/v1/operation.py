from datetime import datetime
from typing import Any
from typing import Dict
from typing import Optional
from typing import Type

from pydantic import BaseModel
from pydantic import condecimal
from pydantic import validator

from app.core.settings.settings import data_validation


class OperationBase(BaseModel):
    benefactor_client_id: Optional[int]
    beneficiary_client_id: Optional[int]
    transfer_amount: Optional[  # type: ignore
        condecimal(
            ge=data_validation.transfer_minimum_amount,
            le=data_validation.transfer_maximum_amount,
            max_digits=data_validation.transfer_maximum_number_of_digits,
            decimal_places=data_validation.transfer_maximum_number_of_decimal_places,
        )
    ]
    operation_date: Optional[datetime]
    is_active: Optional[bool]


# Properties to receive via API on creation
class OperationCreate(OperationBase):
    benefactor_client_id: Optional[int] = None
    beneficiary_client_id: Optional[int] = None
    transfer_amount: condecimal(  # type: ignore
        ge=data_validation.transfer_minimum_amount,
        le=data_validation.transfer_maximum_amount,
        max_digits=data_validation.transfer_maximum_number_of_digits,
        decimal_places=data_validation.transfer_maximum_number_of_decimal_places,
    )
    operation_date: datetime = datetime.utcnow()
    is_active: bool = True

    class Config:
        @staticmethod
        def schema_extra(
            schema: Dict[str, Any], model: Type["OperationCreate"]
        ) -> None:
            schema["properties"].pop("operation_date", None)
            schema["properties"].pop("is_active", None)


# Properties to receive via API on update
class OperationUpdate(OperationBase):
    benefactor_client_id: Optional[int]
    beneficiary_client_id: Optional[int]
    transfer_amount: Optional[  # type: ignore
        condecimal(
            ge=data_validation.transfer_minimum_amount,
            le=data_validation.transfer_maximum_amount,
            max_digits=data_validation.transfer_maximum_number_of_digits,
            decimal_places=data_validation.transfer_maximum_number_of_decimal_places,
        )
    ]
    operation_date: Optional[datetime]
    is_active: Optional[bool]


class OperationInDBBase(OperationBase):
    id: int
    benefactor_client_id: Optional[int] = None
    beneficiary_client_id: Optional[int] = None
    transfer_amount: condecimal(  # type: ignore
        ge=data_validation.transfer_minimum_amount,
        le=data_validation.transfer_maximum_amount,
        max_digits=data_validation.transfer_maximum_number_of_digits,
        decimal_places=data_validation.transfer_maximum_number_of_decimal_places,
    )
    operation_date: datetime
    is_active: bool

    class Config:
        orm_mode = True

    @validator("operation_date")
    def result_check(cls, value):
        value = value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return value


# Additional properties to return via API
class Operation(OperationInDBBase):
    pass
