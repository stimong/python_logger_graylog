#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: second_dir/second_dir_sample.py
Description: Sample code for retrieving logs from subfolders
"""

# ModuleNotFoundError: No module named 에러가 뜰것이기 때문에 아래와같이 __init__.py 추가
try:
    import __init__
except:
    pass

from log_utils.basic_logger import CustomLogger, make_dir

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
