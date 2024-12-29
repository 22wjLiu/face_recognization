from app.models.class_ import Class_


def query_student_list(page, per_page):
    # 查询分页数据
    pagination = Class_.query.paginate(page=page, per_page=per_page, error_out=False)

    # 获取分页结果
    classes = [{'id': class_.id, 'name': class_.name} for class_ in pagination.items]

    # 返回分页结果和元数据
    return {
        'students': classes,
        'total': pagination.total  # 数据总条数
    }, 200
