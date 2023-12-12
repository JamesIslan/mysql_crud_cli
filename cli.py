from crudfuncs import *
from os import getenv
from dotenv import load_dotenv
from pprint import pprint


def show_options() -> None:
    print(f'1 - Inserir Registro')
    print(f'2 - Editar Registro')
    print(f'3 - Remover Registro')
    print(f'4 - Buscar Registro')
    print(f'0 - Encerrar Programa')
    return None


def get_attr_options(attr: tuple | list) -> dict:
    int_enum = enumerate(attr, 1)
    str_enum = [(str(i[0]), i[1]) for i in int_enum]
    return dict(str_enum)


def show_attr_options(options: dict) -> None:
    for k, v in options.items():
        print(f'{k} – {v}')


def display_db_response(raw_response: tuple | list) -> None:
    if raw_response:
        for row in raw_response:
            pprint(row, width=100)
            # print((" "*10).join(row))
    else:
        print('Sua consulta não retornou valores!')


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
                desired_table = lambda: input('Nome da Tabela: ')
                while inner_table := desired_table():
                    if not db.check_table(inner_table):
                        print('Esta tabela não existe!')
                        continue
                    break
                raw_table_fields = db.get_fields(inner_table)
                display_table_fields = [i.capitalize() for i in raw_table_fields]
                data = lambda: input(
                    f'{(", ").join(display_table_fields)} (separado por espaços): '
                ).split()

                while inner_data := data():
                    if len(inner_data) < len(raw_table_fields):
                        print('Há parâmetros faltando!')
                        continue
                    elif len(inner_data) > len(raw_table_fields):
                        print('Há parâmetros a mais!')
                        continue
                    break
                db.create(inner_table, raw_table_fields, inner_data)

            case '2':
                # Checagem tabela
                desired_table = lambda: input('Tabela a ser alterada: ')
                while inner_table := desired_table():
                    if not db.check_table(inner_table):
                        print('Esta tabela não existe!')
                        continue
                    break
                table_pk_field = db.get_pk_field(inner_table)
                # Checagem ID
                registry_id = lambda: input('ID a ser alterado: ')
                while inner_id := registry_id():
                    attribute_checking = db.check_value(
                        table=inner_table,
                        field=table_pk_field,
                        value=inner_id
                    )
                    if not attribute_checking:
                        print('O ID informado não existe!')
                        continue
                    break
                # Campo Alterado
                update_field = lambda: input('Campo a ser alterado: ')
                table_fields = db.get_fields(inner_table)
                update_options = get_attr_options(table_fields)
                print('Que campo você deseja alterar?: ')
                show_attr_options(update_options)
                while inner_option := update_field():
                    if inner_option not in list(update_options.keys()):
                        print('O campo informado não existe!')
                        continue
                    break
                inner_field = update_options[inner_option]
                new_reg_value = input(f'Novo valor para o campo {inner_field}: ')
                db.update(
                    table=inner_table,
                    attribute=inner_field,
                    newvalue=new_reg_value,
                    id_field=table_pk_field,
                    id_value=inner_id
                )
                print('Alteração feita com sucesso!')
            case '3':
                desired_table = lambda: input('Tabela do registro a ser removido: ')
                while inner_table := desired_table():
                    if not db.check_table(inner_table):
                        print('Esta tabela não existe!')
                        continue
                    break
                table_pk_field = db.get_pk_field(inner_table)
                registry_id = lambda: input('ID do registro a ser removido: ')
                while inner_id := registry_id():
                    attribute_checking = db.check_value(
                        table=inner_table,
                        field=table_pk_field,
                        value=inner_id
                    )
                    if not attribute_checking:
                        print('O ID informado não existe!')
                        continue
                    break
                db.delete(table=inner_table, pk_field=table_pk_field, pk_value=inner_id)
                print('Registro removido!')
            case '4':
                desired_table = lambda: input('Tabela a ser consultada: ')
                while inner_table := desired_table():
                    if not db.check_table(inner_table):
                        print('Esta tabela não existe!')
                        continue
                    break
                update_field = lambda: str(input(
                    'Campos a serem exibidos (separados por espaço) '
                    '[em branco para todos]: '
                )).split()
                table_fields = db.get_fields(inner_table)
                update_options = get_attr_options(table_fields)
                available_options = list(update_options.keys())
                show_attr_options(update_options)
                while inner_options := update_field():
                    check_list = [item in available_options for item in inner_options]
                    if not all(check_list):
                        print('Você digitou opções inválidas!')
                        continue
                    break
                select_list = [update_options[i] for i in inner_options]
                select_list = (', ').join(select_list)
                input_where_field = lambda: input(
                    'Campo para pesquisar (em branco para pular): '
                )
                while inner_where_field := input_where_field():
                    if inner_where_field:  # Usuário digitou campo
                        field_checking = db.check_field(
                            table=inner_table,
                            field=inner_where_field
                        )
                        if field_checking:  # Campo digitado existe
                            break
                        print('Este campo não existe!')
                        continue
                    break  # Usuário não digitou campo (mostrar todos)
                if inner_where_field:
                    # Pedir valor
                    input_where_value = input(
                        f'Valor de busca para o campo {inner_where_field}: '
                    )
                else:
                    input_where_value = ''
                result = db.read(
                    fields=select_list,
                    table=inner_table,
                    where_field=inner_where_field,
                    where_value=str(input_where_value)
                )
                display_db_response(result)
            case '0':
                print('Saindo do programa!')
                db.close()
                exit()
            case _:
                print('Opção Inválida!')
                continue


if __name__ == '__main__':
    main()
