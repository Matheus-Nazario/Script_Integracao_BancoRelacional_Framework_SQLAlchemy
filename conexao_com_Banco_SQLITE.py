import sqlalchemy
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# Criar Conexão com Banco SQLITE
# Conectar com o banco de dados SQLITE e criar a
# tabela FUNCIONARIO (utilize o script abaixo para a criação da tabela)
engine = sqlalchemy.create_engine("sqlite:///servidor_exercicio_01.db")
connection = engine.connect()

# Criar sessão com o Banco de Dados
Base = declarative_base(engine)
session = Session()


# Criar tabela no banco de dados, caso não exista
connection.execute(
    """CREATE TABLE IF NOT EXISTS FUNCIONARIO(
                      ID INTEGER PRIMARY KEY,
                      NOME VARCHAR(255) NOT NULL,
                      IDADE INT NOT NULL,
                      SALARIO FLOAT NOT NULL)"""
)

# Criar uma classe Funcionario e mapear a tabela criada anteriormente.
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


# Instanciar três objetos da classe Funcionario.
lista_funcionario = []
for i in range(3):
    print(" - " * 30)
    nome = input("Nome: ")
    idade = int(input("Idade:"))
    salario = float(input("Salario:"))
    func = Funcionario(nome, idade, salario)
    lista_funcionario.append(func)
    print(" - " * 30)

# Inserir os dados dos objetos na tabela.
session.add_all(lista_funcionario)
session.commit()

# Realizar uma consulta na tabela de funcionários e
# verificar se os dados foram inseridos corretamente.

resultado = session.query(Funcionario)

print(" - " * 30)
print("\nTodos os Funcionários:")
for i in resultado:
    print(
        "ID: {} | Nome: {} | Idade: {} | salario: {}".format(
            i.id, i.nome, i.idade, i.salario
        )
    )
print(" - " * 30)

# Realizar uma consulta na tabela de todos os
# funcionários com salário superior a R$ 1.500,00

d = session.query(Funcionario).filter(Funcionario.salario > 1500)

print(" - " * 30)
print("\nFuncionários com salário superior a R$1500:")
for i in d:
    print(
        "ID: {} | Nome: {} | Idade: {} | salario: {}".format(
            i.id, i.nome, i.idade, i.salario
        )
    )
print(" - " * 30)

# fecha a conexão
connection.close()
