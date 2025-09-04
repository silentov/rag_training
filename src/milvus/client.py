from pymilvus import MilvusClient

from ..configs.configs import Config


config = Config.load()

# TODO: создать клиент для доступа к бд
client = MilvusClient(uri="http://localhost:19530", token="root:Milvus")

client.create_database(db_name="my_database_1")
