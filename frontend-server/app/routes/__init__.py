import os

from .index import index_ft
from .auth import auth_ft
from .order import order_ft
from .home import home_ft
from .recharge import recharge_ft
from .. import config


# 注册的蓝图列表
routes = [
    index_ft,
    auth_ft,
    order_ft,
    home_ft,
    recharge_ft
]


# 注入全局模板变量
URL = config[os.getenv('ENV') or 'production'].CORS_DOMAIN
for route in routes:
    @route.context_processor
    def inject():
        return {'URL': URL}
