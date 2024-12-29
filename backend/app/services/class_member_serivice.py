from app.models.class_member import ClassMember
from app import db


# 分页获取班级
def query_class_member_list(page, per_page):
    # 查询分页数据
    pagination = ClassMember.query.paginate(page=page, per_page=per_page, error_out=False)

    # 获取分页结果
    class_members = [{'id': class_member.id,
                      's_id': class_member.s_id,
                      'c_id': class_member.c_id
                      } for class_member in pagination.items]

    # 返回分页结果和元数据
    return {
        'class_members': class_members,
        'total': pagination.total  # 数据总条数
    }, 200


# 创建新班级
def add_class_member(class_member):
    temp = ClassMember(s_id=class_member.s_id, c_id=class_member.c_id)
    db.session.add(temp)
    db.session.commit()
    return {'message': '添加班级成员成功！'}, 200


# 删除班级
def delete_class_member(id):
    temp = ClassMember.query.get(id)
    if not temp:
        return {'message': '该班级成员不存在'}, 404

    db.session.delete(temp)
    db.session.commit()
    return {'message': '删除班级成员成功！'}, 200
