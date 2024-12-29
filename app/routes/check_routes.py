from flask import Blueprint, request, jsonify
from app.services.check_service import (query_check_list_by_page, query_check_info_list_by_page)  # 导入服务层函数

check_bp = Blueprint('check', __name__)


# 获取所有签到
@check_bp.route('/class/queryClassList', methods=['GET'])
def query_check_lists():
    # 获取分页参数，默认为第一页，每页10条
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    response, status_code = query_check_list_by_page(page, per_page)

    return jsonify(response), status_code
