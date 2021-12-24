# C - Create (criar um novo registro no banco)
# R - Read (ler/consultar um registro)
# U - Update (atualizar um registro)
# D - Delete (excluir um registro do banco)
import peewee
from models import contato,telefones

def adiciona_fones(id_contato):
    
    fones=[]  
    while True:     
        
        fone=input(f'Telefone:')
        desc = input("descrição:")
        if fone=='':
            fone=None
        if desc=='':
            desc=None
        fones.append({'numero':fone,'descricao':desc,'id_contato_id':id_contato})
        #print(fones)
        conf = input("deseja cadastrar outro telefone para este contato?(S/N)")
        if conf in "Ss":
            pass   
        elif conf in "Nn":
            break
    return fones
def inserir():
    # Inserimos dois contatos  na tabela 'contatos'
    '''  
    maria = contato.create(nome='MARIA')
    joão = contato.create(nome='JOÃO')
    
    telefone_1 = {
        'numero':'9999-1122',
        'descricao' : 'celular',
        'id_contato_id': maria,
    }
    telefone_2 = {
        'numero':'3333-1010',
        'descricao' : 'casa',
        'id_contato_id': maria,
    }
    telefone_3 = {
        'numero':'98767-9876',
        'descricao' : 'celular',
        'id_contato_id': joão,
    }
    fones = [telefone_1,telefone_2,telefone_3]
    telefones.insert_many(fones).execute()
    '''
    try:
        nome_contato = input('Entre com o nome do contato:')
        novo_contato = contato.create(nome=nome_contato)
        fones = adiciona_fones(novo_contato)
        telefones.insert_many(fones).execute()

        #telefones.insert({'numero':'9898-0076','descricao':'sd876fssa','id_contato_id':paulo}).execute()
        #fone1 = telefones.create(numero='98989-1212',descricao='celular',id_contato_id=edu)
    except peewee.OperationalError:
        print ("Erro ao inserir registros!")

def print_menu(titulo,lista):
   print(titulo)
   for i in lista:
       print(i)

def consulta_por_nome(nome):
    fones=[]
    res = telefones.select().join(contato).where(contato.nome==nome)
    if res.count()>0:
        for i in res:
            fones.append({'id':i.id,'numero':i.numero,'descricao':i.descricao})
    return fones

def consultar():
    print('1-Consultar contato pelo número')
    print('2-Consultar numeros de telefone pelo contato')
    op=int(input('escolha a opção:'))
    if op==1:
        numero = input('Entre com um numero de telefone:')
        
        res1 = telefones.get_or_none(telefones.numero == numero)
        if res1!=None:                
            res2 = contato.get(contato.id == res1.id_contato_id)
            print(f'O nome do contato é:{res2.nome}')
        else:
            print('telefone não encontrado na agenda!')         
    elif op==2:
        nome = input('Entre com o nome do contato:')
        try:
            #res1 = contato.get(contato.nome == nome)
            # res2 = telefones.select().where(id_contato_id=res1.id)
            fones = consulta_por_nome(nome)
            print(fones)
            if len(fones) >0:
            #res2 = telefones.select().join(contato).where(contato.nome==nome)
            #if res2.count()>0:
                print('numero    |  descrição')
                print('----------------------')
                for i in fones:
                    print(f"{i['numero']} | {i['descricao']}" )
                    
                input('pressione <ENTER> para voltar ao menu...')
            else:
                print('Contato não existente ou sem telefones cadastrados!')
        except peewee.DatabaseError:
            print('Erro no banco de dados!')
    
def atualizar():
    print('--------------------------------')
    print('  atualizar contato')
    print('--------------------------------')
    nome = input('Digite o nome do contato:')
    fones = consulta_por_nome(nome)
    
    if len(fones)>0:
        res_contato = contato.get_or_none(contato.nome == nome)
        print('id|  numero   |  descrição')
        print('----------------------')
        for i in fones:
            print(f"{i['id']} | {i['numero']} | {i['descricao']}")    

        print_menu('Menu',['1-Altera contato','2-Exclui contato','3-Inclui Telefone','4-Altera Telefone','5-Exclui telefone','6-Sair'])
        op=int(input('Entre com a opção:'))
        if op==1:
            novo_nome=input('Digite o novo nome:')
            res_contato.nome = novo_nome
            if res_contato.save() > 0:
                print('Alteração efetuada com sucesso!')
                        
        elif op==2:
            try:

                res_contato.delete_instance(True)
                print('contato excluido com sucesso!)')
            except peewee.DatabaseError:
                print('Exclusão não permitida!')
                        
        elif op==3:
            try:
                fones = adiciona_fones(res_contato.id)
                telefones.insert_many(fones).execute()
            except peewee.DatabaseError:
                print('Erro ao inserir no banco de dados!')
                       

        elif op==4:
            id_fone=int(input('Digite o id do telefone a ser alterado:'))
            res_fone = telefones.get_or_none(telefones.id == id_fone)
            if res_fone!= None:
                novo_numero=input('Digite o novo numero de telefone:')
                nova_desc= input('Digite a nova descrição:')
                res_fone.numero = novo_numero
                res_fone.descricao = nova_desc
                if res_fone.save()>0:
                    print('Alteração efetuada com sucesso!')
                else:
                    print('Alteração não realizada.')
            else:
                print('id não encontrado!')       
        elif op==5:
                id_fone=int(input('Digite o id do telefone a ser excluído:'))
                res_fone = telefones.get_or_none(telefones.id == id_fone)
                if res_fone!= None:
                    if res_fone.delete_instance() > 0:
                        print('Telefone excluído com sucesso!')
                    else:
                        print('Exclusão não efetuada!')
                else:
                    print('id não encontrado!')

        elif op==6:
            exit
    else:
        print('Nome de contato inexistente ou sem telefones cadastrados!')


def menuprincipal():
    while True:
        print("1-Inserir")
        print("2-Consultar")
        print("3-Atualizar")
        print("4-Sair")
        op=int(input("Opção:"))
        if op==1:
            inserir()
        elif op==2:
            consultar()
        elif op==3:
            atualizar()
        elif op==4:
            break
        

def main():
    menuprincipal()       
    
if __name__ == '__main__':
    main()