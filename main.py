from crudfuncs import *
from os import getenv
from dotenv import load_dotenv
from os import system
from pprint import pprint

def show_options():
    print(f'1 - Inserir Usuário')
    print(f'2 - Editar Usuário')
    print(f'3 - Remover Usuário')
    print(f'4 - Buscar Usuário')
    print(f'0 - Encerrar Programa')
    return None

def get_attr_options(attr: tuple | list):
    int_enum = enumerate(attr, 1)
    str_enum = [(str(i[0]), i[1]) for i in int_enum]
    return dict(str_enum)

def show_attr_options(options: dict):
    for k, v in options.items():
        print(f'{k} – {v}')

def display_db_response(raw_response: tuple | list):
    for row in raw_response:
        pprint(row, width=100)
        # print((" "*10).join(row))


def main() -> None:
    load_dotenv()
    db = DataBase(
        host=getenv("HOST", ""),
        user=getenv("USER", ""),
        password=getenv("PASSWORD", ""),
        db_name=getenv("DB_NAME", ""))
    while True:
        show_options()
        desired_option = input('Opção Desejada: ')
        match desired_option:
            case '1':
                data = lambda: input(
                    'Nome, Email, Sexo, Telefone (separado por espaços): '
                    ).split()
                while len(inner := data()) != 4:
                    print('Há parâmetros faltando!')
                    continue
                db.insert('cliente', inner)
            case '2':
                # Checagem ID
                registry_id = lambda: input('ID a ser alterado: ')
                while inner_id := registry_id():
                    attribute_checking = db.check_value(
                        table='cliente',
                        attribute='id_cliente',
                        value=inner_id
                    )
                    if not attribute_checking:
                        print('O ID informado não existe!')
                        continue
                    break
                # Campo Alterado
                update_field = lambda: input('Campo a ser alterado: ') # Desconsidere
                table_fields = db.get_fields('cliente')
                update_options = get_attr_options(table_fields)
                print('Que campo você deseja alterar?: ')
                show_attr_options(update_options) # 1 - nome; 2 - email; 3 - sexo; 4 - telefone
                while inner_option := update_field():
                    if inner_option not in list(update_options.keys()):
                        print('O campo informado não existe!')
                        continue
                    break
                inner_field = update_options[inner_option]
                new_reg_value = input(f'Novo valor para o campo {inner_field}: ')
                db.update_value(
                    table='cliente',
                    attribute=inner_field,
                    newvalue=new_reg_value,
                    id_field='id_cliente',
                    id_value=inner_id
                )
                print('Alteração feita com sucesso!')
            case '3':
                # Id Field Input
                # id_field = lambda: input('Nome do Campo: ')
                # while inner_field := id_field():
                #     field_checking = db.check_field(table='cliente', field=inner_field)
                #     if not field_checking:
                #         print('O campo informado não existe!')
                #         continue
                #     break
                registry_id = lambda: input('ID do atributo a ser removido: ')
                while inner_id := registry_id():
                    attribute_checking = db.check_value(
                        table='cliente',
                        attribute='id_cliente',
                        value=inner_id
                    )
                    if not attribute_checking:
                        print('O ID informado não existe!')
                        continue
                    break
                db.delete('cliente', 'id_cliente', inner_id)
                print('Registro removido!')
            case '4':
                # Buscar todos os clientes
                # Buscar clientes pelo nome
                update_field = lambda: str(input(
                    'Campos a serem exibidos (separados por espaço): '
                    )).split()
                table_fields = db.get_fields('cliente')
                update_options = get_attr_options(table_fields)
                available_options = list(update_options.keys())
                # print('Que campo você deseja alterar?: ')
                show_attr_options(update_options) # 1 - nome; 2 - email; 3 - sexo; 4 - telefone
                while inner_options := update_field():
                    check_list = [item in available_options for item in inner_options]
                    if not all(check_list):
                        print('Você digitou opções inválidas!')
                        continue
                    break
                select_list = [update_options[i] for i in inner_options]
                select_list = (', ').join(select_list)
                # Input nome usuario
                input_where = lambda: input(
                    'Nome do cliente (em branco para pesquisar todos): '
                    )
                while inner := input_where():
                    if inner:
                        validation = db.check_value(
                            table='cliente',
                            attribute='nome',
                            value=inner
                        )
                        if validation:
                            print('Este nome existe na tabela!')
                            result = db.read(
                                fields=select_list,
                                table='cliente',
                                where=inner
                            )
                            display_db_response(result)
                        else:
                            print('Este nome não está contido na tabela!')
                result = db.read(
                    fields=select_list,
                    table='cliente',
                    where=None
                )
                display_db_response(result)
            case '5':
                attrs = db.get_fields('cliente')
                fields = get_attr_options(attrs)
                print(fields)
            case '0':
                print('Saindo do programa!')
                db.close()
                exit()
            case _:
                # system("cls")
                print('Opção Inválida!')
                # db.close()
                continue


if __name__ == '__main__':
    main()
