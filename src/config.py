
from os import getenv, sep
from pathlib import Path
from secrets import token_urlsafe
from subprocess import check_output
from werkzeug.utils import import_string


HERE = Path(__file__).parent.__str__()  # @see https://stackoverflow.com/a/56621841
ROOT_FOLDER = Path.cwd().__str__()
STATIC_FOLDER = getenv(key='STATIC_FOLDER', default=Path(ROOT_FOLDER).joinpath('static').__str__())
TEMPLATE_FOLDER = getenv(key='TEMPLATE_FOLDER', default=STATIC_FOLDER)


class Config:
    DEBUG = getenv(key='FLASK_DEBUG', default=False)
    ENV = getenv(key='FLASK_ENV', default='production')
    ICON = getenv(key='FLASK_ICON',
                  default=Path(ROOT_FOLDER).joinpath('assets', 'images', 'logo.svg').__str__())
    SECRET_KEY = getenv(key='SECRET_KEY', default=token_urlsafe())
    # As of Flask-SQLAlchemy 2.4.0 it is easy to pass in options directly to the underlying engine.
    # This option makes sure that DB connections from the pool are still valid.
    # It is important since many DBaaS options automatically close idle connections.
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True}
    TITLE = getenv(key='FLASK_TITLE', default=Path(ROOT_FOLDER).name)


def output(cmd, verbose=False):
    out = check_output(cmd).__str__()
    if verbose:
        print(out)
    try:
        end = out.rindex('make')
    except ValueError:
        end = out.rindex('\'')
    start = out.rindex('\\n', 0, end) + 2
    return out[start:end]


class MixinConfig(Config):
    SQLALCHEMY_DATA = {
        'db': getenv(key='POSTGRES_DB', default='postgres'),
        'host': getenv(key='POSTGRES_HOST', default=output(cmd='make network')),
        'port': getenv(key='POSTGRES_PORT', default=output(cmd='make port')),
        'pw': getenv(key='POSTGRES_PASSWORD'),
        'user': getenv(key='POSTGRES_USER', default='postgres')}
    SQLALCHEMY_DATABASE_URI =\
        'postgres+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(**SQLALCHEMY_DATA)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class StageConfig(MixinConfig):
    DEBUG = getenv(key='FLASK_DEBUG', default=True)
    ENV = getenv(key='FLASK_ENV', default='development')
    SQLALCHEMY_ECHO = True


class TestingConfig(MixinConfig):
    ENV = getenv(key='FLASK_ENV', default='testing')
    TESTING = True


def files(src='', pattern='*.py'):
    return Path(HERE).joinpath(src).glob(pattern=pattern)


def import_file(src, verbose=False):
    parent = Path(src).parent.__str__().replace(HERE, '')[1:].replace(sep, '.')
    import_name = '%s.%s' % (parent, Path(src).stem)
    if verbose:
        print('\t`%s`...' % import_name)
    return import_string(import_name=import_name)
