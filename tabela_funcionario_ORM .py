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


# Criar tabela no banco de dados, caso não exista
connection.execute(
    """CREATE TABLE IF NOT EXISTS FUNCIONARIO (
                        ID INTEGER PRIMARY KEY,
                        NOME VARCHAR(255) NOT NULL,
                        IDADE INT NOT NULL,
                        SALARIO FLOAT NOT NULL)
                    """
)


# Mapeamento da tabela
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


# Inserir dados (um objeto)
func = Funcionario("Zezinho", 20, 1700)
session.add(func)  # insere os dados de um objeto
session.commit()  # necessario fazer o commit()


# Inserir dados (lista de varios objetos)
func1 = Funcionario("Luizinho", 22, 1250)
func2 = Funcionario("Huguinho", 22, 2000)
lista = [func1, func2]
session.add_all(lista)
session.commit()


# Busca todos os dados da tabela
print("-" * 30)
resultado = session.query(Funcionario)  # Retorna lista de objetos
for i in resultado:
    print(i.id, i.nome, i.idade, i.salario)


# Busca um dado específico (pela primary key)
print("-" * 30)
func = session.query(Funcionario).get(2)  # Busca um funcionário pelo id
if func is not None:  # Se não existir, retorna None
    print(func.id, func.nome, func.idade, func.salario)


# Busca utilizando filtros
# salario maior que 1500
print("-" * 30)
d = (
    session.query(Funcionario)
    .filter(Funcionario.salario > 1500)
    .order_by(Funcionario.nome)
)
for i in d:
    print(i.id, i.nome, i.idade, i.salario)


# Busca utilizando filtros (retorna todos)
print("-" * 30)
d = session.query(Funcionario).filter(
    Funcionario.idade == 22 and Funcionario.nome.like("%inho%")
)
for i in d:
    print(i.id, i.nome, i.idade, i.salario)


# Busca utilizando filtros (retorna apenas o primeiro)
print("-" * 30)
d = (
    session.query(Funcionario)
    .filter(Funcionario.idade == 22 and Funcionario.nome.like("%inho%"))
    .first()
)
print(d.id, d.nome, d.idade, d.salario)


# Alterar um registro
func = session.query(Funcionario).get(1)  # Busca um funcionário pelo id
func.nome = "Zezinho da Silva"  # Altera os atributos do objeto
func.idade = 25
session.commit()

# Excluir um registro
func = session.query(Funcionario).get(5)  # busca um funcionário pelo id
if func is not None:
    session.delete(func)
    session.commit()

# Busca todos os dados da tabela
print("-" * 30)
result = session.query(Funcionario)  # retorna lista de objetos
for i in result:
    print(i.id, i.nome, i.idade, i.salario)

# fecha a conexão
connection.close()
