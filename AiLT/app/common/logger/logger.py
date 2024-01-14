import logging
import datetime

"""
    logger.py
    다중 핸들러을 사용하여, Error 로그 레벨은 ./error 폴더에 txt로 기록됩니다.
    Error 로그 레벨 미만은 콘솔에서만 출력됩니다.
    
    작성자 : 정용규
    작성일 : 2024. 01. 14 
"""


# 다중 핸들러 방식 사용, common_logger로 정의, DEBUG 이상 레벨 지정
logger = logging.getLogger("common_logger")
logger.setLevel(logging.DEBUG)

# 포맷 지정
formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
date = str(datetime.datetime.now()).split(" ")[0]

# info, debug를 콘솔에 표시하는 핸들러
handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

# error를 콘솔에 표시하고, log에 기록하는 핸들러
error_handler = logging.FileHandler(f'./log/error_log_{date}.log', mode="w")
error_handler.setFormatter(formatter)
error_handler.setLevel(logging.ERROR)
logger.addHandler(error_handler)

