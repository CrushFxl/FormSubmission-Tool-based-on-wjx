from .auth import auth_bk
from .user import user_bk
from .business_order import business_order_bk
from .query import query_bk
from .recharge_order import recharge_order_bk
from .api.task import task_bk

routes = [
    auth_bk,
    user_bk,
    business_order_bk,
    query_bk,
    recharge_order_bk,
    task_bk
]
