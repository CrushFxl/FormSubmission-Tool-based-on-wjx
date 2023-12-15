import os

from app import create_app

app = create_app(os.getenv('ENV') or 'production')     # 设置上线环境


if __name__ == '__main__':
    conf = dict(app.config.items())
    app.run(host=conf['HOST'], port=conf['PORT'])
