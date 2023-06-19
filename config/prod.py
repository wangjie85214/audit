# -*- coding: utf-8 -*-
from config import RUN_VER
if RUN_VER == 'open':
    from blueapps.patch.settings_open_saas import *  # noqa
else:
    from blueapps.patch.settings_paas_services import *  # noqa

# 正式环境
RUN_MODE = 'PRODUCT'

# 设置平台地址
BK_PAAS_URL = 'dev.womaiyun.com'

# 只对正式环境日志级别进行配置，可以在这里修改
LOG_LEVEL = 'ERROR'

# V2
# import logging
# logging.getLogger('root').setLevel('INFO')
# V3
# import logging
# logging.getLogger('app').setLevel('INFO')


# 正式环境数据库可以在这里配置

DATABASES.update(
    {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'womaiyun',  # 数据库名
            'USER': 'womaiyun',  # 数据库用户
            'PASSWORD': 'womaiyun',  # 数据库密码
            'HOST': 'localhost',  # 数据库主机
            'PORT': '3306',  # 数据库端口
        },
    }
)

