#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: main_sample.py
Description: for sample code log import 
"""

# 프로젝트 가장 상위에서 불러올때는 바로 불러 올수 있지만
# 내부 폴더에서 불러올때는 log_utils/__init__.py 참고해서
# 내부 폴더 경로에 __init__.py을 생성해줘야 경로를 찾음
# __init__.py 생성 후 아래 try구문 추가
# try:
#     import __init__
# except:
#     pass

from log_utils.basic_logger import make_dir, CustomLogger

# 콘솔에 저장할 경로 설정 default = ./logs 
make_dir() #logs 폴더가 이미 생성된경우 주석처리 해도 됨.

# logtype_dict={} 이면 기본 설정 은 모두 DEBUG level
logtype_dict={"gray":"DEBUG",
            "consol":"DEBUG",
                "stream":"INFO"} 


c_logger= CustomLogger(name="test_logger_dev01", 
            config_path="log_utils/logging_gray.ini",
            logtype_dict=logtype_dict)

logger = c_logger.logger

# 기본 logger 테스트
logger.info("This is info")
logger.debug("This is debug")
logger.warning('This is warning')

# formatter 추가 테스트
# 기존 formatter에  task_id 등을 로그에 기록하기 위한 설정
logger.info("before add formatter")
c_logger.set_formatter("test","test")

logger.info("after add formatter")
c_logger.change_formatter("test","test msg changed")
logger.info("changed formatter")

c_logger.reset_formatter()
logger.info("reset formatter")
