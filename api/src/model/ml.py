from .base import Base, BaseMySQL


class PredictedData(BaseMySQL, Base):
    """predicted value entity"""

    __tablename__ = "predicted_data"
