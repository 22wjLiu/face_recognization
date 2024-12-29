from app.models.check_list import CheckList
from app.models.check_info import CheckInfo
from app.models.class_member import ClassMember
from app import db


def query_check_list_by_page(page, per_page):
    # 查询分页数据
    pagination = CheckList.query.paginate(page=page, per_page=per_page, error_out=False)

    # 获取分页结果
    check_lists = [{'id': check_list.id,
                    'c_id': check_list.c_id,
                    'create_time': check_list.create_time,
                    'end_time': check_list.end_time} for check_list in pagination.items]

    # 返回分页结果和元数据
    return {
        'checkLists': check_lists,
        'total': pagination.total  # 数据总条数
    }, 200


def query_check_info_list_by_page(page, per_page):
    # 查询分页数据
    pagination = CheckInfo.query.paginate(page=page, per_page=per_page, error_out=False)

    # 获取分页结果
    check_info_list = [{'id': check_info.id,
                        's_id': check_info.s_id,
                        'c_id': check_info.c_id,
                        'status': check_info.status} for check_info in pagination.items]

    # 返回分页结果和元数据
    return {
        'checkInfoList': check_info_list,
        'total': pagination.total  # 数据总条数
    }, 200


# 创建签到记录
def add_check_list(check_list):
    new_check_list = CheckList(c_id=check_list['c_id'],
                               create_time=check_list['create_time'],
                               end_time=check_list['end_time'])

    db.session.add(new_check_list)
    db.session.commit()

    class_members = ClassMember.query.filter(ClassMember.c_id == check_list['c_id']).all()

    for member in class_members:
        new_check_info = CheckInfo(s_id=member.s_id,
                                   c_id=new_check_list.id,
                                   status=0)
        db.session.add(new_check_info)

    db.session.commit()
    return {'message': '创建签到记录成功！'}, 200


# 更新签到详情信息
def update_check_info(s_ids, c_id):

    check_infos = CheckInfo.query.filter(CheckInfo.c_id == c_id).all()

    if not check_infos:
        return {'message': '未找到符合条件的考勤详情！'}, 404

    # 更新符合条件的考勤详情的状态
    updated = False
    for check_info in check_infos:
        if check_info.s_id in s_ids:
            check_info.status = 1
            updated = True

    # 如果没有任何记录被更新
    if not updated:
        return {'message': '未找到符合条件的考勤详情！'}, 400

    # 提交更改
    db.session.commit()
    return {'message': '考勤详情更新成功！'}, 200


# 删除签到记录
def delete_check_list(id):
    check_list = CheckList.query.get(id)
    if not check_list:
        return {'message': '该考勤记录不存在'}, 404

    check_infos = CheckInfo.query.filter(CheckInfo.c_id == id).all()

    for check_info in check_infos:
        db.session.delete(check_info)

    db.session.delete(check_list)
    db.session.commit()
    return {'message': '删除考勤记录成功！'}, 200
