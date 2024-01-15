
from pymongo import MongoClient
from app.common.configs.config import DbConfig
from app.common.logger.logger import logger
from bson import ObjectId

class Connection:
    def __init__(self, config: DbConfig):
        self.config = config
        self.connection = MongoClient(
            host=config.DB_HOST,
            port=config.DB_PORT,
            username=config.DB_USER,
            password=config.DB_PASSWORD,
            ssl=config.DB_SSL,
        )
        self.db = self.connection[config.DB_NAME]

    def close_connection(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
            print("Connection closed successfully.")
        else:
            print("Connection already closed")

    def check_connection(self):
        try:
            self.connection.server_info()
            print("Connection is alive.")
        except Exception as e:
            print(f"Connection error: {e}")

    def insert_document(self, collection_name, document):
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return str(result.inserted_id)

    def find_document(self, collection_name, query):
        collection = self.db[collection_name]
        document = collection.find_one(query)
        return document

    def find_documents(self, collection_name, query):
        collection = self.db[collection_name]
        documents = collection.find(query)
        return list(documents)

    def update_document(self, collection_name, query, update_data):
        collection = self.db[collection_name]
        result = collection.update_one(query, {"$set": update_data})
        return result.modified_count > 0

    def delete_document(self, collection_name, query):
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count > 0