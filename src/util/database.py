"""Database module, including the SQLAlchemy database object and DB-related utilities."""

from sqlalchemy import Column, ForeignKey

from config import files, import_file
from util.extensions import Base, db

Base.query = db.session.query_property()


def load_fixtures():
    print('Loading fixtures...')
    for file in files(src='fixture'):
        import_file(src=file, verbose=True).load(db)


def reference_col(table_name, nullable=False, pk_name='id',
                  foreign_key_kwargs=None, column_kwargs=None):
    """Column that adds primary key foreign key reference.
    Usage: ::
        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    foreign_key_kwargs = foreign_key_kwargs or {}
    column_kwargs = column_kwargs or {}

    return Column(
        ForeignKey(f"{table_name}.{pk_name}", **foreign_key_kwargs),
        nullable=nullable,
        **column_kwargs,
    )
