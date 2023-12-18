from guizero import App, Text, TextBox, PushButton, Box, Picture, Window, ButtonGroup
from crud import DataBase


def check_options():
    pass


def add(window, name, email, sex, phone):
    connect = DataBase('localhost', 'root', '123', 'aula_conexao_bd')
    connect.create('cliente', fields=['nome', 'email', 'sexo', 'telefone'], values=[
        name.value, email.value, sex.value, phone.value
    ])
    connect.close()
    window.destroy()


def window_add():
    window = Window(app, width=300, height=250, layout='grid')
    text_name = Text(window, text='Nome:', grid=[0, 0])
    input_name = TextBox(window, grid=[1, 0])
    sex_name = Text(window, text='  Sexo:', grid=[2, 0])
    sex_input = ButtonGroup(window, options=['m', 'f'], selected='m', grid=[3, 0], horizontal=True)
    ghost_box = Box(window, height='20', grid=[0, 1])
    text_email = Text(window, text='Email:', grid=[0, 2])
    input_email = TextBox(window, grid=[1, 2])
    phone_text = Text(window, text='   Telefone:', grid=[2, 2])
    phone_input = TextBox(window, grid=[3, 2])
    button = PushButton(window, grid=[0, 3], command=add, args=[
                        window, input_name, input_email, sex_input, phone_input])
    window.tk.resizable(0, 0)
    window.show()


def edit():
    pass


def search():
    pass


def remove():
    pass


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
        rows = connect.read(fields='usuario,senha', table='usuario')
        data_input = (user_input.value, pwd_input.value)
        connect.close()
        if data_input in rows:
            options = Window(app, width=400, height=400, layout='grid', bg='#EDE7DF',)
            options.tk.resizable(0, 0)
            ghost_box = Box(options, grid=[0, 0], width=65)
            button_add = PushButton(options, text="Adicionar", command=window_add, grid=[1, 0])
            button_edit = PushButton(options, text="Editar", command=edit, grid=[2, 0])
            button_search = PushButton(options, text="Buscar", command=search, grid=[3, 0])
            button_remove = PushButton(options, text="Excluir", command=remove, grid=[4, 0])
            button_add.bg = button_edit.bg = button_remove.bg = button_search.bg = 'white'
            app.hide()
            options.show()
        else:
            app.warn(title='Inform', text='Usuário e/ou senha inválidos')
            pwd_input.value = user_input.value = ''


def focus_email():
    user_input.focus()


def focus_password():
    pwd_input.focus()


app = App(title="Gerenciador MEPOUPE", bg='#EDE7DF', width='400', height='250')
app.tk.resizable(0, 0)
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
