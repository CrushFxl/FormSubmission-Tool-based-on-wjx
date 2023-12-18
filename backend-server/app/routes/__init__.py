from .auth import auth_bk
from .user import user_bk
from .order import order_bk
from .query import query_bk

routes = [
    auth_bk,
    user_bk,
    order_bk,
    query_bk
]
