from flask import Blueprint, request, jsonify
from app.services import check_service  # 导入服务层函数

check_bp = Blueprint('check', __name__)


# 分页获取签到记录
@check_bp.route('/check/queryCheckListByPage', methods=['GET'])
def query_check_lists():
    # 获取分页参数，默认为第一页，每页10条
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    response, status_code = check_service.query_check_list_by_page(page, per_page)

    return jsonify(response), status_code


# 分页获取签到详情
@check_bp.route('/check/queryCheckInfoListByPage', methods=['GET'])
def query_check_info_lists():
    # 获取分页参数，默认为第一页，每页10条
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    response, status_code = check_service.query_check_info_list_by_page(page, per_page)

    return jsonify(response), status_code


# 创建签到
@check_bp.route('/check/addCheckList', methods=['POST'])
def add_check_list():
    check_list = request.get_json()
    if not check_list or not check_list.get('c_id'):
        return jsonify({'message': '需要学生ID'}), 400
    elif not check_list.get('create_time'):
        return jsonify({'message': '需要创建时间'}), 400
    elif not check_list.get('end_time'):
        return jsonify({'message': '需要截止时间'}), 400

    response, status_code = check_service.add_check_list(check_list)

    return jsonify(response), status_code


# 删除签到记录
@check_bp.route('/check/deleteCheckList', methods=['DELETE'])
def delete_check_list():
    id = request.args.get('id', type=int)

    response, status_code = check_service.delete_check_list(id)
    return jsonify(response), status_code
