"""base service"""
import re
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from typing import List, Tuple, Union

import numpy as np
import src.schema.service.ml as svcschema
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process.kernels import ConstantKernel as C
from sqlalchemy.orm import Session
from src.configuration import const
from src.repository import mysql as repository


class Interface(metaclass=ABCMeta):
    """class for account interface"""

    def __call__(self):
        return self

    def validate_time_range(
        X: List[svcschema.InputData],
    ) -> Tuple[bool, Union[timedelta, None]]:
        """
        validate time range
        Args:
          X(List[schema.InputData]): input data
        Returns:
          bool: is valid or not
          timedelta: time range
        """
        # check time range
        if len(X) < 2:
            return False, None

        target_range = X[1].time - X[0].time

        for i in range(len(X)):
            if not isinstance(X[i].time, datetime):
                return False, None
            if i == 0 or i == 1:
                continue
            if X[i].time - X[i - 1].time != target_range:
                return False, None

        return True, target_range

    @abstractmethod
    def train_and_predict(
        self, db: Session, rep: repository.Interface, data: svcschema.InputData
    ) -> Tuple[List[svcschema.PredictedData], svcschema.PredictedData]:
        """
        train from input data and return predicted values
        Args:
          data(schema.InputData): input data
        Returns:
          List[schema.PredictedData]: predicted values
          schema.PredictedData: predicted next value
        """


class Service(Interface):
    """class for predict service"""

    def train_and_predict(
        self,
        rep: repository.Interface,
        data: List[svcschema.InputData],
    ) -> Tuple[List[svcschema.PredictedData], svcschema.PredictedData]:
        # define kernel and model
        kernel = C(1.0, (1e-3, 1e3)) * RBF(1.0, (1e-2, 1e2))
        gp = GaussianProcessRegressor(
            kernel=kernel, n_restarts_optimizer=10, optimizer=None
        )

        is_verified, time_range = self.validate_time_range(data) == False
        if not is_verified:
            raise ValueError("invalid time range")

        X = []
        y = []
        for i, d in enumerate(data):
            X.append(i + 1)
            y.append(d.value)
        X = np.array(X).reshape(-1, 1)  # [[1], [2], [3], ...]
        y = np.array(y)  # [1, 4, 9, ...]

        # train model
        gp.fit(X, y)

        # predict next data
        y_pred, std_dev = gp.predict(np.array([i + 2]).reshape(-1, 1), return_std=True)
        predicted_next_data = svcschema.PredictedData(
            value=y_pred[-1],
            time=data[-1].time + time_range,
            lower_bound=y_pred - 1.96 * std_dev,
            upper_bound=y_pred + 1.96 * std_dev,
        )

        # predict filling data
        x_pred = np.linspace(1, i + 2, 100, endpoint=False)[:, np.newaxis]
        y_pred, std_dev = gp.predict(x_pred, return_std=True)
        predicted_data = []
        for i, y_pred_i in enumerate(y_pred):
            predicted_data.append(
                svcschema.PredictedData(
                    value=y_pred_i,
                    time=data[-1].time + time_range * (x_pred[i][0] - 1),
                    lower_bound=y_pred_i - 1.96 * std_dev,
                    upper_bound=y_pred_i + 1.96 * std_dev,
                ),
            )

        return predicted_data, predicted_next_data
