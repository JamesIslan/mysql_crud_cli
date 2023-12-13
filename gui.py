from guizero import App, Text, TextBox, PushButton, Box, Picture, Window, ButtonGroup


def block_window(app: App):
    app.tk.attributes('-toolwindow', 1)
    app.tk.resizable(False, False)


def check_options():
    pass


def add():
    pass


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
    if pwd_input.value.strip() == '' or email_input.value.strip() == '':
        app.info("Inform", "Informe um valor de email e senha para de efetuar o login!")
        pwd_input.value = email_input.value = ''
    else:
        if email_input.value == 'admin' and pwd_input.value == '123':
            options = Window(app, width=400, height=400, layout='grid')
            options.tk.resizable(0, 0)
            ghost_box = Box(options, grid=[0, 0], width=65)
            button_add = PushButton(options, text="Adicionar", command=add, grid=[1, 0])
            button_edit = PushButton(options, text="Editar", command=edit, grid=[2, 0])
            button_search = PushButton(options, text="Buscar", command=search, grid=[3, 0])
            button_remove = PushButton(options, text="Excluir", command=remove, grid=[4, 0])
            app.hide()
            options.show()


def focus_email():
    email_input.focus()


def focus_password():
    pwd_input.focus()


app = App(title="Gerenciador MEPOUPE", bg='#EDE7DF', width='400', height='250')
block_window(app)
ghost_box_1 = Box(app, width='fill', height=75)
box_info = Box(app, layout='grid')
email_text = Text(box_info, text="Email:", grid=[0, 0], size=15, font='Times')
email_text.when_clicked = focus_email
email_input = TextBox(box_info, grid=[1, 0], width='fill')
email_input.bg = 'white'
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
