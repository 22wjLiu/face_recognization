from app.models.check_list import CheckList
from app.models.check_info import CheckInfo


def query_check_list_by_page(page, per_page):
    # 查询分页数据
    pagination = CheckList.query.paginate(page=page, per_page=per_page, error_out=False)

    # 获取分页结果
    check_lists = [{'id': check_list.id,
                    'c_id': check_list.c_id,
                    ''} for check_list in pagination.items]

    # 返回分页结果和元数据
    return {
        'students': classes,
        'total': pagination.total  # 数据总条数
    }, 200