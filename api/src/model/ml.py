from .base import BaseMySQL, Base


class PredictedNextValue(BaseMySQL, Base):
    """predicted value entity"""

    __tablename__ = "predicted_next_value"
