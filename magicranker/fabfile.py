from fabric.api import run, env

from backend import jobs


def prod():
    env.hosts = private.PROD_SERVERS


def local():
    env.hosts = ['localhost']
    

def daily_stock_update():
    with run('export DJANGO_SETTINGS_MODULE=magicranker.settings'):
        if jobs.get_updated_stock_list():
            jobs.set_unlisted_companies()
