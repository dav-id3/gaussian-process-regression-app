"""Dependency injencton"""
from src.configuration.env import new_env
from src.model import BaseMySQL
from src.repository import mysql
from src.service import ml

env = new_env()

mysqlrep: mysql.Interface = mysql.Repository(env)

BaseMySQL.prepare(mysqlrep.engine)

mlsvc: ml.Interface = ml.Service()
