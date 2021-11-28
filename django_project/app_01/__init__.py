#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/11/18 5:44 下午
# @Author : XXX
# @File : __init__.py
import pymysql
pymysql.version_info = (1, 4, 13, "final", 0)
pymysql.install_as_MySQLdb()  # 通知Django使用pymysql模块进行连接mysql数据库
