from app.models.student import Student
from app.models.class_member import ClassMember
from app.models.feature import Feature
from app.models.check_info import CheckInfo
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

    # 删除班级成员
    class_members = ClassMember.query.filter(ClassMember.s_id == id).all()

    for class_member in class_members:
        db.session.delete(class_member)

    # 删除考勤详情记录
    check_infos = CheckInfo.query.filter(CheckInfo.s_id == id).all()

    for check_info in check_infos:
        db.session.delete(check_info)

    # 删除人脸特征
    features = Feature.query.filter(Feature.s_id == id).all()

    for features in features:
        db.session.delete(features)

    db.session.delete(student)
    db.session.commit()
    return {'message': '删除学生成功！'}, 200
