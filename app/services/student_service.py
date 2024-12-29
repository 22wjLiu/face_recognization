from app.models.student import Student
from app import db


# 获取所有学生
def query_student_list(page, per_page):
    # 查询分页数据
    pagination = Student.query.paginate(page=page, per_page=per_page, error_out=False)

    # 获取分页结果
    students = [{'id': student.id, 'name': student.name} for student in pagination.items]

    # 返回分页结果和元数据
    return {
        'students': students,
        'total': pagination.total  # 数据总条数
    }, 200


# 创建新学生
def add_student(student):
    new_student = Student(name=student['name'])
    db.session.add(new_student)
    db.session.commit()
    return {'message': '添加学生成功！'}, 200


# 更新学生信息
def update_student(student):
    student = Student.query.get(student.id)
    if not student:
        return {'message': '该学生不存在'}, 404

    student.name = student['name']
    db.session.commit()
    return {'message': '编辑学生信息成功！'}, 200


# 删除学生
def delete_student():
    student = Student.query.get(id)
    if not student:
        return {'message': '该学生不存在'}, 404

    db.session.delete(student)
    db.session.commit()
    return {'message': '删除学生成功！'}, 200
