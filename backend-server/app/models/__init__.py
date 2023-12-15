from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class EntityBase(object):
    def to_json(self):
        dic = self.__dict__
        if "_sa_instance_state" in dic:
            del dic["_sa_instance_state"]
        return dic
