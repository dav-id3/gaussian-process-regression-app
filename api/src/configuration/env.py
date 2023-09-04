"""environment variables"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class ENV:
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_DATABASE: str
    MYSQL_USER: Optional[str]
    MYSQL_PASSWORD: Optional[str]
    ALLOW_ORIGINS: str


def new_env() -> ENV:
    """
    dependemcy injection for env

    Returns:
        ENV
    """
    return ENV(
        MYSQL_HOST=os.environ.get("MYSQL_HOST"),
        MYSQL_PORT=os.environ.get("MYSQL_PORT"),
        MYSQL_DATABASE=os.environ.get("MYSQL_DATABASE"),
        MYSQL_USER=os.environ.get("MYSQL_USER"),
        MYSQL_PASSWORD=os.environ.get("MYSQL_PASSWORD"),
        ALLOW_ORIGINS=os.environ.get("ALLOW_ORIGINS", "*"),
    )
