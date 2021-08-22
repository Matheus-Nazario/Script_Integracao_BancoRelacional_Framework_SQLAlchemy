import sqlalchemy
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# Criar Conexão com Banco SQLITE
# caso o arquivo de banco não exista, ele será criado
engine = sqlalchemy.create_engine("sqlite:///server.db")
connection = engine.connect()

# Criar sessão com o Banco de Dados
Base = declarative_base(engine)
session = Session()

connection.execute(
    """CREATE TABLE IF NOT EXISTS FUNCIONARIO (
                        ID INTEGER PRIMARY KEY,
                        NOME VARCHAR(255) NOT NULL,
                        IDADE INT NOT NULL,
                        SALARIO FLOAT NOT NULL)
                    """
)


class Funcionario(Base):
    __tablename__ = "FUNCIONARIO"
    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    nome = Column("NOME", String(255), nullable=False)
    idade = Column("IDADE", Integer, nullable=False)
    salario = Column("SALARIO", Float, nullable=False)

    def __init__(self, nome, idade, salario):
        self.nome = nome
        self.idade = idade
        self.salario = salario


# Abre o arquivo de texto
arquivo = open("listade_funcionarios.txt", "r", encoding="UTF-8")

list_atl_func = []

for linha in arquivo:
    lista = linha.split(";")
    func = Funcionario(lista[0], int(lista[1]), float(lista[2]))
    list_atl_func.append(func)

session.add_all(list_atl_func)
session.commit()

resultado = session.query(Funcionario).all()

for i in resultado:
    print(
        "ID: {} | Nome: {} | Idade: {} | Salario: {}".format(
            i.id, i.nome, i.idade, i.salario
        )
    )


arquivo.close()
connection.close()
