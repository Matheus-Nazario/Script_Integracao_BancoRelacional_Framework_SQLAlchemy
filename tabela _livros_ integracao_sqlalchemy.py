# Conectar com o banco de dados SQLITE e criar as
# tabelas AUTOR e LIVRO (utilize os scripts abaixo para a criação das tabelas).

import sqlalchemy
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# Criar Conexão com Banco SQLITE
# caso o arquivo de banco não exista, ele será criado
engine = sqlalchemy.create_engine("sqlite:///server_ex2.db")
connection = engine.connect()

# Criar sessão com o Banco de Dados
Base = declarative_base(engine)
session = Session()


# Criar tabela no banco de dados, caso não exista

connection.execute(
    """CREATE TABLE IF NOT EXISTS AUTOR(
           ID INTEGER PRIMARY KEY,
           NOME varchar(255) NOT NULL)"""
)

connection.execute(
    """CREATE TABLE IF NOT EXISTS LIVRO(
           ID INTEGER PRIMARY KEY,
           TITULO VARCHAR(255) NOT NULL,
           PAGINAS INT NOT NULL,
           AUTOR_ID INT NOT NULL)"""
)

# Mapeamento da tabela Criar as classes Autor e Livro e fazer o mapeamento das tabelas
class Autor(Base):
    __tablename__ = "AUTOR"
    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    nome = Column("NOME", String(255), nullable=False)

    def __init__(self, nome):
        self.nome = nome


# Mapeamento da tabela
class Livro(Base):
    __tablename__ = "LIVRO"
    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    titulo = Column("TITULO", String(255), nullable=False)
    paginas = Column("PAGINAS", Integer, nullable=False)
    autor_id = Column("AUTOR_ID", Integer, nullable=False)

    def __init__(self, titulo, paginas, autor_id):
        self.titulo = titulo
        self.paginas = paginas
        self.autor_id = autor_id


# Inserir nas tabelas dois autores e dois livros.

autor1 = Autor("Dan Brown")
autor2 = Autor("J. K. Rowling")

lista_de_autores = [autor1, autor2]

session.add_all(lista_de_autores)
session.commit()

livro1 = Livro("O Código Da Vinci", 200, 999999999)
livro2 = Livro("Harry Potter e o Enigma do Príncipe", 800, 88888888)

lista_de_livros = [livro1, livro2]

session.add_all(lista_de_livros)
session.commit()

# Fazer uma consulta para verificar
# se os dados foram inseridos corretamente.
resultado_autores = session.query(Autor)
print(" - " * 30)
for i in resultado_autores:
    print("ID: {} | Nome: {} ".format(i.id, i.nome))
print(" - " * 30)

resultado_livros = session.query(Livro)
print(" - " * 30)
for i in resultado_livros:
    print(
        "ID: {} | Titulo: {} | Paginas: {} | Autor_id: {}".format(
            i.id, i.titulo, i.paginas, i.autor_id
        )
    )
print(" - " * 30)

# fecha a conexão
connection.close()
