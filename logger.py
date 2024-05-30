import time
from config import log_base

# generate log name
def generate_log_name():
    t = time.localtime()
    log_name = f"{t.tm_year}-{t.tm_mon}-{t.tm_mday}.log"
    return log_name

# log an error
def log_error(content):
    log_path = f"{log_base}/{generate_log_name()}"
    t = time.localtime()
    with open(log_path, 'a') as f:
        f.write(f"[{t.tm_year}-{t.tm_mon}-{t.tm_mday} {t.tm_hour}:{t.tm_min}:{t.tm_sec}] [ERROR]: {content}\n")

# record info
def log_info(content):
    log_path = f"{log_base}/{generate_log_name()}"
    t = time.localtime()
    with open(log_path, 'a') as f:
        f.write(f"[{t.tm_year}-{t.tm_mon}-{t.tm_mday} {t.tm_hour}:{t.tm_min}:{t.tm_sec}] [INFO]: {content}\n")

# record warning
def log_warning(content):
    log_path = f"{log_base}/{generate_log_name()}"
    t = time.localtime()
    with open(log_path, 'a') as f:
        f.write(f"[{t.tm_year}-{t.tm_mon}-{t.tm_mday} {t.tm_hour}:{t.tm_min}:{t.tm_sec}] [WARNING]: {content}\n")
