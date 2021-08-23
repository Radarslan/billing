from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.engine import Engine  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

from app.core.settings.settings import settings


def get_engine(isolation_level: str = "READ COMMITTED") -> Engine:
    """

    :param isolation_level: set to READ COMMITTED because we expect
        many write requests and need to have opportunity to update
        data without blocking operation. Data read consistency
        consider REPEATABLE READ and SERIALIZABLE isolation levels.
        To use them, different PostgreSQL deployments should be
        created. Like masters and standby read-only replicas of
        multi-master ones.
        In that case 2 changes required:
        1. PostgreSQL deployment should be changed.
        2. Code must be updated to handle concurrent update and
        transaction block errors, and ignored operations.
        We do not allow to perform withdrawal or minus operations on
        users' wallets to anyone except users themselves. Thereby
        collisions on such operation are impossible, hence only 1
        operation will done at a time - by user himself when he sends
        money or withdraws it.

    :return: SQL Alchemy Engine
    """
    return create_engine(
        url=settings.SQLALCHEMY_DATABASE_URI,
        execution_options={"isolation_level": isolation_level},
        pool_pre_ping=True,
    )


def get_session(engine: Engine) -> Session:
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()
