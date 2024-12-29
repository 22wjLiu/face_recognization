from app import db


class ClassMember(db.Model):
    __tablename__ = 'class_member'  # 表名 'class_member'

    id = db.Column(db.Integer, primary_key=True)  # 班级ID
    s_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)  # 学生ID
    c_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)  # 班级ID

    # 关联关系
    students = db.relationship('Student', back_populates='class_members', lazy=True)
    classes = db.relationship('Class_', back_populates='class_members', lazy=True)