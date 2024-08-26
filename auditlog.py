#!/usr/bin/python3
import os
import logging
import time
import pymysql
import pytz
from datetime import datetime
import json

# 解析审计日志、入库
def parse_and_store_log_data(log_data):
    # 数据库连接参数
    db_host = '172.18.135.141'
    db_user = 'root'
    db_password = '6OeILca2x0c35ga'
    db_name = 'audit'

    # 建立数据库连接
    conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)

    try:
        # 创建游标对象
        cursor = conn.cursor()

        # 解析日志数据
        log_json = json.loads(log_data)
        audit_record = log_json['audit_record']

        timestamp = audit_record['timestamp']
        # 将字符串转换为datetime对象
        utc_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        # 将时区从UTC转换为北京时区
        utc_timezone = pytz.timezone('UTC')
        beijing_timezone = pytz.timezone('Asia/Shanghai')
        beijing_time = utc_timezone.localize(utc_time).astimezone(beijing_timezone)
        # 将时间格式化为字符串
        timestamp = beijing_time.strftime("%Y-%m-%d %H:%M:%S")

        hostname = audit_record['host'] or 'localhost'
        username = audit_record['user']
        source_ip = audit_record['ip']
        session_id = audit_record['connection_id']
        query_id = audit_record['record']
        statement_type = audit_record['command_class']
        database = audit_record['db']
        operation = audit_record['sql_text']

        # 存储到数据库
        sql = "INSERT INTO audit_log (timestamp, hostname, username, source_ip, session_id, query_id, " \
              "statement_type, database_name, operation) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (timestamp, hostname, username, source_ip, session_id, query_id,
                             statement_type, database, operation))

        # 提交事务
        conn.commit()
        logging.info('日志数据已成功存储到数据库')

    except Exception as e:
        logging.error(f'存储日志数据时发生错误：{str(e)}')
        conn.rollback()

    finally:
        # 关闭数据库连接
        conn.close()

# 实时读取本地日志文件
def monitor_local_log_file(log_file_path):
    try:
        with open(log_file_path, 'r') as f:
            f.seek(0, os.SEEK_END)  # 移动到文件末尾
            while True:
                line = f.readline()
                if not line:
                    time.sleep(1)  # 如果没有新内容，等待1秒
                    continue

                # 解析日志并存储到数据库中
                parse_and_store_log_data(line)

    except Exception as e:
        logging.error(f'读取日志文件时发生错误：{str(e)}')

# 定义本地日志文件路径
log_file_path = '/path/to/your/local/audit.log'

# 监控本地日志文件
monitor_local_log_file(log_file_path)
