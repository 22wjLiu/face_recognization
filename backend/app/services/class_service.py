from app.models.class_ import Class_
from app.models.class_member import ClassMember
from app.models.check_list import CheckList
from app.services import check_service
from app import db


# 分页获取班级
def query_class_list(page, per_page):
    # 查询分页数据
    pagination = Class_.query.paginate(page=page, per_page=per_page, error_out=False)

    # 获取分页结果
    classes = [{'id': class_.id,
                'name': class_.name
                } for class_ in pagination.items]

    # 返回分页结果和元数据
    return {
        'classes': classes,
        'total': pagination.total  # 数据总条数
    }, 200


# 创建新班级
def add_class(class_):
    new_class = Class_(name=class_['name'])
    db.session.add(new_class)
    db.session.commit()
    return {'message': '添加班级成功！'}, 200


# 更新班级信息
def update_class(class_):
    temp = Class_.query.get(class_.id)
    if not temp:
        return {'message': '该班级不存在'}, 404

    temp.name = temp.name
    db.session.commit()
    return {'message': '编辑班级信息成功！'}, 200


# 删除班级
def delete_class(id):
    temp = Class_.query.get(id)
    if not temp:
        return {'message': '该班级不存在'}, 404

    # 删除班级成员
    class_members = ClassMember.query.filter(ClassMember.c_id == id).all()

    for class_member in class_members:
        db.session.delete(class_member)

    # 删除考勤详情记录
    check_lists = CheckList.query.filter(CheckList.c_id == id).all()

    for check_list in check_lists:
        check_service.delete_check_list(check_list.id)

    db.session.delete(temp)
    db.session.commit()
    return {'message': '删除班级成功！'}, 200
