import os
import cv2
from app.models.feature import Feature
from werkzeug.utils import secure_filename
import time
from flask import g
from app.config import Config
from app import db

def generate_filename(original_filename):
    # 使用时间戳生成唯一前缀
    timestamp = int(time.time())
    # 获取文件扩展名
    extension = original_filename.rsplit('.', 1)[-1] if '.' in original_filename else ''
    # 使用 secure_filename 清理原始文件名
    safe_filename = secure_filename(original_filename.rsplit('.', 1)[0])
    # 动态生成文件名
    return f"{safe_filename}_{timestamp}.{extension}"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def save_face_feature(s_id, file):
    if not file or not allowed_file(file.filename):
        return {"message": "不合法文件格式"}, 400

    filename = generate_filename(file.filename)
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)

    # 确保上传文件夹存在
    if not os.path.exists(Config.UPLOAD_FOLDER):
        os.makedirs(Config.UPLOAD_FOLDER)  # 如果文件夹不存在，则创建文件夹

    try:
        file.save(filepath)

        # 读取图片
        img = cv2.imread(filepath)

        # 提取人脸特征
        face_features, _ = g.face.get_feature(img)

        if len(face_features) == 0:
            return {"message": "图片未识别到人脸特征！"}, 400

        feature = face_features[0]
        features_blob = feature.tobytes()  # 转换特征为字节流

        stored_img_path = f'{Config.RESPONSE_FOLDER}/{filename}'

        # 将特征存入数据库
        try:
            # 使用 db.session 来管理数据库操作
            new_feature = Feature(s_id=s_id, feature=features_blob, img_url=stored_img_path)  # 假设你有 Feature 这个模型
            db.session.add(new_feature)
            db.session.commit()

            return {"message": "人脸图片特征保存成功!", "data": stored_img_path}, 200

        except Exception as e:
            db.session.rollback()  # 出现异常时回滚事务
            return {"message": f"数据库操作失败: {str(e)}"}, 500

    except Exception as e:
        return {"message": f"文件保存失败: {str(e)}"}, 500

def recognize(file):
    if not file or not allowed_file(file.filename):
        return {"message": "不合法文件格式"}, 400

    filename = generate_filename(file.filename)
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)

    # 确保上传文件夹存在
    if not os.path.exists(Config.UPLOAD_FOLDER):
        os.makedirs(Config.UPLOAD_FOLDER)  # 如果文件夹不存在，则创建文件夹

    try:
        file.save(filepath)

        # 读取图片
        img = cv2.imread(filepath)

        # 提取人脸特征
        img, name = g.face.recognize(img, Feature.query.all())

        img.save(filepath)

        stored_img_path = f'{Config.RESPONSE_FOLDER}/{filename}'

        return {"message": "识别成功!", "data": stored_img_path}, 200

        # # 将特征存入数据库
        # try:
        #     # 使用 db.session 来管理数据库操作
        #     new_feature = Feature(s_id=s_id, feature=features_blob, img_url=stored_img_path)  # 假设你有 Feature 这个模型
        #     db.session.add(new_feature)
        #     db.session.commit()
        #
        #     return {"message": "人脸图片特征保存成功!", "data": stored_img_path}, 200
        #
        # except Exception as e:
        #     db.session.rollback()  # 出现异常时回滚事务
        #     return {"message": f"数据库操作失败: {str(e)}"}, 500

    except Exception as e:
        return {"message": f"识别失败: {str(e)}"}, 500
