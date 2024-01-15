from pymongo import MongoClient
from app.common.configs.config import DbConfig
from app.common.logger.logger import logger

# TODO 공식 문서 다시 확인
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

    #TODO mongodb 권한 추가
    def create_connection(self):
        if self.config.LOCAL_CHECK == 0:
            logger.info("Connecting to server")
            return MongoClient(#username=self.config.DB_USER,
                               #password=self.config.DB_PASSWORD,
                               host=self.config.DB_HOST,
                               port=self.config.DB_PORT,
                               ssl=self.config.DB_SSL)

        else:
            logger.info("Connecting to server using local mode")
            return MongoClient(host=self.config.DB_HOST,
                               port=self.config.DB_PORT)

    def close_connection(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
            print("Connection closed successfully.")
        else:
            print("Connection-aleady-dead")

    def check_connection(self):
        try:
            self.connection.server_info()
            print("Connection is alive.")

        except Exception as e:
            print(f"Connection error: {e}")

