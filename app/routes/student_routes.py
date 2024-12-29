from flask import Blueprint, request, jsonify
from app.services.student_service import query_student_list# 导入服务层函数

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
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'message': 'Name is required'}), 400

    new_student = Student(name=data['name'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'id': new_student.id, 'name': new_student.name}), 201


# 更新学生信息
@student_bp.route('/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404

    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'message': 'Name is required'}), 400

    student.name = data['name']
    db.session.commit()
    return jsonify({'id': student.id, 'name': student.name}), 200


# 删除学生
@student_bp.route('/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully'}), 200

