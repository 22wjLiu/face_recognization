from app import db


class CheckInfo(db.Model):
    __tablename__ = 'check_info'  # 表名 'check_info'

    id = db.Column(db.Integer, primary_key=True)  # 签到详情ID
    s_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)  # 学生ID
    c_id = db.Column(db.Integer, db.ForeignKey('check_list.id'), nullable=False)  # 签到ID
    status = db.Column(db.String(50), nullable=False)  # 签到状态

    # 关联关系
    check_lists = db.relationship('CheckList', back_populates='check_info', lazy=True)
    students = db.relationship('Student', back_populates='check_info', lazy=True)
