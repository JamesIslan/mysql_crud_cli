from guizero import App, Text, TextBox, PushButton, Box, Picture, Window, ButtonGroup, ListBox
from crud import DataBase

def add(window,name,email,sex,phone):
    connect = DataBase('localhost', 'root', '123', 'aula_conexao_bd')
    connect.create('cliente',fields=['nome', 'email','sexo', 'telefone'],values=[
        name.value,email.value,sex.value,phone.value
    ])
    connect.close()
    window.destroy()
  
def close_window_search():
    window_search_result.hide()
    options.show()

def remove(connection, reg):
    registry_remove = eval(reg.value)
    connection.delete('cliente','id_cliente', registry_remove['id_cliente'])
    connection.close()
    close_window_search()


def window_add():
    window = Window(app,width=300,height=250, layout='grid')
    text_name = Text(window, text='Nome:', grid=[0,0])
    input_name = TextBox(window, grid=[1,0])
    sex_name = Text(window,text='  Sexo:',grid=[2,0])
    sex_input = ButtonGroup(window,options=['m','f'],selected='m', grid=[3,0], horizontal=True)
    ghost_box = Box(window, height='20', grid=[0,1])
    text_email = Text(window, text='Email:', grid=[0,2])
    input_email = TextBox(window,grid=[1,2])
    phone_text = Text(window,text='   Telefone:', grid=[2,2])
    phone_input = TextBox(window,grid=[3,2])
    button = PushButton(window,grid=[0,3],command=add,args=[window,input_name, input_email,sex_input,phone_input])
    window.tk.resizable(0,0)
    window.show()


def edit():
    pass


def search(window):
    search_method = window.question('Método de busca', "Insira o nome dos registros que deseja buscar\nou "
                    "deixe em branco para obter todos os registros.")
    connect = DataBase('localhost', 'root', '123', 'aula_conexao_bd')
    if search_method not in (None, ''):
        rows = connect.read(fields='',table='cliente',where_field='nome',where_value=search_method)
    else:
        rows = connect.read(fields='',table='cliente')
    if len(rows) == 0:
        window.info("Info", "Sua busca não resultou em nenhum registro!")
    else:
        result_search = []
        for reg in rows:
            result_search.append({'id_cliente': reg[0] ,'nome': reg[1] ,'email': reg[2] ,'sexo': reg[3] ,'telefone': reg[4]})
        global window_search_result
        window_search_result = Window(window,width=580, height=345, title='Resultados da busca')
        window_search_result.bg ='#EDE7DF'
        box = Box(window_search_result, width='fill')
        listbox = ListBox(box,items=result_search,scrollbar=True, width=550, height=250)
        ghost_box = Box(window_search_result,width='fill', height=50)
        box_options = Box(window_search_result,width='fill', height=50,layout='grid')
        ghost_box_options = Box(box_options, grid=[0, 0], width=250)
        button_edit = PushButton(box_options, text="Editar", command=edit,grid=[1,0])
        button_remove = PushButton(box_options, text="Excluir", command=remove, grid=[2, 0], args=[connect,listbox])
        button_edit.bg = button_remove.bg = "#CB9888"
        button_edit.font = button_remove.font =  "Calibri"
        listbox.bg='white'
        window_search_result.when_closed = close_window_search
        window_search_result.tk.resizable(0,0)
        window.hide()
        window_search_result.show()


def show_password():
    if pwd_show.image == 'img/senha_nao_visivel.png/':
        pwd_show.image = 'img/senha_visivel.png/'
        pwd_input.hide_text = False
    else:
        pwd_show.image = 'img/senha_nao_visivel.png/'
        pwd_input.hide_text = True


def submit():
    if pwd_input.value.strip() == '' or user_input.value.strip() == '':
        app.info("Inform", "Informe um valor de email e senha para de efetuar o login!")
        pwd_input.value = user_input.value = ''
    else:
        connect = DataBase('localhost', 'root', '123', 'aula_conexao_bd')
        rows = connect.read(fields='usuario,senha',table='usuario')
        data_input = (user_input.value, pwd_input.value)
        connect.close()
        if data_input in rows:
            global options
            options = Window(app, width=400, height=250, bg='#EDE7DF',)
            options.when_closed = app.destroy
            box_options = Box(options,layout='grid')
            options.tk.resizable(0, 0)
            ghost_box = Box(box_options, grid=[0, 0], width=10)
            button_add = PushButton(box_options, text="Adicionar", command=window_add, grid=[1, 0])
            button_search = PushButton(box_options, text="Buscar", command=search, grid=[2, 0], args=[options])
            button_add.bg = button_search.bg ='white'
            app.hide()
            options.show()
        else:
            app.warn(title='Inform', text='Usuário e/ou senha inválidos')
            pwd_input.value = user_input.value = ''



def focus_email():
    user_input.focus()


def focus_password():
    pwd_input.focus()


app = App(title="Gerenciador Cliente", bg='#EDE7DF', width='400', height='250')
app.tk.resizable(0,0)
ghost_box_1 = Box(app, width='fill', height=75)
box_info = Box(app, layout='grid')
user_text = Text(box_info, text="Usuário:", grid=[0, 0], size=15, font='Times')
user_text.when_clicked = focus_email
user_input = TextBox(box_info, grid=[1, 0], width='fill')
user_input.bg = 'white'
pwd_text = Text(box_info, text="Senha:", grid=[0, 1], size=15, font='Times')
pwd_text.when_clicked = focus_password
pwd_input = TextBox(box_info, hide_text=True, grid=[1, 1], width='fill')
pwd_input.bg = 'white'
pwd_show = Picture(box_info, image="img/senha_nao_visivel.png/", grid=[2, 1])
pwd_show.when_clicked = show_password
ghost_box_2 = Box(box_info, grid=[1, 2], height=15, width=1)
button_submit = PushButton(box_info, text="Fazer login", grid=[1, 3], width='13', command=submit)
button_submit.font = "Calibri"
button_submit.bg = "#CB9888"
app.display()