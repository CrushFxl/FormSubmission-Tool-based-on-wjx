import os

from app import create_app

ENV = os.getenv('ENV') or 'production'     # 设置上线环境

app = create_app(ENV)
conf = dict(app.config.items())

if __name__ == '__main__':
    if ENV == 'development':
        app.run(host=conf['HOST'], port=conf['PORT'])
    else:
        app.run(host=conf['HOST'], port=conf['PORT'],
                ssl_context=('app/misc/hmc.weactive.top.pem',
                             'app/misc/hmc.weactive.top.key'))
