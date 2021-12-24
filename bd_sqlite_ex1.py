import sqlite3
import os


def criaBanco():
    global conexão,cursor
    if not os.path.exists('agenda.db'):
        
        conexão = sqlite3.connect("agenda.db")
        cursor = conexão.cursor()
        
        sql_contato_create= 'create table contato('\
                'id integer primary key autoincrement,'\
                'nome varchar(50) not null unique)'

        sql_telefones_create = 'create table telefones('\
                'id_fone integer primary key autoincrement,'\
                'numero varchar(20) not null,'\
                'descricao varchar(30) not null,' \
                'id_contato integer not null,'\
                'FOREIGN KEY (id_contato) REFERENCES contato(id))'              

        cursor.execute(sql_contato_create)
        cursor.execute(sql_telefones_create)
        conexão.commit()

def adiciona_contato_db(nome):
    global conexão,cursor
    sql_contato = 'insert into contato (nome) values (?)'
    cursor.execute(sql_contato,[nome])

def adiciona_telefones_db(id_contato,fones):
    global conexão,cursor
    sql_telefones = 'insert into telefones (numero,descricao,id_contato) values (?,?,?)'  
    for i in fones:
        cursor.execute(sql_telefones,[i[0],i[1],id_contato])


def adiciona_fones():
    
    fones=[]  
    while True:     
        
        fone=input(f'Telefone:')
        desc = input("descrição:")
        if fone=='':
            fone=None
        if desc=='':
            desc=None
        fones.append((fone,desc))
        print(fones)
        conf = input("deseja cadastrar outro telefone para este contato?(S/N)")
        if conf in "Ss":
            pass   
        elif conf in "Nn":
            break
    return fones
   

def cadastro():
    global conexão,cursor
    if conexão==None:
        conexão = sqlite3.connect("agenda.db")
        cursor = conexão.cursor()
    
    nome = input("Entre com o nome:")
    if nome=='':
        nome=None
    else:
        res=consultar('contato','id,nome','nome',nome)
        print(res)
        if len(res)>0:
            id=res[0][0]
            res = consultar('telefones','numero,descricao','id_contato',id)
            if len(res)>0:
                print('telefones cadastrados')
                for i in res:
                    print(i)
            else:
                print('Não há telefones cadastrados para este contato!')
        else:
            fones=adiciona_fones()
            # sentença SQL para inserir registros
            
            try:
                adiciona_contato_db(nome)
                id_contato = cursor.lastrowid
                adiciona_telefones_db(id_contato)
                conexão.commit()
            except:
                print('Erro de integridade do banco de dados!')    

            
def atualizar_contato():
    global conexão,cursor
    if conexão==None:
        conexão = sqlite3.connect("agenda.db")
        cursor = conexão.cursor()
    print('--------------------------------')
    print('  Consultar/atualizar contato')
    print('--------------------------------')
    nome = input('Digite o nome do contato:')
    sql = f"select * from contato where nome like '%{nome}%'"
    cursor.execute(sql)
    res = cursor.fetchall()
    if len(res)>0:
        for i in res:
          print(i)
        resp=int(input('Digite o numero do contato para ser atualizado ou "0" para sair:'))
        if resp!=0:
            id_contato=resp
            res=consultar('contato','id,nome','id',id_contato)
            if len(res)>0:
                id_contato=res[0][0]
                print(f'Nome:{res[0][1]}')
                res2=consultar('telefones','id_fone,numero,descricao','id_contato',id_contato)   
                
                if len(res2)>0:
                    print('--------------------------------')
                    print('          Telefones             ')
                    print('--------------------------------') 
                    for i in res2:
                        print(i)
                    menu('Menu',['1-Altera contato','2-Exclui contato','3-Inclui Telefone','4-Altera Telefone','5-Exclui telefone','6-Sair'])

                    op=int(input('Entre com a opção:'))
                    if op==1:
                        novo_nome=input('Digite o novo nome:')
                        sql=f'UPDATE contato SET nome=? WHERE id=?'
                        cursor.execute(sql,[novo_nome,id_contato])
                    elif op==2:
                        sql=f'DELETE FROM contato WHERE id=?'
                        cursor.execute(sql,[id_contato])
                    elif op==3:
                        fones = adiciona_fones()
                        adiciona_telefones_db(id_contato,fones)

                    elif op==4:
                        id_fone=int(input('Digite o id do telefone a ser alterado:'))
                        novo_numero=input('Digite o novo numero de telefone:')
                        nova_desc= input('Digite a nova descrição:')
                        sql='UPDATE telefones set numero=?, descricao=? WHERE id_fone=?'
                        cursor.execute(sql,[novo_numero,nova_desc,id_fone])
                    elif op==5:
                        id_fone=int(input('Digite o id do telefone a ser excluído:'))
                        sql='DELETE from telefones where id_fone=?'
                        cursor.execute(sql,[id_fone])

                    elif op==6:
                        exit

                else:
                    
                    print('Sem telefones cadastrados!')
                    resp=input('Deseja incluir um novo numero de telefone?(S/N)')
                    if resp in "Ss":
                        fones = adiciona_fones()
                        adiciona_telefones_db(id_contato,fones)
                conexão.commit()

            else:
                print('Contato não cadastrado!')   
    else:
        print('contato não cadastrado!')                     
        
            

def consultar(tabela,campos,campo_cond,valor):
    sql = f'select {campos} from {tabela} where {campo_cond} = ?'
    cursor = conexão.cursor()
    cursor.execute(sql,[valor])
    res = cursor.fetchall()
    return res
    
def menu(titulo,lista):
   print(titulo)
   for i in lista:
       print(i)
   
    

def main():
    global conexão, cursor
    
    conexão=None
    cursor=None

    criaBanco()
    while True:
        menu('Menu Principal',['1-Novo contato','2-Atualizar contato','3-Sair'])
        op=int(input('Opção:'))
        if op==1:
            cadastro()
        elif op==2:
            atualizar_contato()
        elif op==4:
            break
    if cursor!=None:
       cursor.close()
    if conexão!=None:
       conexão.close()

    

#main()

    