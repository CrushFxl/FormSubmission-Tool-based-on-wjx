from .auth import auth_bk
from .user import user_bk
from .business_order import business_order
from .query import query_bk
from .recharge_order import recharge_order_bk

routes = [
    auth_bk,
    user_bk,
    business_order,
    query_bk,
    recharge_order_bk
]