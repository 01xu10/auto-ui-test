# -*- coding:utf-8 -*-
# ---------^-^----------
# @Time : 2023/3/16 19:23
# @Author : chenxx
# @Email : 1150772265@qq.com
# @File : log_controller.py
# ----------------------
import logging
import colorlog
import time
from logging import handlers
from typing import Text
from common.setting import ensure_path_sep
from utils.time_tools.time_control import now_time_day


class LogHandler:
    """ 日志打印封装"""
    # 日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }

    def __init__(
            self,
            filename: Text,
            level: Text = "debug",
            when: Text = "D",
            fmt: Text = "[%(asctime).19s] [%(module)s:%(lineno)d] [%(levelname)s]: %(message)s"
    ):
        self.logger = logging.getLogger(filename)
        sys_fmt = '%(log_color)s' + fmt
        formatter = self.log_color(sys_fmt)

        # 设置日志格式
        format_str = logging.Formatter(fmt)
        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))
        # 往屏幕上输出
        screen_output = logging.StreamHandler()
        # 设置屏幕上显示的格式
        screen_output.setFormatter(formatter)
        # 往文件里写入#指定间隔时间自动生成文件的处理器
        time_rotating = handlers.TimedRotatingFileHandler(
            filename=filename,
            when=when,
            backupCount=3,
            encoding='utf-8'
        )
        # 设置文件里写入的格式
        time_rotating.setFormatter(format_str)
        # 把对象加到logger里
        self.logger.addHandler(screen_output)
        self.logger.addHandler(time_rotating)
        self.log_path = ensure_path_sep('\\logs\\log.log')

    @classmethod
    def log_color(cls, fmt):
        """ 设置日志颜色 """
        log_colors_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        }
        formatter = colorlog.ColoredFormatter(
            fmt,
            log_colors=log_colors_config
        )
        return formatter


f = "[mitmproxy_server]: %(message)s"

INFO = LogHandler(ensure_path_sep(f"\\logs\\info-{now_time_day()}.log"), level='info')
RESP = LogHandler(ensure_path_sep(f"\\logs\\resp_info-{now_time_day()}.log"), level='warning', fmt=f)
ERROR = LogHandler(ensure_path_sep(f"\\logs\\error-{now_time_day()}.log"), level='error')
WARNING = LogHandler(ensure_path_sep(f'\\logs\\warning-{now_time_day()}.log'))


if __name__ == '__main__':
    ERROR.logger.error("测试")
    INFO.logger.info("测试")
    WARNING.logger.warning("测试")
    RESP.logger.warning("测试")
