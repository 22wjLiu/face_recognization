from flask import Blueprint, request, jsonify, send_from_directory
from app.services import feature_service  # 导入服务层函数

feature_bp = Blueprint('feature', __name__)


@feature_bp.route('/upload', methods=['POST'])
def upload_img():
    s_id = request.args.get('s_id')  # 获取sId参数
    if 'file' not in request.files:
        return jsonify({"message": "没有上传图片"}), 400

    file = request.files['file']

    # 调用服务层的处理函数
    response, status_code = feature_service.save_face_feature(s_id, file)
    return jsonify(response), status_code


@feature_bp.route('/image/<filename>')
def get_file(filename):
    return send_from_directory('../uploads', filename)


@feature_bp.route('/recognize', methods=['POST'])
def recognise_face():
    c_id = request.args.get('c_id')  # 获取签到ID
    if 'file' not in request.files:
        return jsonify({"message": "没有上传图片"}), 400

    file = request.files['file']

    # 调用服务层的处理函数
    response, status_code = feature_service.recognize(file, c_id)
    return jsonify(response), status_code
