from app import db
#from sqlalchemy.dialects.postgresql import JSON


class F1(db.Model):
    __tablename__ = 'f1'

    id = db.Column(db.Integer, primary_key=True)
    f1_score = db.Column(db.Float)
    datetime = db.Column(db.DataTime)    

    def __init__(self, f1_score, datetime):
        self.f1_score = f1_score
        self.datetime = datetime

    def __repr__(self):
        return '<id {}>'.format(self.id)
