import os

class Config:
    # 上传图片的配置
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', './uploads')  # 默认上传目录
    RESPONSE_FOLDER = os.environ.get('RESPONSE_FOLDER', '/image')  # 默认上传目录
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}  # 允许的图片后缀
    # 数据库配置，连接到 MySQL
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')  # MySQL 用户
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'LiuWanJia')  # MySQL 密码
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')  # MySQL 主机
    MYSQL_PORT = os.environ.get('MYSQL_PORT', 3306)  # MySQL 端口
    MYSQL_DB = os.environ.get('MYSQL_DB', 'face')  # 数据库名

    SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
