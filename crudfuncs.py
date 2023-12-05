import mysql.connector as connector


class DataBase():
    def __init__(self, host: str, user: str, password: str, db_name: str):
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
        self.__cursor = self.__connection.cursor(buffered=True)

    def create(self, table: str, fields: list, values: list) -> None:
        query = (
            f'INSERT INTO {table}({(",").join(fields)}) '
            f'VALUES({", ".join(["%s"] * len(fields))})'
        )
        self.__cursor.execute(query, values)
        self.__connection.commit()
        print('Insert realizado!')

    def read(self, fields: str | None = None, table: str | None = 'cliente', where: str | None = None) -> list:
        query = f'SELECT {fields} FROM {table} '
        if where is not None:
            query += f'WHERE nome like "%{where}%"'
        self.__cursor.execute(query)
        response = self.__cursor.fetchall()
        return response

    def update(self, table, attribute, newvalue, id_field, id_value) -> None:
        query = (
            f'UPDATE {table} '
            f'SET {attribute} = %s '  # newvalue
            f'WHERE {id_field} = %s '  # id_value
        )
        self.__cursor.execute(query, (newvalue, id_value))
        self.__connection.commit()

    def delete(self, table: str, pk_field: str, pk_value: str) -> None:
        query = f'DELETE FROM {table} WHERE {pk_field} = %s'
        try:
            self.__cursor.execute(query, (pk_value, ))
            self.__connection.commit()
        except Exception as e:
            raise e

    def check_table(self, table: str) -> bool:
        query = f'SHOW TABLES LIKE "{table}"'
        self.__cursor.execute(query)
        response = self.__cursor.fetchone()
        return bool(response)

    def check_field(self, table: str, field: str) -> bool:
        table_fields = self.get_fields(table)
        print(table_fields)
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
            self.__cursor.execute(query)
            return bool(self.__cursor.fetchone())
        except Exception as e:
            raise e

    def get_fields(self, table: str, PK: bool = False) -> list:

        query = f'DESCRIBE {table}'
        self.__cursor.execute(query)
        response = self.__cursor.fetchall()
        if PK:
            table_fields = [elem[0] for elem in response]
        else:
            table_fields = [elem[0] for elem in response if not 'PRI' in elem]
        return table_fields

    def close(self) -> None:
        self.__connection.close()
        self.__cursor.close()
