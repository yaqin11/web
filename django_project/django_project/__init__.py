import pymysql
pymysql.version_info = (1, 4, 13, "final", 0)
pymysql.install_as_MySQLdb()  # 通知Django使用pymysql模块进行连接mysql数据库
