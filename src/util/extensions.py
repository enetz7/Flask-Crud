"""Extensions module. Each extension is initialized in the app factory located in app.py."""

from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import Model, SQLAlchemy


class CRUDMixin(Model):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    def dict(self):  # @see https://stackoverflow.com/q/1958219/1960546#comment12704240_1960546
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()

    @classmethod
    def get_or_create(cls, defaults=None, **kwargs):
        try:
            return db.session.query(cls).filter_by(**kwargs).one(), False

        except db.exc.NoResultFound:
            if defaults:
                kwargs.update(defaults)
            instance = cls(**kwargs)
            try:
                db.session.add(instance)
                db.session.flush()

                return instance, True
            except db.exc.FlushError:
                db.session.rollback()

                return db.session.query(cls).filter_by(**kwargs).one(), True


bcrypt = Bcrypt()
db = SQLAlchemy(model_class=CRUDMixin)
migrate = Migrate()
