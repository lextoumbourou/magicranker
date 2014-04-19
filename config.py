# -*- coding: utf-8 -*-
import os

import private

AVAILABLE_CONFIGS = {
    'production': 'config.ProductionConfig',
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig'
}
DEFAULT_CONFIG = 'development'


class Config(object):
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    DEBUG = False
    ASSETS_LOAD_PATH = [
        os.path.join(PROJECT_ROOT, 'app', 'assets')
    ]


class ProductionConfig(Config):
    SECRET_KEY = private.SECRET_KEY
    ASESTS_AUTO_BUILD = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(
        private.PROD_DB_USER,
        private.PROD_DB_PASS,
        private.PROD_DB_HOST,
        private.DB_NAME
    )


class DevelopmentConfig(Config):
    SECRET_KEY = private.SECRET_KEY
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(
        private.DEV_DB_USER,
        private.DEV_DB_PASS,
        private.DEV_DB_HOST,
        private.DB_NAME
    )
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    SECRET_KEY = 'testkey'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
