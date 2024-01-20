from pymongo import MongoClient
from app.common.configs.config import DbConfig
from app.common.logger.logger import logger
from app.models.model import ModelDto

# TODO db를 정의하는 database를 부모 클래스로 수정,
#  connection에 상속하는 방법 검토.
# https://mongodb.github.io/node-mongodb-native/api-generated/mongoclient.html
# https://pymongo.readthedocs.io/en/stable/tutorial.html

"""
    class Database:
        def __init__(self)
            config = DbConfig
            connection = create_connection(self)
        close_connection(self)

         DataBase 클래스는 __init__ 함수에 변수와 create_connection()를 선언했고, 
        close_connection()를 선언했습니다. 
         __init__ 함수는 DbConfig의 LOCAL_CHECK에 따라 외부 서버 또는 local 데이터로 바인딩 후 
        MongoDB와 연결합니다.
         connection이 활성 상태라면 close_connection을 이용하여 MongdoDB와 
        연결 해제할 수 있습니다.

    데이터베이스 등의 정보를 초기화하는 클래스입니다.
    코드 노출, 종속 등의 이유로 외부 json 파일을 수정하여 설정하실 수 있습니다.
    !절대로 config.json 파일을 커밋하지 마세요. 보안 상의 문제가 생길 수 있습니다.

    작성자 : 정용규
    작성일 : 2024. 01. 14
"""


class Database:
    def __init__(self, config: DbConfig):
        self.config = config
        self.connection = self.create_connection()

    # TODO mongodb 권한 추가
    def create_connection(self):
        if self.config.LOCAL_CHECK == 0:
            logger.info("Connecting to server")
            return MongoClient(  # username=self.config.DB_USER,
                # password=self.config.DB_PASSWORD,
                host=self.config.DB_HOST,
                port=self.config.DB_PORT,
                ssl=self.config.DB_SSL)

        else:
            logger.info("Connecting to server using local mode")
            return MongoClient(host=self.config.DB_HOST,
                               port=self.config.DB_PORT)

    """
        close_connection(self), check_connection(self)

        close_connection()과 check_connection은 테스트를 위한 함수입니다.
        TODO pymongo는 데이터베이스와 연결하고 닫는 함수를 제공하지 않습니다.
        pymongo는 풀링 기능을 사용하여 자동 처리합니다.

        작성자 : 정용규
        작성일 : 2024. 01. 16
    """

    def close_connection(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
            logger.info("Connection closed successfully.")
        else:
            logger.info("Connection-aleady-dead")

    def check_connection(self):
        try:
            self.connection.server_info()
            logger.info("Connection is alive.")

        except Exception as e:
            logger.error(f"Connection error: {e}")

    # TODO DTO의 부모 클래스로부터 상속 받은 클래스 사용 가능하도록 수정.
    def insert_collection(self, collection_name, dto: ModelDto):
        collection = self.connection[collection_name]
        result = collection.insert_one(dto.model_dump())
        return str(result.inserted_id)

    def select_collection(self, collection_name, query):
        collection = self.connection[collection_name]
        document = collection.find_one(query)
        return document

    def select_collections(self, collection_name, query):
        collection = self.connection[collection_name]
        documents = collection.find(query)
        return list(documents)

    def update_collection(self, collection_name, query, dto: ModelDto):
        collection = self.connection[collection_name]
        result = collection.update_one(query, {"$set": dto})
        return result.modified_count > 0

    def delete_collection(self, collection_name, query):
        collection = self.connection[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count > 0
