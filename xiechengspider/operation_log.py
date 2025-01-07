import logging
import os
from pathlib import Path

class Logger:
    def __init__(self, log_path: str, log_path_path, log_name: str, level=logging.DEBUG):
        """
        初始化日志对象。
        :param log_path: 日志文件存放的路径。
        :param log_path_path:需要凭借的路径
        :param log_name: 日志文件的名称（不需要扩展名）。
        :param level: 日志级别，默认是DEBUG。
        """

        self.log_path = Path(log_path) / log_path_path
        # 如果路径不存在，则创建路径
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
        self.log_name = log_name
        self.level = level

        # 设置日志的完整文件路径
        # self.log_file = os.path.join(self.log_path, f"{self.log_name}.log")
        name = self.log_name + '.log'
        self.log_file = Path(self.log_path) / name
        print(self.log_file)
        # 创建日志器
        self.logger = logging.getLogger(self.log_name)
        self.logger.setLevel(self.level)

        # 创建日志格式
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # 创建控制台输出
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_format)
        self.logger.addHandler(console_handler)

        # 创建文件输出
        file_handler = logging.FileHandler(self.log_file, mode='a', encoding='utf-8')
        file_handler.setFormatter(log_format)
        self.logger.addHandler(file_handler)

    def set_level(self, level: int):
        """
        设置日志级别。
        :param level: 日志级别，常见的有 logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL。
        """
        self.logger.setLevel(level)

    def debug(self, msg: str):
        self.logger.debug(msg)

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def critical(self, msg: str):
        self.logger.critical(msg)


# 使用示例
if __name__ == "__main__":
    # 创建日志对象
    log_path = "E:/testappuim/test_appium/attraction_log" # 日志文件的路径
    log_path_path = 'shanghai'
    log_name = "app_log"  # 日志文件的名称（不带扩展名）

    logger = Logger(log_path, log_path_path,  log_name)

    # 设置日志级别为 INFO
    logger.set_level(logging.INFO)

    # 记录各种级别的日志
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
