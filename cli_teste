from crud import *

db = DataBase()
db.connect(
    host=getenv("HOST", ""),
    user=getenv("USER", ""),
    password=getenv("PASSWORD", ""),
    db_name=getenv("DB_NAME", "")
)
tabelacliente = TableCliente()  # Instância

# Create
tabelacliente.create(
    'teste1', 'teste2', 'teste3', 'teste4'
)

# Read
response = tabelacliente.read()
print(response)

# Update
tabelacliente.update(
    attribute='nome',
    newvalue='kaiovitor',
    pk_value='13'
)

# Delete
tabelacliente.delete(pk_value='7')

db.close()
