from app import db


class Feature(db.Model):
    __tablename__ = 'features'  # 表名 'features'

    id = db.Column(db.Integer, primary_key=True)  # 特征ID
    s_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)  # 学生ID
    feature = db.Column(db.LargeBinary, nullable=False)  # 存储特征数据（二进制数据）
    img_url = db.Column(db.String(255), nullable=False)

    # 关联关系
    students = db.relationship('Student', back_populates='features', lazy=True)
