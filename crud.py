import mysql.connector as connector


class DataBase:
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

    """def __init__(self, host: str, user: str, password: str, db_name: str):
        pass
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.__connection = connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name,
        )
        self.__cursor = self.__connection.cursor(buffered=True)"""

    def create(self, table: str, fields: list, *args) -> None:
        query = (
            f'INSERT INTO {table}({(",").join(fields)}) '
            f'VALUES({", ".join(["%s"] * len(fields))})'
        )
        DataBase.__cursor.execute(query, values)
        DataBase.__connection.commit()
        # print('Insert realizado!')

    def read(self, fields: str | None, table: str | None = 'cliente', where_field: str | None = '', where_value: str | None = '') -> list:
        if fields == '':
            fields = '*'
        query = f'SELECT {fields} FROM {table} '
        if where_field:
            query += f'WHERE {where_field} like "%{where_value}%"'
        DataBase.__cursor.execute(query)
        response = DataBase.__cursor.fetchall()
        return response

    def update(self, table, attribute, newvalue, id_field, id_value) -> None:
        query = (
            f'UPDATE {table} '
            f'SET {attribute} = %s '  # newvalue
            f'WHERE {id_field} = %s '  # id_value
        )
        DataBase.__cursor.execute(query, (newvalue, id_value))
        DataBase.__connection.commit()

    def delete(self, table: str, pk_field: str, pk_value: str) -> None:
        query = f'DELETE FROM {table} WHERE {pk_field} = %s'
        try:
            DataBase.__cursor.execute(query, (pk_value, ))
            DataBase.__connection.commit()
        except Exception as e:
            raise e

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
        pass


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


DataBase.connect('', '', '', '')
tabelausuario = TableUsuario()
