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
    """CREATE TABLE IF NOT EXISTS PACIENTE (
                        ID INTEGER PRIMARY KEY,
                        NOME VARCHAR(255) NOT NULL,
                        CPF VARCHAR(255) NOT NULL,
                        IDADE INT NOT NULL)
                    """
)

connection.execute(
    """CREATE TABLE IF NOT EXISTS MEDICO (
                        ID INTEGER PRIMARY KEY,
                        NOME VARCHAR(255) NOT NULL,
                        CRM VARCHAR(255) NOT NULL,
                        ESPECIALIZACAO VARCHAR(255) NOT NULL)
                    """
)

connection.execute(
    """CREATE TABLE IF NOT EXISTS EXAME (
                        ID INTEGER PRIMARY KEY,
                        ID_MEDICO INT NOT NULL,
                        ID_PACIENTE INT NOT NULL,
                        DESCRICAO VARCHAR(255) NOT NULL,
                        RESULTADO VARCHAR(255) NOT NULL)
                    """
)


class Paciente(Base):
    __tablename__ = "PACIENTE"
    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    nome = Column("NOME", String(255), nullable=False)
    cpf = Column("CPF", String(255), nullable=False)
    idade = Column("IDADE", Integer, nullable=False)

    def __init__(self, nome, cpf, idade):
        self.nome = nome
        self.cpf = cpf
        self.idade = idade


class Medico(Base):
    __tablename__ = "MEDICO"
    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    nome = Column("NOME", String(255), nullable=False)
    crm = Column("CRM", String(255), nullable=False)
    especializacao = Column("ESPECIALIZACAO", String(255), nullable=False)

    def __init__(self, nome, crm, especializacao):
        self.nome = nome
        self.crm = crm
        self.especializacao = especializacao


class Exame(Base):
    __tablename__ = "EXAME"
    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    id_medico = Column("ID_MEDICO", Integer, nullable=False)
    id_paciente = Column("ID_PACIENTE", Integer, nullable=False)
    descricao = Column("DESCRICAO", String(255), nullable=False)
    resultado = Column("RESULTADO", String(255), nullable=False)

    def __init__(self, id_medico, id_paciente, descricao, resultado):
        self.id_medico = id_medico
        self.id_paciente = id_paciente
        self.descricao = descricao
        self.resultado = resultado


# Criar objetos médico e pacientes
medico1 = Medico("Rodolfo", "234565", "Cardiologista")
paciente1 = Paciente("Maria", "044033022-23", 25)
paciente2 = Paciente("João", "022022044-39", 32)

# Inserir médico e pacientes no Banco de Dados
session.add(medico1)
session.add(paciente1)
session.add(paciente2)
session.commit()

# Para criar os exames, é necessário primeiro inserir os medicos e pacientes,
# para que os ids sejam gerados pelo banco de dados

# Criar objetos exames
exame1 = Exame(medico1.id, paciente1.id, "PCR COVID-19", "Negativo")
exame2 = Exame(medico1.id, paciente2.id, "Eletrocardiograma", "Normal")

# Inserir exames no Banco de Dados
session.add(exame1)
session.add(exame2)
session.commit()

# Realiza consultas
lista_medicos = session.query(Medico).all()
lista_pacientes = session.query(Paciente).order_by(Paciente.nome).all()
lista_exames = session.query(Exame).all()

# Exibe os resultados
print("-" * 30)
for m in lista_medicos:
    print(m.id, m.nome, m.crm, m.especializacao)

print("-" * 30)
for p in lista_pacientes:
    print(p.id, p.nome, p.cpf, p.idade)

print("-" * 30)
for e in lista_exames:
    print(e.id, e.id_medico, e.id_paciente, e.descricao, e.resultado)

# Fecha a conexão com o Banco de Dados
connection.close()
