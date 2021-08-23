from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session  # type: ignore

from app.db.session import get_engine
from app.db.session import get_session
from app.main import app
from app.models.clients import Clients
from app.models.operations import Operations
from tests.utils.clients import create_random_client
from tests.utils.clients import create_random_client_dict
from tests.utils.operations import create_random_operation
from tests.utils.operations import create_random_operation_dict


@pytest.fixture()
def db() -> Generator:
    yield get_session(get_engine())


@pytest.fixture()
def another_session_db() -> Generator:
    yield get_session(get_engine())


@pytest.fixture()
def test_client() -> Generator:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def benefactor_dict() -> dict:
    return create_random_client_dict()


@pytest.fixture
def benefactor(db: Session, benefactor_dict: dict) -> Clients:
    return create_random_client(db, benefactor_dict)


@pytest.fixture
def beneficiary_dict() -> dict:
    return create_random_client_dict()


@pytest.fixture
def beneficiary(db: Session, beneficiary_dict: dict) -> Clients:
    return create_random_client(db, beneficiary_dict)


@pytest.fixture
def deposit_operation_dict(beneficiary: Clients) -> dict:
    return create_random_operation_dict(None, beneficiary)


@pytest.fixture
def deposit_operation(
    db: Session, deposit_operation_dict: dict
) -> Operations:
    return create_random_operation(db, deposit_operation_dict)


@pytest.fixture
def withdraw_operation_dict(benefactor: Clients) -> dict:
    return create_random_operation_dict(benefactor, None)


@pytest.fixture
def withdraw_operation(
    db: Session, withdraw_operation_dict: dict
) -> Operations:
    return create_random_operation(db, withdraw_operation_dict)


@pytest.fixture
def send_operation_dict(benefactor: Clients, beneficiary: Clients) -> dict:
    return create_random_operation_dict(benefactor, beneficiary)


@pytest.fixture
def send_operation(db: Session, send_operation_dict: dict) -> Operations:
    return create_random_operation(db, send_operation_dict)
