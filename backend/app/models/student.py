from app import db


class Student(db.Model):
    __tablename__ = 'student'  # 表名 'students'

    id = db.Column(db.Integer, primary_key=True)  # 学生ID
    name = db.Column(db.String(100), nullable=False)  # 学生姓名

    # 关联关系
    features = db.relationship('Feature', back_populates='students', lazy=True)
    check_info = db.relationship('CheckInfo', back_populates='students', lazy=True)
    class_members = db.relationship('ClassMember', back_populates='students', lazy=True)
