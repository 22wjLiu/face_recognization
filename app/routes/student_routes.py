from flask import Blueprint, request, jsonify
from app.services.student_service import query_student_list, add_student, update_student, delete_student# 导入服务层函数

student_bp = Blueprint('student', __name__)


# 获取所有学生
@student_bp.route('/student/queryStudentList', methods=['GET'])
def query_student_list():
    # 获取分页参数，默认为第一页，每页10条
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    response, status_code = query_student_list(page, per_page)

    return jsonify(response), status_code


# 创建新学生
@student_bp.route('/student/addStudent', methods=['POST'])
def add_student():
    student = request.get_json()
    if not student or not student.get('name'):
        return jsonify({'message': '需要学生姓名'}), 400

    response, status_code = add_student(student)

    return jsonify(response), status_code


# 更新学生信息
@student_bp.route('/student/updateStudent', methods=['PUT'])
def update_student():
    student = request.get_json()
    if not student or not student.get('name'):
        return jsonify({'message': '需要学生姓名'}), 400

    response, status_code = update_student(student)

    return jsonify(response), status_code


# 删除学生
@student_bp.route('/student/updateStudent', methods=['DELETE'])
def delete_student():

    id = request.args.get('id', type=int)

    response, status_code = delete_student(id)
    return jsonify(response), status_code

