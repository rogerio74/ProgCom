import peewee

# Criamos o banco de dados
db = peewee.SqliteDatabase('agenda2.db')


class BaseModel(peewee.Model):
    """Classe model base"""

    class Meta:
        # seleciona em qual banco de dados as tabelas serão criadas 
        database = db

class contato(BaseModel):

    """
    Classe que representa a tabela contato
    """
    # A tabela possui apenas o campo 'nome', que receberá o nome do contato que sera unico
    nome = peewee.CharField(unique=True)

class telefones(BaseModel):
    """
    Classe que representa a tabela telefones
    """
  
    numero = peewee.CharField(unique=True)
    descricao = peewee.CharField()

    # Chave estrangeira para a tabela Contato
    id_contato = peewee.ForeignKeyField(contato)

if __name__ == '__main__':
    try:
        contato.create_table()
        print("Tabela 'contato' criada com sucesso!")
    except peewee.OperationalError:
        print("Tabela 'contato' ja existe!")

    try:
        telefones.create_table()
        print("Tabela 'telefones' criada com sucesso!")
    except peewee.OperationalError:
        print("Tabela 'telefones' ja existe!")