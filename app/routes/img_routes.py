from flask import Blueprint, request, jsonify, send_from_directory
from app.services.image_service import save_face_feature, recognize  # 导入服务层函数

img_bp = Blueprint('img', __name__)


@img_bp.route('/upload', methods=['POST'])
def upload_img():
    s_id = request.args.get('sId')  # 获取sId参数
    if 'file' not in request.files:
        return jsonify({"message": "没有上传图片"}), 400

    file = request.files['file']

    # 调用服务层的处理函数
    response, status_code = save_face_feature(s_id, file)
    return jsonify(response), status_code


@img_bp.route('/image/<filename>')
def get_file(filename):
    return send_from_directory('../uploads', filename)


@img_bp.route('/recognize', methods=['POST'])
def recognise_face():
    if 'file' not in request.files:
        return jsonify({"message": "没有上传图片"}), 400

    file = request.files['file']

    # 调用服务层的处理函数
    response, status_code = recognize(file)
    return jsonify(response), status_code
