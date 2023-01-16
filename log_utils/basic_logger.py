#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: basic_logger.py
Description: basic logger module
"""
import datetime
import logging
import os
from logging import LoggerAdapter, config, handlers
from os.path import join

import graypy
import logaugment
from pytz import timezone

try:
    import __init__
except:
    pass

current_dir = os.path.dirname(__file__)
parrent_dir = os.path.abspath(os.path.join(current_dir,".."))
# #sys.path.append(current_dir)
# sys.path.append(parrent_dir)

LOG_NAME = "test_logger"

def customTime(*args):
    """
    Convert log time to timezone
        Return: time converted to timezone
    """
    dt = datetime.datetime.now(timezone("Asia/Seoul"))
    return dt.timetuple()
    
def make_dir(dir_name="./logs"):
    """
    Create log directory
    Args:
        dir_name: log directory name
    """
    if os.path.isdir(dir_name)==False:
        os.mkdir(dir_name)
        print("create log directory:",dir_name)
    #else:
    #    print("already exists log directory:",dir_name)

class CustomLogger(logging.LoggerAdapter):
    """Custum logging module"""
    def __init__(self , 
                name=LOG_NAME, 
                config_path="log_utils/logging_gray.ini",
                logtype_dict={}) :
        
        self.logger_name = name 
        #self.config_path = config_path
        self.config_path = join(parrent_dir, config_path)
        self.extra = {"id":None}
        self.logtype_dict = logtype_dict

        #logging.config.fileConfig(self.config_path)
        #self.logger = logging.getLogger(self.logger_name)
        self.logger = None
        self.set_logtype_dict()
        self.load_logger()
        self.setlevel_streamhandler()
        self.set_init_formatter()

    def set_logtype_dict(self):
        """
        Log level setting dictionary by log type initial setting
        """
        if len(self.logtype_dict)==0:
            self.logtype_dict={"gray":"INFO",
                               "consol":"DEBUG",
                               "stream":"DEBUG"}

    def load_logger(self):
        """load log from config file """
        #logging.config.fileConfig(self.config_path)
        # 외부에서 불러올때 경로가 혼선되는것을 방지하기위해, 절대 경로로 변경
        logging.config.fileConfig(self.config_path, defaults={'logfilename': join(parrent_dir, "logs/{}.log".format(LOG_NAME))})
        logging.Formatter.converter = customTime

        custum_dict = {'user': LOG_NAME} # 필터링할 때 넣을 값

        self.logger = logging.getLogger(self.logger_name)
        logging.LoggerAdapter(self.logger, custum_dict)

        #logger_handler = logging.StreamHandler() 
        #self.logger.addHandler(logger_handler)
    
    def set_formatter(self,extra_key="None",extra_msg="None"):
        """
        formatter 추가 및 초기값 설정
        """
        for i in range(len(self.logger.handlers)):
            str2 = " %(message)s"
            str1 = self.logger.handlers[i].formatter._fmt.split(str2)[0]
            add_str = "{} [%({})s]{}".format(str1, extra_key, str2)
            self.logger.handlers[i].setFormatter(logging.Formatter(add_str))
            logaugment.set(self.logger.handlers[i], {extra_key: extra_msg})

    def change_formatter(self,extra_key="None",extra_msg="None"):
        """
        이미 set 이후에 extra_msg 변경
        """
        for i in range(len(self.logger.handlers)):
            logaugment.add(self.logger.handlers[i], {extra_key: extra_msg})

    def set_init_formatter(self):
        """
        ini 파일에 작성된 초기 formatter 추출
        """
        self.init_formatter_console = self.logger.handlers[0].formatter._fmt
        self.init_formatter_file = self.logger.handlers[1].formatter._fmt
        self.init_formatter_gray = self.logger.handlers[2].formatter._fmt

    def reset_formatter(self):
        """
        ini 파일에 작성된 최초 formatter 로 초기화 
        """
        self.logger.handlers[0].setFormatter(logging.Formatter(self.init_formatter_console))
        self.logger.handlers[1].setFormatter(logging.Formatter(self.init_formatter_file))
        self.logger.handlers[2].setFormatter(logging.Formatter(self.init_formatter_gray))
        #logaugment.reset(logger) # 없어도 아마 될것

    def setlevel_streamhandler(self):
        """Log handler level setting.

        self.logtype_dict={"gray":"DEBUG",
                            "consol":"DEBUG",
                            "stream":"DEBUG"}
        """
        log_level_dict = {"INFO":logging.INFO,
                        "DEBUG":logging.DEBUG,
                        "WARNING":logging.WARNING,
                        "ERROR":logging.ERROR}

        for hdlr in self.logger.handlers:
            if isinstance(hdlr,graypy.GELFUDPHandler):
                log_level = log_level_dict[self.logtype_dict["gray"]]
                hdlr.setLevel(log_level)
            elif isinstance(hdlr,handlers.TimedRotatingFileHandler):
                log_level = log_level_dict[self.logtype_dict["consol"]]
                hdlr.setLevel(log_level)
            elif isinstance(hdlr,logging.StreamHandler):
                log_level = log_level_dict[self.logtype_dict["stream"]]
                hdlr.setLevel(log_level)

    def set_user(self, extra):
        """log extra 파라미터 설정"""
        self.extra = extra

    def add_extra_msg(self, msg):
        """extra 값을 log msg에 추가"""

        extra_str = ""
        for key in self.extra.keys():
            extra_str += "({}) ".format(self.extra[key])
        return extra_str + msg


    def info(self, msg):
        """print log info level"""
        self.logger.info(msg, extra=self.extra)

    def debug(self, msg):
        """print log debug level"""
        self.logger.debug(msg, extra=self.extra)

    def warning(self, msg):
        """print log warning level"""
        self.logger.warning(msg, extra=self.extra)

    def critical(self, msg):
        """print log critical level"""
        self.logger.critical(msg, extra=self.extra)

    def error(self, msg):
        """print log error level"""
        self.logger.error(msg, extra=self.extra)

    def exception(self, msg):
        """print log exception level"""
        self.logger.exception(msg, extra=self.extra)


if __name__ == '__main__':
    # 콘솔에 저장할 경로 설정 default = ./logs 
    make_dir()

    # logtype_dict={} 이면 기본 설정 은 모두 DEBUG level
    logtype_dict={"gray":"DEBUG",
                "consol":"DEBUG",
                 "stream":"INFO"} 
    

    c_logger= CustomLogger(name=LOG_NAME, 
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


    