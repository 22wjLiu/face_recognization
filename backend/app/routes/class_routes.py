from flask import Blueprint, request, jsonify
from app.services import class_service # 导入服务层函数

class_bp = Blueprint('class', __name__)


# 分页获取班级
@class_bp.route('/class/queryClassList', methods=['GET'])
def query_class_list():
    # 获取分页参数，默认为第一页，每页10条
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    response, status_code = class_service.query_class_list(page, per_page)

    return jsonify(response), status_code


# 创建新班级
@class_bp.route('/class/addClass', methods=['POST'])
def add_class():
    class_ = request.get_json()
    if not class_ or not class_.get('name'):
        return jsonify({'message': '需要班级名称'}), 400

    response, status_code = class_service.add_class(class_)

    return jsonify(response), status_code


# 更新班级信息
@class_bp.route('/class/updateClass', methods=['PUT'])
def update_class():
    class_ = request.get_json()
    if not class_ or not class_.get('name'):
        return jsonify({'message': '需要班级名称'}), 400

    response, status_code = class_service.update_class(class_)

    return jsonify(response), status_code


# 删除班级
@class_bp.route('/class/deleteClass', methods=['DELETE'])
def delete_class():
    id = request.args.get('id', type=int)

    response, status_code = class_service.delete_class(id)
    return jsonify(response), status_code
