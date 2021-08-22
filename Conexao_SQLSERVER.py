# Conexao_SQLSERVER
# necessário instalar o pyodbc, executando no terminal o comando: pip install pyodbc


import pyodbc  # importar o pyodbc
import sqlalchemy  # importar sqlalchemy
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# Inserir abaixo as informações de acesso ao servidor SQLSERVER
con_server = "SERVERNAME"
con_database = "DATABASENAME"
con_username = "USERNAME"
con_password = "USERPASSWORD"

# Criar conexão com o banco SQLSERVER
engine = sqlalchemy.create_engine(
    "mssql+pyodbc://{con_username}:{con_password}@{con_server}:1433/{con_database}?driver=ODBC+Driver+17+for+SQL+Server"
)
connection = engine.connect()
