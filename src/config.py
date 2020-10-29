
from os import getenv, pardir, path, urandom

setattr(path, 'here', path.abspath(path.dirname(__file__)))
setattr(path, 'name', path.basename(path.here))
setattr(path, 'root', path.abspath(path.join(path.here, pardir)))
setattr(path, 'test', path.join(path.root, 'test'))


class Config:
    SECRET_KEY = urandom(16)


class MixinConfig(Config):
    from util.mixin import output
    SQLALCHEMY_DATA = {
        'db': getenv('POSTGRES_DB', 'postgres'),
        'host': getenv('POSTGRES_HOST', output('make network')),
        'port': getenv('POSTGRES_PORT', output('make port')),
        'pw': getenv('POSTGRES_PASSWORD', getenv('PGPASSWORD', None)),
        'user': getenv('POSTGRES_USER', 'postgres')}
    SQLALCHEMY_DATABASE_URI =\
        'postgres+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(**SQLALCHEMY_DATA)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class StageConfig(MixinConfig):
    SQLALCHEMY_ECHO = True


class TestingConfig(MixinConfig):
    TESTING = True
