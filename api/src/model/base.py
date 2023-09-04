from typing import Any, Dict, Optional, Set

from sqlalchemy.ext.declarative import DeferredReflection, as_declarative, declarative_base


Base = declarative_base()


class BaseMySQL(DeferredReflection):
    """Entity with its identifier"""

    # def to_dict(self, exclude: Optional[Set[str]] = None) -> Dict[str, any]:
    #     """Returns attributes mapped from the columns of DB model"""
    #     if exclude is None:
    #         exclude = set()
    #     return {k: v for k, v in self.__dict__.items() if not k.startswith("_") and k not in exclude}
