"""Database module, including the SQLAlchemy database object and DB-related utilities."""

from werkzeug.utils import import_string

from config import path
from util.extensions import db
from util.mixin import glob


def filename(src):
    return path.splitext(path.basename(src))[0]


def load_models(folder='model'):
    print('Loading models...')
    for item in glob(folder):
        module = '%s.%s' % (folder, filename(item))
        print('\t`%s`...' % module)
        import_string(import_name='%s.%s' % (path.name, module))


def load_fixtures(folder='fixture'):
    print('Loading fixtures...')
    for item in glob(folder):
        module = '%s.%s' % (folder, filename(item))
        print('\t`%s`...' % module)
        import_string(import_name='%s.%s' % (path.name, module)).load(db)


def reference_col(table_name, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey('{0}.{1}'.format(table_name, pk_name)),
        nullable=nullable, **kwargs)
