import mysql.connector as connector
from os import getenv


class DataBase:
    table_name = str()
    table_fields = list()

    @classmethod
    def connect(cls, host: str, user: str, password: str, db_name: str) -> None:
        cls.host = host
        cls.user = user
        cls.password = password
        cls.db_name = db_name
        cls.__connection = connector.connect(
            host=cls.host,
            user=cls.user,
            password=cls.password,
            database=cls.db_name
        )
        cls.__cursor = cls.__connection.cursor(buffered=True)

    def create(self, *args) -> None:
        fields = self.table_fields[1:]
        if len(args) != len(fields):
            raise Exception
        query = (
            f'INSERT INTO {self.table_name}({(", ").join(fields)}) '
            f'VALUES({", ".join(["%s"] * len(fields))})'
        )
        print(query)
        self.__cursor.execute(query, args)
        self.__connection.commit()
        print('Deu tudo certo!')

    def read(
        self,
        fields: list | None = None,
        where_field: str | None = None,
        where_value: str | None = None
    ) -> list:
        if not fields:
            fields = self.table_fields[1:]
        query = f'SELECT {", ".join(fields)} FROM {self.table_name} '
        if where_field:
            query += f'WHERE {where_field} like "%{where_value}%"'
        self.__cursor.execute(query)
        response = self.__cursor.fetchall()
        return response

    def update(
            self,
            attribute,
            newvalue,
            pk_value) -> None:
        pk_field = self.table_fields[0]
        query = (
            f'UPDATE {self.table_name} '
            f'SET {attribute} = "{newvalue}" '  # newvalue
            f'WHERE {pk_field} = "{pk_value}" '  # id_value
        )
        self.__cursor.execute(query)
        self.__connection.commit()
        print('Deu certo o update')

    def delete(self, pk_value: str) -> None:
        pk_field = self.table_fields[0]
        query = (
            f'DELETE FROM {self.table_name} '
            f'WHERE {pk_field} = "{pk_value}"'
        )
        try:
            self.__cursor.execute(query)
            self.__connection.commit()
        except Exception as e:
            raise e
        finally:
            print('Deleção feita com sucesso!')

    def check_table(self, table: str) -> bool:
        query = f'SHOW TABLES LIKE "{table}"'
        DataBase.__cursor.execute(query)
        response = DataBase.__cursor.fetchone()
        return bool(response)

    def check_field(self, table: str, field: str) -> bool:
        table_fields = self.get_fields(table)
        return field in table_fields

    def check_value(self, table: str, field: str, value: str) -> bool:
        if field == 'nome':
            operator = 'like'
            value_check = f'"%{value}%"'
        else:
            operator = '='
            value_check = f'{value}'
        try:
            query = f'SELECT * FROM {table} WHERE {field} {operator} {value_check}'
            DataBase.__cursor.execute(query)
            return bool(self.__cursor.fetchone())
        except connector.errors.ProgrammingError:
            return False

    def get_fields(self, table: str, PK: bool = False) -> list:
        query = f'DESCRIBE {table}'
        DataBase.__cursor.execute(query)
        response = self.__cursor.fetchall()
        if PK:
            table_fields = [elem[0] for elem in response]
        else:
            table_fields = [elem[0] for elem in response if not 'PRI' in elem]
        return table_fields

    def get_pk_field(self, table: str) -> str:
        query = f'DESCRIBE {table}'
        self.__cursor.execute(query)
        response = self.__cursor.fetchall()
        pk_field = [i[0] for i in response if i[3] == 'PRI'][0]
        return str(pk_field)

    def close(self) -> None:
        self.__connection.close()
        self.__cursor.close()


class TableCliente(DataBase):
    table_name = 'cliente'
    table_fields = ['id_cliente', 'nome', 'email', 'sexo', 'telefone']

    def __init__(self) -> None:
        super().__init__()


class TableProduto(DataBase):
    table_name = 'produto'
    table_fields = ['id_produto', 'nome_produto', 'preco']

    def __init__(self) -> None:
        pass


class TableUsuario(DataBase):
    table_name = 'usuario'
    table_fields = ['idusuario', 'usuario', 'senha']

    def __init__(self) -> None:
        pass
