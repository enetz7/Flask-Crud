from datetime import datetime

from flask_login import AnonymousUserMixin, UserMixin

from util.extensions import bcrypt, db


# @see https://stackoverflow.com/a/19275188
class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.email = 'guest@guest.net'
        self.role = 'guest'
        self.username = 'Guest'

# @see https://stackoverflow.com/a/37473078
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    postal_code = db.Column(db.String(10))
    username = db.Column(db.String, unique=True)
    password = db.Column(db.LargeBinary(128))
    country = db.Column(db.String(100))
    locality = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phone_number= db.Column(db.String(100))
    id_role = db.Column(db.Integer,db.ForeignKey('roles.id'))
    #id_role = db.relationship("Role",back_populates="id_user")
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    def __init__(self,postal_code,username,password=None, id_role=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self,postal_code=postal_code, username=username, id_role=id_role,
                          created_at=datetime.now(), modified_at=datetime.now(), **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)

    def is_admin(self):
        """Check admin role."""
        return self.role == 'admin'

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)
