from datetime import datetime
from util.extensions import bcrypt, db
from flask_login import AnonymousUserMixin, UserMixin
# @see https://stackoverflow.com/a/37473078
class Email(UserMixin,db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'emails'
    

    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    email = db.Column(db.String(200))
    id_user= db.Column(db.Integer,db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self,email):
        """Create instance."""
        db.Model.__init__(self,email=email)
  