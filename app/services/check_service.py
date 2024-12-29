from app.models.check_list import CheckList
from app.models.check_info import CheckInfo


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
