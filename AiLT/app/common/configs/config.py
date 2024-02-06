import json
from dataclasses import dataclass
from pathlib import Path

from app.common.logger.logger import logger

# JSON 유형의 외부 참조 파일을 읽어오는 코드 config_file 별칭 이용
with open('./app/config.json', 'r') as config_file:
    config = json.load(config_file)

# BASE_DIR 변수 선언
base_dir = Path(__file__).resolve().parent.parent

"""
    class Config:
        try 
            config.json을 읽어옵니다.
        except
            로컬 호스팅 설정으로 mongodb의 값을 세팅합니다.
        else 
            config.json의 값에 따라 mongodb의 값을 세팅합니다.
            
    데이터베이스 등의 정보를 초기화하는 클래스입니다.
    코드 노출, 종속 등의 이유로 외부 json 파일을 수정하여 설정하실 수 있습니다.
    !절대로 config.json 파일을 커밋하지 마세요. 보안 상의 문제가 생길 수 있습니다.
    
    작성자 : 정용규
    작성일 : 2024. 01. 14
"""
@dataclass
class DbConfig:
    try:
        with open('./app/config.json', 'r') as config_file:
            config = json.load(config_file)

    except:
        logger.info("Error reading config.json, set it to local host setting")
        DB_URL: str = "mongodb://localhost:27017"
        DB_HOST: str = "localhost"
        DB_PORT: int = 27017
        DB_NAME: str = "local"
        DB_SSL: bool = 0
        LOCAL_CHECK: bool = 1

    else:
        DB_URL: str = config['DATABASE']['DB_URL']
        DB_HOST: str = config['DATABASE']['DB_HOST']
        DB_PORT: int = config['DATABASE']['DB_PORT']
        DB_NAME: str = config['DATABASE']['DB_NAME']
        DB_USER: str = config['DATABASE']['DB_USER']
        DB_PASSWORD: str = config['DATABASE']['DB_PASSWORD']
        DB_SSL: bool = config['DATABASE']['DB_SSL']
        LOCAL_CHECK: bool = 0

    # BASE_DIR 변수 선언
    BASE_DIR = Path(__file__).resolve().parent.parent
