from flask import Blueprint, request, jsonify
from app.services.class_service import query_class_list  # 导入服务层函数

class_bp = Blueprint('class', __name__)


# 获取所有班级
@class_bp.route('/class/queryClassList', methods=['GET'])
def query_student_list():
    # 获取分页参数，默认为第一页，每页10条
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    response, status_code = query_class_list(page, per_page)

    return jsonify(response), status_code
