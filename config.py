class BaseConfig(object):
    DEBUG = True
    SECRET_KEY = '_@awb+dp6x96^m+rcsn7^qh9xl1b)=tm76=jgjue_io2$ycu1m'
    # SQLALCHEMY_DATABASE_URI = 'mysql://bluegarden:XN4rcpxxwXdcDm2E@127.0.0.1:3306/bluegarden'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # Max File size = 10MB


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bluegarden.db'
    UPLOAD_FOLDER = 'images/d/'


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    UPLOAD_FOLDER = 'images/t/'
