import os
import requests

from server.config import config as env_conf

BACKEND_SERVER_DOMAIN = env_conf[os.getenv('ENV')].BACKEND_SERVER_DOMAIN


def update(oid, status, config=None, dtime='-'):
    requests.post(url=BACKEND_SERVER_DOMAIN + '/update',
                  json={'oid': oid,
                        'status': status,
                        'config': config,
                        'dtime': dtime
                        })
