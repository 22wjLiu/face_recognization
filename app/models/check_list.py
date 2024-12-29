from app import db


class CheckList(db.Model):
    __tablename__ = 'check_list'  # 表名 'check_list'

    id = db.Column(db.Integer, primary_key=True)  # 签到ID
    c_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)  # 班级ID
    create_time = db.Column(db.DateTime, nullable=False)  # 创建时间
    end_time = db.Column(db.DateTime, nullable=False)  # 结束时间

    # 关联关系
    check_info = db.relationship('CheckInfo', back_populates='check_lists', lazy=True)
    classes = db.relationship('Class_', back_populates='check_lists', lazy=True)
