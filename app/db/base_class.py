from string import ascii_lowercase
from string import ascii_uppercase
from typing import Any

from sqlalchemy.ext.declarative import as_declarative  # type: ignore
from sqlalchemy.ext.declarative import declared_attr  # type: ignore


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Use full words as class names.
        DO NOT use abbreviations or shortened words like VM, ABS,
        MVP etc. Use VirtualMachine, Abstract, MinimumViableProduct
        instead. The code below will convert them into snake case
        table names.
        """

        table_name = ""
        i = 0
        name_length = len(cls.__name__)
        while i in range(name_length):
            if cls.__name__[i] in ascii_uppercase:
                table_name += cls.__name__[i].lower()
            elif cls.__name__[i] in ascii_lowercase:
                table_name += cls.__name__[i]

            if i < name_length - 1 and cls.__name__[i + 1] in ascii_uppercase:
                table_name += "_" + cls.__name__[i + 1].lower()
                i += 2
            else:
                i += 1

        return table_name
