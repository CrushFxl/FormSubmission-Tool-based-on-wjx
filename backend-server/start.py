import os

from app import create_app
from app.models import db

app = create_app(os.getenv('ENV') or 'production')     # 设置上线环境


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    conf = dict(app.config.items())
    app.run(host=conf['HOST'], port=conf['PORT'])
