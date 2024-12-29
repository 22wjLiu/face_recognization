from app import db


class Class_(db.Model):
    __tablename__ = 'class'  # 表名 'class'

    id = db.Column(db.Integer, primary_key=True)  # 班级ID
    name = db.Column(db.String(255), nullable=False)  # 班级名称

    # 关联关系
    check_lists = db.relationship('CheckList', back_populates='classes', lazy=True)
    class_members = db.relationship('ClassMember', back_populates='classes', lazy=True)
