# python 로그 샘플 
gray log 를 포함한 python logger 예제코드

======================
## git 프로젝트 다운로드
./git_example.txt

======================
## Requirements
ubuntu 18.04 | python3.8.11 
``` 
pip install -r requirements.txt 
wheel
formatter
logaugment
pytz
graypy
목록에 없는 pkg는 알아서 설치해주세요
``` 

======================
## 초기 설정
./log_utils/logging_gray.ini 파일의
모든 로그이름을 "test_logger_dev01" -> "원하는로그이름" 으로 변경해주세요

./log_utils/basic_logger.py 파일의
모든 로그이름을 "test_logger_dev01" -> "원하는로그이름" 으로 변경해주세요

======================
## test code
``` 
# 프로젝트 최상위경로에서 실행 예제
python ./main_sample.py

# 프로젝트 하위경로에서 실행 예제
python ./second_dir/second_dir_sample.py
``` 

``` 
# 콘솔에 저장할 경로 설정 default = ./logs 
make_dir()

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
``` 