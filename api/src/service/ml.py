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
        input_data: List[svcschema.InputData],
    ) -> Tuple[List[svcschema.PredictedData], svcschema.PredictedData]:
        # define kernel and model
        kernel = C(1.0, (1e-3, 1e3)) * RBF(1.0, (1e-2, 1e2))
        gp = GaussianProcessRegressor(
            kernel=kernel, n_restarts_optimizer=10, optimizer=None
        )

        X = []
        y = []
        for input_datum in enumerate(input_data):
            X.append(input_datum.x_value)
            y.append(input_datum.y_value)
        X.sort()
        X = np.array(X).reshape(-1, 1)  # [[1], [2], [3], ...]
        y = np.array(y)  # [1, 4, 9, ...]

        # train model
        gp.fit(X, y)

        # predict next data
        y_pred, std_dev = gp.predict(
            np.array([X[-1][0] + 1]).reshape(-1, 1), return_std=True
        )
        predicted_next_data = svcschema.PredictedData(
            y_value=y_pred[-1],
            x_value=X[-1][0] + 1,
            lower_bound=y_pred - 1.96 * std_dev,
            upper_bound=y_pred + 1.96 * std_dev,
        )

        # predict filling data
        x_pred = np.linspace(X[0][0], X[-1][0] + 1, 100, endpoint=False)[:, np.newaxis]
        y_pred, std_dev = gp.predict(x_pred, return_std=True)
        predicted_data = []
        for i, y_pred_i in enumerate(y_pred):
            predicted_data.append(
                svcschema.PredictedData(
                    y_value=y_pred_i,
                    x_value=x_pred[i][0],
                    lower_bound=y_pred_i - 1.96 * std_dev,
                    upper_bound=y_pred_i + 1.96 * std_dev,
                ),
            )

        return predicted_data, predicted_next_data
