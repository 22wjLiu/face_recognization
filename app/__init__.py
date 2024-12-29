from flask import Flask, g
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.utils.face_recognize import Face_rec

# 初始化数据库
db = SQLAlchemy()

from app.routes.img_routes import img_bp
from app.routes.student_routes import student_bp
from app.routes.class_routes import class_bp
from app.routes.check_routes import check_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # 初始化数据库
    db.init_app(app)

    with app.app_context():
        db.create_all()  # 确保所有模型的表都已创建

    # 在每次请求之前初始化 Face_rec
    @app.before_request
    def before_request():
        if not hasattr(g, 'face'):  # 确保每个请求只有一个 Face_rec 实例
            g.face = Face_rec()

    # 注册蓝图
    app.register_blueprint(img_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(class_bp)
    app.register_blueprint(check_bp)

    return app
