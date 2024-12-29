from flask import Blueprint, request, jsonify
from app.services.student_service import query_student_list# 导入服务层函数

check_bp = Blueprint('check', __name__)