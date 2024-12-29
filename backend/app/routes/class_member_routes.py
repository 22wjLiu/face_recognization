from flask import Blueprint, request, jsonify
from app.services import class_member_serivice # 导入服务层函数

class_member_bp = Blueprint('class_member', __name__)


# 获取所有学生
@class_member_bp.route('/classMember/queryClubMemberList', methods=['GET'])
def query_class_member_list():
    # 获取分页参数，默认为第一页，每页10条
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    response, status_code = class_member_serivice.query_class_member_list(page, per_page)

    return jsonify(response), status_code


# 创建新学生
@class_member_bp.route('/classMember/addClassMember', methods=['POST'])
def add_class_member():
    class_member = request.get_json()
    if not class_member or not class_member.get('s_id'):
        return jsonify({'message': '需要学生ID'}), 400
    if not class_member.get('c_id'):
        return jsonify({'message': '需要班级ID'}), 400

    response, status_code = class_member_serivice.add_class_member(class_member)

    return jsonify(response), status_code


# 删除学生
@class_member_bp.route('/classMember/deleteClassMember', methods=['DELETE'])
def delete_class_member():
    id = request.args.get('id', type=int)

    response, status_code = class_member_serivice.delete_class_member(id)
    return jsonify(response), status_code
