import PySimpleGUI as sg

def tela_login():
    
    event, values = sg.Window('Login Window',
                    [[sg.T('Enter your Login ID'), sg.In(key='-ID-')],
                    [sg.B('OK'), sg.B('Cancelar') ]]).read(close=True)
    
    return values['-ID-'],event
   

def main():
    
    id = tela_login()
    print(id[1])
    if id[1]=='OK':
       if id[0]!='':
           sg.popup('Seu login é:', id[0])
       else:
           sg.popup("login inválido!")

    else:
        sg.Window.close()

main()