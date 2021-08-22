import sqlalchemy

from sqlalchemy import Column, Integer, String, Float, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# Criar Conexão com Banco SQLITE
engine = sqlalchemy.create_engine("sqlite:///server.db")
connection = engine.connect()
Base = declarative_base(engine)
session = Session()

# Mapeamento da tabela
class Filme(Base):
    __tablename__ = 'FILME'
    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    titulo = Column('TITULO', String(255))
    ano = Column('ANO', Integer)
    genero = Column('GENERO', String(255))
    duracao = Column('DURACAO', Integer)
    pais = Column('PAIS', String(255))
    diretor = Column('DIRETOR', String(255))
    elenco = Column('ELENCO', String(255))
    avaliacao = Column('AVALIACAO', Float)
    votos = Column('VOTOS', Integer)

    # Método construtor
    def __init__(self, titulo, ano, genero, duracao, pais, diretor, elenco, avaliacao, votos):
        self.titulo = titulo
        self.ano = ano
        self.genero = genero
        self.duracao = duracao
        self.pais = pais
        self.diretor = diretor
        self.elenco = elenco
        self.avaliacao = avaliacao
        self.votos = votos


# Classe para interação com o Banco de Dados
class BancoDeDados:
    def criar_tabela(self):

        # Cria a tabela FILME no banco de dados
        connection.execute("""CREATE TABLE IF NOT EXISTS FILME(
                              ID INTEGER PRIMARY KEY,
                              TITULO VARCHAR(255) NOT NULL,
                              ANO INT NOT NULL,
                              GENERO VARCHAR(255) NOT NULL,
                              DURACAO INT NOT NULL,
                              PAIS VARCHAR(255) NOT NULL,
                              DIRETOR VARCHAR(255) NOT NULL,
                              ELENCO VARCHAR(255) NOT NULL,
                              AVALIACAO FLOAT NOT NULL,
                              VOTOS INT NOT NULL)""")

    def incluir(self, filme):
        '''
        Recebe um objeto Filme e armazena esse
        objeto no banco de dados.
        '''
        session.add(filme)
        session.commit()

    def incluir_lista(self, filmes):
        '''
        Recebe uma lista de objetos Filme e armazena esses
        objetos no banco de dados
        '''
        session.add_all(filmes)
        session.commit()

    def alterar_avaliacao(self, filme, avaliacao):
        '''
        Recebe um objeto filme e altera sua avaliação de
        acordo com o valor do parametro avaliacao
        '''
        filme.avaliacao = avaliacao
        session.commit()

    def excluir(self, id):
        '''
        Recebe o id de um filme e exclui o filme correspondente
        do banco de dados
        '''
        obj = session.query(Filme).get(id)
        if obj is not None:
            session.delete(obj)
        session.commit()

    def buscar_todos(self):
        '''
        Realiza busca no banco de dados e retorna uma
        lista de objetos Filme com todos os registros,
        ordenados de forma crescente pelo titulo.
        '''
        lista = session.query(Filme).order_by(Filme.titulo).all()
        return lista

    def buscar_por_id(self, id):
        '''
        Realiza busca no banco de dados e retorna um
        objeto Filme de acordo com o seu id
        '''
        obj = session.query(Filme).get(id)
        return obj

    def buscar_por_ano(self, ano):
        '''
        Realiza busca no banco de dados e retorna uma
        lista de objetos Filme de um ano específico,
        ordenado pelo ID de forma crescente
        '''
        lista = session.query(Filme).filter(Filme.ano == ano).order_by(Filme.id).all()
        return lista

    def buscar_por_genero(self, genero):
        '''
        Realiza busca no banco de dados e retorna uma
        lista de objetos Filme de um gênero específico,
        ordenados pelo titulo de forma crescente
        '''
        lista = session.query(Filme).filter(Filme.genero.like('%'+genero+'%')).order_by(Filme.titulo).all()
        return lista

    def buscar_por_elenco(self, ator):
        '''
        Realiza busca no banco de dados e retorna uma
        lista de objetos Filme que tenha um determinado ator/atriz como parte
        do elenco, ordenados pelo ano de lançamento em ordem crescente
        '''
        lista = session.query(Filme).filter(Filme.elenco.like('%'+ator+'%')).order_by(Filme.ano).all()
        return lista

    def buscar_melhores_do_ano(self, ano):
        '''
        Realiza busca no banco de dados e retorna uma lista de
        objetos Filme de um ano específico, com avaliação
        maior ou igual a 90
        Deve retornar ordenado pela avaliação de forma decrescente.
        DICA - utilize a função:
            .order_by(desc(Filme.avaliacao))
        '''
        lista = session.query(Filme).filter(Filme.ano == ano, Filme.avaliacao >= 90).order_by(desc(Filme.avaliacao)).all()
        return lista

    def exportar_filmes(self, nome_arquivo):
        '''
        Exporta os dados contidos na tabela de filmes para um arquivo de texto
        O arquivo deve conter uma listagem dos filmes, ordenados pelos titulos
        dos filmes, contendo os dados de cada filme em uma linha, no formato:
        titulo;ano;genero;duracao;país;diretor;elenco;avaliacao;votos
        '''
        resultado = self.buscar_todos()
        arquivo = open(nome_arquivo, 'w', encoding="utf-8")
        for f in resultado:
            arquivo.write('{};{};{};{};{};{};{};{};{}\n'.format(
                f.titulo,
                f.ano,
                f.genero,
                f.duracao,
                f.pais,
                f.diretor,
                f.elenco,
                f.avaliacao,
                f.votos
            ))
        arquivo.close()
        
    def importar_filmes(self, nome_arquivo):
        '''
        Recebe como parâmetro o nome de um arquivo de texto e importa os
        dados contidos no arquivo para o banco de dados.
        Considere que o arquivo contém uma listagem de filmes no formato:
        titulo;ano;genero;duracao;país;diretor;elenco;avaliacao;votos
        '''
        # Abrir Arquivo
        arquivo = open(nome_arquivo, "r", encoding="utf-8")
        lista = []
        for linha in arquivo:
            dados = linha.split(';')
            filme = Filme(dados[0], int(dados[1]), dados[2], int(dados[3]), dados[4], dados[5], dados[6], float(dados[7]), int(dados[8]))
            lista.append(filme)
        arquivo.close()
        self.incluir_lista(lista)


# PROGRAMA COM TESTES PARA AS FUNÇÕES SOLICITADAS
banco = BancoDeDados()
banco.criar_tabela()

try:
    # Importa filmes do arquivo de texto e salva no banco de dados
    banco.importar_filmes('movies.txt')
    print("ACERTO - importar_filmes")
except AssertionError:
    print("ERRO   - importar_filmes")
except Exception:
    print("ERRO   - importar_filmes")

try:
    # Busca por id existente
    filme = banco.buscar_por_id(100)
    assert filme is not None
    assert filme.titulo == 'Project Gio'
    print("ACERTO - buscar_por_id")
except AssertionError:
    print("ERRO   - buscar_por_id")
except Exception:
    print("ERRO   - buscar_por_id")
    
try:
    # Busca por id inexistente
    filme = banco.buscar_por_id(77777)
    assert filme is None
    print("ACERTO - buscar_por_id inexistente")
except AssertionError:
    print("ERRO   - buscar_por_id inexistente (deve retornar None se id não existir)")
except Exception:
    print("ERRO   - buscar_por_id inexistente (deve retornar None se id não existir)")

try:
    # Busca todos os filmes
    lista = banco.buscar_todos()
    c = 0
    for x in lista:     # Conta a quantidade de itens na lista de retorno
        c += 1
    assert c == 993
    assert lista[0].id == 69
    assert lista[0].titulo == 'A Beauty & The Beast Christmas'
    assert lista[-1].id == 143
    assert lista[-1].titulo == 'Zuo jia de huang yan: Bi zhong you zui'
    print("ACERTO - buscar_todos")
except AssertionError:
    print("ERRO   - buscar_todos")
except Exception:
    print("ERRO   - buscar_todos")

try:
    # Busca todos os filmes do ano de 2019
    lista = banco.buscar_por_ano(2020)
    c = 0
    for x in lista:     # Conta a quantidade de itens na lista de retorno
        c += 1
    assert c == 109
    assert lista[0].id == 14
    assert lista[0].titulo == 'Trolls World Tour'
    assert lista[-1].id == 993
    assert lista[-1].titulo == 'Body Cam'
    print("ACERTO - buscar_por_ano")
except AssertionError:
    print("ERRO   - buscar_por_ano")
except Exception:
    print("ERRO   - buscar_por_ano")

try:
    # Busca todos os filmes contendo o gênero 'Crime'
    lista = banco.buscar_por_genero('Crime')
    c = 0
    for x in lista:     # Conta a quantidade de itens na lista de retorno
        c += 1
    assert c == 83
    assert lista[0].id == 374
    assert lista[0].titulo == 'A Vigilante'
    assert lista[-1].id == 143
    assert lista[-1].titulo == 'Zuo jia de huang yan: Bi zhong you zui'
    print("ACERTO - buscar_por_genero")
except AssertionError:
    print("ERRO   - buscar_por_genero")
except Exception:
    print("ERRO   - buscar_por_genero")

try:
    # Busca todos os filmes com participação da atriz de nome 'Nicole Balsam'
    lista = banco.buscar_por_elenco('Nicole Balsam')
    c = 0
    for x in lista:     # Conta a quantidade de itens na lista de retorno
        c += 1
    assert c == 2
    assert lista[0].id == 426
    assert lista[0].titulo == 'Stretch Marks'
    assert lista[-1].id == 44
    assert lista[-1].titulo == 'Nighthawks'
    print("ACERTO - buscar_por_elenco")
except AssertionError:
    print("ERRO   - buscar_por_elenco")
except Exception:
    print("ERRO   - buscar_por_elenco")

try:
    # Cria um novo Filme e insere no banco de dados
    filme1 = Filme("Parasite", 2019, "Comedy, Drama, Thriller", 132, "Korea", "Bong Joon Ho", "Song Kang-ho, Jang Hye-jin, Choi Woo-shik", 92, 40273)
    banco.incluir(filme1)
    lista = banco.buscar_todos()
    c = 0
    for x in lista:     # Conta a quantidade de itens na lista de retorno
        c += 1
    assert c == 994
    print("ACERTO - incluir")
except AssertionError:
    print("ERRO   - incluir")
except Exception:
    print("ERRO   - incluir")

try:
    # Cria uma lista com dois novos filmes e insere no banco de dados
    filme2 = Filme("Joker", 2019, 'Crime, Drama, Thriller', 122, "USA", "Todd Phillips", "Joaquin Phoenix, Robert De Niro, Zazie Beetz", 91, 78481)
    filme3 = Filme("Avengers: Endgame", 2019, 'Drama, Thriller', 181, "USA", "Anthony Russo, Joe Russo", "Robert Downey Jr., Chris Evans, Mark Ruffalo", 93, 715250)
    lista_filmes = [filme2, filme3]
    banco.incluir_lista(lista_filmes)
    lista = banco.buscar_todos()
    c = 0
    for x in lista:         # Conta a quantidade de itens na lista de retorno
        c += 1
    assert c == 996
    print("ACERTO - incluir_lista")
except AssertionError:
    print("ERRO   - incluir_lista")
except Exception:
    print("ERRO   - incluir_lista")

try:
    # Busca os melhores filmes do ano de 2019
    lista = banco.buscar_melhores_do_ano('2019')
    c = 0
    for x in lista:     # Conta a quantidade de itens na lista de retorno
        c += 1
    assert c == 3
    assert lista[0].id == 996
    assert lista[0].titulo == 'Avengers: Endgame'
    assert lista[-1].id == 995
    assert lista[-1].titulo == 'Joker'
    print("ACERTO - buscar_melhores_do_ano")
except AssertionError:
    print("ERRO   - buscar_melhores_do_ano")
except Exception:
    print("ERRO   - buscar_melhores_do_ano")

try:
    # Altera a avaliação do filme de id 7 para 98
    filme = banco.buscar_por_id(7)
    if filme is not None:
        banco.alterar_avaliacao(filme, 98.0)
    filme = banco.buscar_por_id(7)
    assert filme.avaliacao == 98.0
    print("ACERTO - alterar_avaliacao")
except AssertionError:
    print("ERRO   - alterar_avaliacao")
except Exception:
    print("ERRO   - alterar_avaliacao")

try:
    # Exclui o filme de id 6
    banco.excluir(6)
    filme = banco.buscar_por_id(6)
    assert filme is None
    lista = banco.buscar_todos()
    c = 0
    for x in lista:     # Conta a quantidade de itens na lista de retorno
        c += 1
    assert c == 995
    print("ACERTO - excluir")
except AssertionError:
    print("ERRO   - excluir")
except Exception:
    print("ERRO   - excluir")


try:
    # Tenta Excluir filme de id inexistente
    banco.excluir(4444444)
    print("ACERTO - excluir filme inexistente")
except AssertionError:
    print("ERRO   - excluir filme inexistente")
except Exception:
    print("ERRO   - excluir filme inexistente (deve verificar se filme existe, antes de excluir")

try:
    # Exporta filmes do banco de dados para um novo arquivo de texto
    banco.exportar_filmes('saida.txt')
    print("ACERTO - exportar_filmes")
except AssertionError:
    print("ERRO   - exportar_filmes")
except Exception:
    print("ERRO   - exportar_filmes")
