"""mysql repository"""
import textwrap
from abc import ABCMeta, abstractmethod
from typing import AsyncGenerator, Dict, List

import sqlalchemy
import src.model as model
import src.schema.repository.mysql as mysqlschema
import src.schema.service.ml as mlschema
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import text
from src.configuration.env import ENV


class Interface(metaclass=ABCMeta):
    """class for mysql interface"""

    def __call__(self):
        return self

    def __init__(self, env: ENV):
        self.env = env
        self.engine = create_engine(self.__build_database_url(), pool_pre_ping=True)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    async def get_session(self) -> AsyncGenerator:
        """dependent db session creation"""
        session = self.session()

        try:
            yield session
        finally:
            session.close()

    def __build_database_url(self) -> str:
        """
        build Python MySQL driver specific database url string

        Returns:
            str: database uri string
        Examples:
            >>> build_url()
            "mysql+mysqldb://username:password@hostname:port?charset=utf8"
        """
        hostname = self.env.MYSQL_HOST
        username = self.env.MYSQL_USER
        password = self.env.MYSQL_PASSWORD
        database = self.env.MYSQL_DATABASE
        port = self.env.MYSQL_PORT

        # use pymysql driver instead
        protocol = "mysql+pymysql"
        identity = f"{username}:{password}"
        host = f"{hostname}:{port}"

        pathname = f"/{database}"
        qs = "?charset=utf8"

        origin = f"{protocol}://{identity}@{host}"

        return origin + pathname + qs

    @abstractmethod
    def update_predicted_data(
        self, session: Session, req: mlschema.PredictedData
    ) -> None:
        """
        Update predicted data
        Args:
            req (mysqlschema.record): record
        Returns:
            None
        """


class Repository(Interface):
    """class for mysql repository"""

    def update_predicted_data(
        self, session: Session, req: mlschema.PredictedData
    ) -> None:
        sql = textwrap.dedent(
            f"""
            INSERT INTO
                {model.PredictedData.__tablename__}
                (
                    `value`,
                    `time`,
                    `lower_bound`,
                    `upper_bound`
                )
            VALUES
                (
                    :value,
                    :time,
                    :lower_bound,
                    :upper_bound
                )
            ON DUPLICATE KEY UPDATE
                `value` = :value,
                `time` = :time,
                `lower_bound` = :lower_bound,
                `upper_bound` = :upper_bound
            """
        )
        prepared_statement: List[Dict[str, any]] = []
        for r in req:
            state_dict = {}
            state_dict["value"] = r.value
            state_dict["time"] = r.time
            state_dict["lower_bound"] = r.lower_bound
            state_dict["upper_bound"] = r.upper_bound
            prepared_statement.append(state_dict)
        try:
            session.execute(text(sql), prepared_statement)
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            session.rollback()
            raise mysqlschema.InsertionDBError(
                "mysql.update_predicted_next_value: insertion error"
            )
