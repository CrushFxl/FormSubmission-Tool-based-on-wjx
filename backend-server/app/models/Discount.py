from . import db


class Discount(db.Model):
    __tablename__ = 'discount'
    mob = db.Column(db.TEXT, primary_key=True)
