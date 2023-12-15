from . import db, EntityBase


class RegisterCache(db.Model, EntityBase):
    __tablename__ = 'register_cache'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    ip = db.Column('ip', db.TEXT, nullable=False)
    time = db.Column('time', db.TEXT, nullable=False)
    mob = db.Column('mob', db.INTEGER, nullable=False)
    code = db.Column('code', db.INTEGER, nullable=False)
