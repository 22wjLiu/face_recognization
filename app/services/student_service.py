from app.models.student import Student


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
