from flask import Blueprint, request, jsonify, send_from_directory
from app.services.class_service import # 导入服务层函数

class_bp = Blueprint('class', __name__)

